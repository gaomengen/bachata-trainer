# Deploying Bachata Trainer

This folder is a ready-to-go static site (a git repo with history already committed).
You can get it live on Vercel in a couple of minutes. Two paths below — pick one.

---

## Path A — From a computer (fastest, uses GitHub CLI)

Requires the GitHub CLI (`gh`). Install: https://cli.github.com

```bash
cd bachata-app
gh auth login                          # one-time, follow the prompts
gh repo create bachata-trainer --public --source=. --remote=origin --push
```

That creates the public repo AND pushes in one command.

Then deploy with Vercel:

```bash
npm i -g vercel
vercel --prod                          # log in when prompted, accept defaults
```

Vercel auto-detects it as a static site — just press Enter through the prompts.
It prints your live URL when done.

---

## Path B — All from the browser / phone (no CLI)

### 1. Create the repo on GitHub
- Go to https://github.com/new
- Repository name: **bachata-trainer**, visibility **Public**, then **Create repository**.
- On the new repo page, click **uploading an existing file**.
- Upload **index.html** (and optionally README.md, vercel.json) from this folder.
- Commit.

### 2. Deploy on Vercel
- Go to https://vercel.com/new
- Sign in with GitHub, click **Import** next to `bachata-trainer`.
- Framework preset: **Other** (it's plain static). Leave everything default.
- Click **Deploy**. In ~20 seconds you get a live `.vercel.app` URL.

Every future push to the repo auto-redeploys.

---

## Files in this folder
- `index.html`  — the entire app (no dependencies)
- `README.md`   — project description
- `vercel.json` — clean-URL config (optional)
- `.gitignore`

## Updating later
Edit `index.html`, then either `git push` (Path A) or re-upload via GitHub (Path B).
Vercel redeploys automatically.
