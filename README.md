# 🌹 Bachata Rhythm Trainer

A self-contained web app for practicing bachata musicality — the three rhythms
**Derecho**, **Majao**, and **Mambo**.

## Features
- **Rhythm Trainer** — synthesized güira / bongó / bass grooves for each rhythm, with a
  visual beat indicator, adjustable tempo (90–160 bpm), and per-instrument mute toggles.
- **Ear Game** — "name that rhythm" ear-training drill with scoring and streaks.
- **4-Week Plan** — a guided practice curriculum with checkboxes and a practice timer.
- **Rhythm Reference** — a cheat-sheet for all three rhythms with audio previews.

No build step, no dependencies — a single `index.html` using the Web Audio API.

## Run locally
Just open `index.html` in any browser, or serve it:

```bash
npx serve .
```

Tap once anywhere to enable sound (browsers block audio until a user gesture).
