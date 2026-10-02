# Spotify integration reference

Four moving parts: PKCE auth, token management, the Web Playback SDK, and playback
control via the Web API.

## Requirements / constraints (the stuff that bites you)

- User needs **Spotify Premium** for full-track playback via the SDK.
- You register a developer app for a **Client ID** — but with PKCE there is **no client
  secret**, so it's safe in front-end code.
- Redirect URI must be `https` (or `http://127.0.0.1:<port>` for local). **`localhost` is
  rejected** — it must be the literal IP.
- `crypto.subtle` (used for the PKCE challenge) only exists in a **secure context** — so
  https or 127.0.0.1, never `file://`.
- Unapproved dev apps are capped at **5 allowlisted users**.
- No `audio-features` / `audio-analysis` for new apps → you **can't auto-detect BPM**.
  That's why tap-tempo exists.

## 1. Config

```js
const CLIENT_ID = '<your client id>';
const REDIRECT  = location.origin + location.pathname;   // must be registered verbatim
const SCOPES = 'streaming user-read-email user-read-private ' +
               'user-read-playback-state user-modify-playback-state ' +
               'playlist-read-private playlist-modify-private';
```

## 2. Auth — Authorization Code + PKCE

Login: make a random `code_verifier`, derive an S256 `code_challenge`, stash the verifier,
redirect to Spotify.

```js
const b64url = buf => btoa(String.fromCharCode(...new Uint8Array(buf)))
  .replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
const sha256 = s => crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));

// PKCE unreserved charset per RFC 7636: ALPHA / DIGIT / "-" / "." / "_" / "~"
const CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~';
const rand = n => [...crypto.getRandomValues(new Uint8Array(n))]
  .map(x => CHARS[x % CHARS.length]).join('');

async function login(){
  const verifier = rand(96);
  localStorage.setItem('sp_verifier', verifier);
  const challenge = b64url(await sha256(verifier));
  const p = new URLSearchParams({ client_id:CLIENT_ID, response_type:'code',
    redirect_uri:REDIRECT, scope:SCOPES,
    code_challenge_method:'S256', code_challenge:challenge });
  location.href = 'https://accounts.spotify.com/authorize?' + p;
}
```

On return, Spotify appends `?code=…`. Exchange it (PKCE — send the verifier, no secret):

```js
async function exchange(code){
  const body = new URLSearchParams({ client_id:CLIENT_ID, grant_type:'authorization_code',
    code, redirect_uri:REDIRECT, code_verifier:localStorage.getItem('sp_verifier') });
  const r = await fetch('https://accounts.spotify.com/api/token',
    { method:'POST', headers:{'Content-Type':'application/x-www-form-urlencoded'}, body });
  return r.json();   // { access_token, refresh_token, expires_in }
}
```

Refresh identically with `grant_type:'refresh_token'` + `refresh_token`. Store
`{access_token, refresh_token, expires_at}` and refresh ~15s before expiry. A `token()`
helper returns a fresh access token on demand:

```js
async function token(){
  if (Date.now() > expiresAt - 15000) await refresh();
  return accessToken;
}
```

## 3. Web Playback SDK — creates the in-browser player device

```js
function initPlayer(){
  window.onSpotifyWebPlaybackSDKReady = () => {
    player = new Spotify.Player({
      name: 'My App',
      getOAuthToken: cb => token().then(cb),   // SDK calls this whenever it needs a token
      volume: 0.85
    });
    player.addListener('ready', ({device_id}) => { DEVICE_ID = device_id; });
    player.addListener('player_state_changed', renderNowPlaying);
    player.addListener('account_error', () => alert('Premium required'));
    player.connect();
  };
  const s = document.createElement('script');
  s.src = 'https://sdk.scdn.co/spotify-player.js';
  document.body.appendChild(s);
}
```

## 3b. Spotify Connect — the mobile path (what this app actually uses)

**The Web Playback SDK does not run in mobile browsers.** Not a bug to work around — it's
unsupported by design, so on a phone the browser can never be the player. Connect solves it
by driving a Spotify app that's already running somewhere (the phone, a desktop, a speaker).

List devices, then target one by `device_id` on every call:

```js
const { devices } = await api('/me/player/devices');
// each: { id, name, type, is_active, is_restricted }
```

Transfer playback to a device:

