"""Platform definitions.

Each site has:
  url      - public profile URL shown to the user ({} = username)
  check    - URL actually requested (defaults to url)
  method   - how to decide whether the account exists:
               "status"      200 = found, 404/410 = not found
               "absent_text" found unless `text` appears in the body
               "present_text" found only if `text` appears in the body
               "manual"      the site blocks automated checks; we only give a link
  category - used for filtering in the UI
  no_redirect / found_codes - optional: don't follow redirects; treat these codes as "found"
"""

SITES = [
    # --- Code & dev ---
    {"name": "GitHub", "category": "Dev", "url": "https://github.com/{}", "method": "status"},
    {"name": "GitLab", "category": "Dev", "url": "https://gitlab.com/{}",
     "check": "https://gitlab.com/api/v4/users?username={}", "method": "absent_text", "text": "[]"},
    {"name": "Bitbucket", "category": "Dev", "url": "https://bitbucket.org/{}/", "method": "status"},
    {"name": "npm", "category": "Dev", "url": "https://www.npmjs.com/~{}", "method": "manual"},
    {"name": "PyPI", "category": "Dev", "url": "https://pypi.org/user/{}/", "method": "manual"},
    {"name": "Docker Hub", "category": "Dev", "url": "https://hub.docker.com/u/{}",
     "check": "https://hub.docker.com/v2/users/{}/", "method": "status"},
    {"name": "Dev.to", "category": "Dev", "url": "https://dev.to/{}", "method": "status"},
    {"name": "Hugging Face", "category": "Dev", "url": "https://huggingface.co/{}", "method": "status"},
    {"name": "Kaggle", "category": "Dev", "url": "https://www.kaggle.com/{}", "method": "manual"},
    {"name": "Replit", "category": "Dev", "url": "https://replit.com/@{}", "method": "status"},
    {"name": "Codeforces", "category": "Dev", "url": "https://codeforces.com/profile/{}",
     "check": "https://codeforces.com/api/user.info?handles={}", "method": "absent_text", "text": "\"FAILED\""},
    {"name": "Hacker News", "category": "Dev", "url": "https://news.ycombinator.com/user?id={}",
     "check": "https://hacker-news.firebaseio.com/v0/user/{}.json", "method": "absent_text", "text": "null"},
    {"name": "Keybase", "category": "Dev", "url": "https://keybase.io/{}",
     "check": "https://keybase.io/_/api/1.0/user/lookup.json?usernames={}", "method": "present_text", "text": "\"basics\""},

    # --- Social ---
    {"name": "Reddit", "category": "Social", "url": "https://www.reddit.com/user/{}", "method": "manual"},
    {"name": "Mastodon (.social)", "category": "Social", "url": "https://mastodon.social/@{}",
     "check": "https://mastodon.social/api/v1/accounts/lookup?acct={}", "method": "status"},
    {"name": "Bluesky", "category": "Social", "url": "https://bsky.app/profile/{}.bsky.social",
     "check": "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={}.bsky.social", "method": "status"},
    {"name": "Telegram", "category": "Social", "url": "https://t.me/{}", "method": "present_text",
     "text": "tgme_page_title", "no_redirect": True},
    {"name": "Tumblr", "category": "Social", "url": "https://{}.tumblr.com",
     "check": "https://api.tumblr.com/v2/blog/{}.tumblr.com/avatar", "method": "status",
     "no_redirect": True, "found_codes": [301, 302]},
    {"name": "Gravatar", "category": "Social", "url": "https://gravatar.com/{}",
     "check": "https://en.gravatar.com/{}.json", "method": "status"},
    {"name": "Linktree", "category": "Social", "url": "https://linktr.ee/{}", "method": "status"},
    {"name": "Instagram", "category": "Social", "url": "https://www.instagram.com/{}/", "method": "manual"},
    {"name": "X (Twitter)", "category": "Social", "url": "https://x.com/{}", "method": "manual"},
    {"name": "TikTok", "category": "Social", "url": "https://www.tiktok.com/@{}", "method": "manual"},
    {"name": "Facebook", "category": "Social", "url": "https://www.facebook.com/{}", "method": "manual"},
    {"name": "Threads", "category": "Social", "url": "https://www.threads.net/@{}", "method": "manual"},
    {"name": "Pinterest", "category": "Social", "url": "https://www.pinterest.com/{}/", "method": "manual"},
    {"name": "Snapchat", "category": "Social", "url": "https://www.snapchat.com/add/{}", "method": "manual"},
    {"name": "LinkedIn", "category": "Social", "url": "https://www.linkedin.com/in/{}", "method": "manual"},

    # --- Media & creative ---
    {"name": "YouTube", "category": "Media", "url": "https://www.youtube.com/@{}", "method": "status"},
    {"name": "Twitch", "category": "Media", "url": "https://www.twitch.tv/{}", "method": "manual"},
    {"name": "SoundCloud", "category": "Media", "url": "https://soundcloud.com/{}", "method": "status"},
    {"name": "Vimeo", "category": "Media", "url": "https://vimeo.com/{}", "method": "status"},
    {"name": "Flickr", "category": "Media", "url": "https://www.flickr.com/people/{}", "method": "status"},
    {"name": "Last.fm", "category": "Media", "url": "https://www.last.fm/user/{}", "method": "status"},
    {"name": "Letterboxd", "category": "Media", "url": "https://letterboxd.com/{}/", "method": "manual"},
    {"name": "Wattpad", "category": "Media", "url": "https://www.wattpad.com/user/{}", "method": "status"},
    {"name": "Patreon", "category": "Media", "url": "https://www.patreon.com/{}", "method": "status"},
    {"name": "itch.io", "category": "Media", "url": "https://{}.itch.io", "method": "status"},

    # --- Gaming & hobbies ---
    {"name": "Steam", "category": "Gaming", "url": "https://steamcommunity.com/id/{}", "method": "absent_text",
     "text": "The specified profile could not be found"},
    {"name": "Chess.com", "category": "Gaming", "url": "https://www.chess.com/member/{}",
     "check": "https://api.chess.com/pub/player/{}", "method": "status"},
    {"name": "Lichess", "category": "Gaming", "url": "https://lichess.org/@/{}",
     "check": "https://lichess.org/api/user/{}", "method": "status"},
    {"name": "MyAnimeList", "category": "Gaming", "url": "https://myanimelist.net/profile/{}", "method": "status"},
    {"name": "Duolingo", "category": "Gaming", "url": "https://www.duolingo.com/profile/{}",
     "check": "https://www.duolingo.com/2017-06-30/users?username={}", "method": "absent_text", "text": "\"users\":[]"},
]

