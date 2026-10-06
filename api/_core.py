"""Shared checking logic used by the Vercel functions and the local runner.

Files in api/ that start with "_" are not deployed as endpoints by Vercel.
"""
import re
import ssl
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import parse_qs, urlparse

from _sites import SITES

USERNAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,40}$")
MAX_SITES_PER_REQUEST = 12
REQUEST_TIMEOUT = 8
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
SITES_BY_NAME = {s["name"]: s for s in SITES}

SSL_CTX = ssl.create_default_context()
try:
    import certifi  # some Python installs on macOS lack a CA bundle
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    pass


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None  # surface 3xx as HTTPError so found_codes can match it


_https = urllib.request.HTTPSHandler(context=SSL_CTX)
DEFAULT_OPENER = urllib.request.build_opener(_https)
NO_REDIRECT_OPENER = urllib.request.build_opener(_https, _NoRedirect)

# Per-instance cache. On Vercel it lives as long as a warm function instance.
CACHE = {}
CACHE_TTL = 600
CACHE_LOCK = threading.Lock()


def site_domain(site):
    host = urlparse(site["url"].replace("{}", "x")).hostname or ""
    parts = host.split(".")
    return ".".join(parts[-2:]) if parts[0] == "x" else host


def list_sites():
    return [{"name": s["name"], "category": s["category"], "domain": site_domain(s),
             "manual": s["method"] == "manual"} for s in SITES]


def check_site(site, username):
    """Cached check with one retry for transient failures."""
    key = (site["name"], username.lower())
    with CACHE_LOCK:
        hit = CACHE.get(key)
    if hit and time.time() - hit[0] < CACHE_TTL:
        return hit[1]
    result = _check_site(site, username)
    if result["status"] in ("error", "unknown"):
        time.sleep(0.5)
        result = _check_site(site, username)
    if result["status"] in ("found", "not_found", "manual", "invalid"):
        with CACHE_LOCK:
            CACHE[key] = (time.time(), result)
    return result


def _check_site(site, username):
    if site.get("pattern") and not re.fullmatch(site["pattern"], username):
        return {"status": "invalid", "note": f"Not a valid {site['name']} username"}
    url = site["url"].format(username)
    if site["method"] == "manual":
        return {"status": "manual", "url": url, "note": "This site blocks automatic checks"}

    check_url = site.get("check", site["url"]).format(username)
    req = urllib.request.Request(check_url, headers={
        "User-Agent": UA, "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9"})
    opener = NO_REDIRECT_OPENER if site.get("no_redirect") else DEFAULT_OPENER
    try:
        with opener.open(req, timeout=REQUEST_TIMEOUT) as resp:
            code = resp.status
            final_url = resp.geturl()
            body = resp.read(300_000).decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        code, final_url = e.code, check_url
        body = e.read(300_000).decode("utf-8", "ignore") if e.fp else ""
    except Exception as e:  # timeouts, DNS, TLS
        return {"status": "error", "url": url, "note": f"Site didn't respond ({type(e).__name__})"}

    method = site["method"]
    if code in site.get("found_codes", ()):
        return {"status": "found", "url": url, "note": f"HTTP {code}"}
    if method == "absent_text" and code == 400 and site["text"] in body:
        return {"status": "not_found", "url": url, "note": f"HTTP {code}"}
    if code in (404, 410) or (method == "status" and code == 400):
        return {"status": "not_found", "url": url, "note": f"HTTP {code}"}
    if code in (403, 429, 503):
        return {"status": "unknown", "url": url, "note": "Site blocked the check or is rate-limiting"}
    if code >= 400:
        return {"status": "unknown", "url": url, "note": f"Site returned an error (HTTP {code})"}

    # Redirected somewhere that no longer mentions the username (login page, homepage...)
    if username.lower() not in final_url.lower():
        return {"status": "not_found", "url": url, "note": "Redirected away from profile"}

    if method == "absent_text":
        found = site["text"] not in body
    elif method == "present_text":
        found = site["text"] in body
    else:
        found = True
    return {"status": "found" if found else "not_found", "url": url, "note": f"HTTP {code}"}


def handle_check(query_string):
    """GET /api/check?username=NAME&sites=GitHub,YouTube -> (http_status, payload)."""
    q = {k: v[0] for k, v in parse_qs(query_string).items()}
    username = q.get("username", "")
    names = [n for n in q.get("sites", "").split(",") if n]
    if not USERNAME_RE.match(username):
        return 400, {"error": "Invalid username. Use letters, numbers, dots, dashes or underscores."}
    if not names or len(names) > MAX_SITES_PER_REQUEST:
        return 400, {"error": f"Pass 1-{MAX_SITES_PER_REQUEST} site names in 'sites'."}
    unknown = [n for n in names if n not in SITES_BY_NAME]
    if unknown:
        return 400, {"error": "Unknown site: " + ", ".join(unknown)}
    with ThreadPoolExecutor(len(names)) as pool:
        results = dict(zip(names, pool.map(lambda n: check_site(SITES_BY_NAME[n], username), names)))
    return 200, {"username": username, "results": results}