```js
await api('/me/player', { method:'PUT', body: JSON.stringify({ device_ids:[id], play:false }) });
```

There are no SDK events for a remote device, so poll for now-playing:

```js
const st = await api('/me/player');   // 204 when nothing is active
// st.is_playing, st.item.name, st.item.artists, st.device.id
```

Gotchas:

- A device only appears **while the Spotify app is open** (play something for a second first).
- Connect control also requires **Premium**; a free account gets 403.
- `is_restricted: true` means that device won't accept remote commands.
- Poll on a timer only while the relevant view is visible — otherwise it burns battery and
  eats into the rate limit. `429` means back off.

The SDK and Connect compose: on desktop, initializing the SDK simply adds the browser as one
more device in the same list.

## 4. Playback control

With the SDK, transport is on the player object: `player.togglePlay()`, `player.nextTrack()`,
`player.previousTrack()`. That only works for the SDK's own device.

For Connect — and for uniform behavior across platforms — use the Web API instead, targeting
`device_id`:

```
PUT  /me/player/play?device_id=<id>
PUT  /me/player/pause?device_id=<id>
POST /me/player/next?device_id=<id>
POST /me/player/previous?device_id=<id>
```

To start specific music you POST to the Web API targeting your device — `{uris:[...]}` for
tracks or `{context_uri}` for a playlist/album:

```js
async function play(payload){                    // {uris:[trackUri]} OR {context_uri:playlistUri}
  const t = await token();
  await fetch(`https://api.spotify.com/v1/me/player/play?device_id=${DEVICE_ID}`,
    { method:'PUT', headers:{ Authorization:`Bearer ${t}`, 'Content-Type':'application/json' },
      body: JSON.stringify(payload) });
}
```

Search and playlist lookup are plain GETs with the Bearer token:

```
GET https://api.spotify.com/v1/search?type=track&limit=12&q=<query>
GET https://api.spotify.com/v1/me/playlists?limit=50
```

## 5. Tap-tempo (pure JS, no Spotify)

Collect click timestamps, average the gaps, convert to BPM, fold into a target range:

```js
let taps=[];
tapBtn.onclick = () => {
  const now = performance.now();
  taps = [...taps, now].filter(t => now - t < 3000);      // keep last ~3s
  if (taps.length >= 2){
    const gaps = taps.slice(1).map((t,i)=>t-taps[i]);
    let bpm = Math.round(60000 / (gaps.reduce((a,b)=>a+b)/gaps.length));
    while (bpm>160) bpm/=2; while (bpm<90) bpm*=2;         // fold into a sane octave
    setMetronome(Math.round(bpm));
  }
};
```

> **Note on the fold:** 90–160 is narrower than a full octave (90×2 = 180 > 160), so some
> tempos can't land inside it. A tap at 89 bpm doubles to 178 and stops there, outside the
> range. The loops still terminate — they run in sequence, not nested — but clamp the
> result if you need a hard guarantee it's inside the slider's range.

## Flow to hold in your head

`login()` → redirect → `exchange(code)` → store tokens → `initPlayer()` → on `ready` grab
`DEVICE_ID` → `play()` / `search()` using the Web API, transport via the SDK. Tokens live in
localStorage so a refresh survives reloads; the SDK pulls fresh tokens through
`getOAuthToken`.

---

## Notes for this repo

Nothing here is wired up yet — `index.html` is still fully self-contained with no network
calls. If you build it:

- **Production redirect URI** — register exactly
  `https://bachatamusicalidad.com/`. It's https, so `crypto.subtle` is available.
  If the deployment URL ever changes, the registered URI must change with it.
- **Local dev** — the QA flow in this repo serves on `http://localhost:8765`, which Spotify
  **rejects**. Use `http://127.0.0.1:8765` instead and register that too. Same server,
  different host string; `crypto.subtle` works on 127.0.0.1 but not on `file://`.
- **Tap-tempo fits the existing trainer** — the app's tempo slider is already clamped to
  90–160 (`#bpm`), matching the fold range above. `state.bpm` and `saveTrainer()` are the
  hooks; `setMetronome(bpm)` maps to setting `state.bpm`, updating `#bpm` / `#bpmv`, and
  calling `saveTrainer()`.
- **Premium + the 5-user cap** mean this can't ship to a general audience without Spotify
  app review. Fine for personal use.
