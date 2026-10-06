# Find_me **https://find-me-sandy.vercel.app/**

Find where a username exists across 40+ websites: GitHub, YouTube, Telegram, Steam, Bluesky, Mastodon and more.

Type a username or a name. A name with spaces such as `jk abroad` is checked in every common form (`jkabroad`, `jk_abroad`, `jk.abroad`, `jk-abroad`). Accounts that exist are listed first, with a button to open each profile.

## Deploy to Vercel

1. Push this folder to a GitHub repository.
2. On [vercel.com/new](https://vercel.com/new), import the repository.
3. Leave every setting at its default and click **Deploy**.

No build step, environment variables or packages are needed. `vercel.json` already tells Vercel to serve `public/` and run the Python files in `api/` as functions.

## Run locally

Requires Python 3.9 or newer. Nothing to install.

```bash
python3 dev.py
```

Then open http://localhost:8765. `dev.py` serves the site the same way Vercel does, so what works locally works when deployed.

## Project layout

```
public/index.html   The whole website (HTML, CSS and JavaScript in one file)
api/sites.py        GET /api/sites  - list of platforms
api/check.py        GET /api/check?username=NAME&sites=GitHub,YouTube - checks up to 12 sites
api/_core.py        Checking logic shared by the endpoints
api/_sites.py       Platform list: URLs, how to detect an account, allowed username formats
dev.py              Local server for testing
vercel.json         Vercel settings
```

To add a platform, add an entry to `api/_sites.py`.

## Good to know

- Some sites (Instagram, X, TikTok, Facebook, LinkedIn, Reddit and others) block automatic checks. Find_me shows their links under "Check these yourself".
- Sites sometimes block requests from cloud servers, so a few results may show as "Unclear" on the deployed version more often than locally.

## Responsible use

Only public profile pages are checked. A match means the username exists, not that it belongs to a particular person. Use this for your own accounts, brand availability or authorized research. Don't use it to stalk or harass anyone.