# Allowed username formats per site (approximate). Handles that don't match are
# skipped for that site instead of being checked, which avoids false positives.
PATTERNS = {
    "GitHub": r"[A-Za-z0-9-]{1,39}", "Bitbucket": r"[A-Za-z0-9_-]{1,30}", "Docker Hub": r"[a-z0-9]{4,30}",
    "Dev.to": r"[A-Za-z0-9_]{1,30}", "Hugging Face": r"[A-Za-z0-9-]{2,40}", "Replit": r"[A-Za-z0-9_]{2,15}",
    "Hacker News": r"[A-Za-z0-9_-]{2,15}", "Keybase": r"[A-Za-z0-9_]{2,16}", "Mastodon (.social)": r"[A-Za-z0-9_]{1,30}",
    "Bluesky": r"[A-Za-z0-9-]{1,40}", "Telegram": r"[A-Za-z][A-Za-z0-9_]{4,31}", "Tumblr": r"[A-Za-z0-9-]{1,32}",
    "Gravatar": r"[A-Za-z0-9]{1,40}", "Linktree": r"[A-Za-z0-9._]{1,30}", "YouTube": r"[A-Za-z0-9._-]{3,30}",
    "SoundCloud": r"[A-Za-z0-9_-]{3,25}", "Last.fm": r"[A-Za-z][A-Za-z0-9_-]{1,14}", "Wattpad": r"[A-Za-z0-9_-]{1,20}",
    "Patreon": r"[A-Za-z0-9_]{1,40}", "itch.io": r"[A-Za-z0-9-]{1,40}", "Steam": r"[A-Za-z0-9_-]{2,32}",
    "Chess.com": r"[A-Za-z0-9_-]{3,25}", "Lichess": r"[A-Za-z0-9_-]{2,30}", "MyAnimeList": r"[A-Za-z0-9_-]{2,16}",
    "Duolingo": r"[A-Za-z0-9_]{1,40}", "Instagram": r"[A-Za-z0-9._]{1,30}", "Threads": r"[A-Za-z0-9._]{1,30}",
    "X (Twitter)": r"[A-Za-z0-9_]{1,15}", "TikTok": r"[A-Za-z0-9._]{2,24}", "Facebook": r"[A-Za-z0-9.]{5,50}",
    "Pinterest": r"[A-Za-z0-9_]{3,30}", "Snapchat": r"[A-Za-z][A-Za-z0-9._-]{2,14}", "LinkedIn": r"[A-Za-z0-9-]{3,100}",
    "Reddit": r"[A-Za-z0-9_-]{3,20}", "Twitch": r"[A-Za-z0-9_]{4,25}", "npm": r"[a-z0-9._-]{1,214}",
    "Kaggle": r"[A-Za-z0-9_-]{1,40}", "Letterboxd": r"[A-Za-z0-9_]{2,15}",
}
for _s in SITES:
    if _s["name"] in PATTERNS:
        _s["pattern"] = PATTERNS[_s["name"]]
