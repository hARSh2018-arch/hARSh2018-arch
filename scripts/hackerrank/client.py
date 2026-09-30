import json
import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Optional
import requests

HACKERRANK_BASE = "https://www.hackerrank.com/rest"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "data"

@dataclass
class HackerRankData:
    username: str
    display_name: str
    daily_counts: Dict[str, int] = field(default_factory=dict)
    total_submissions_year: int = 0
    total_solved: int = 0
    streak: int = 0
    total_active_days: int = 0
    badges_count: int = 0
    country: Optional[str] = None
    is_valid: bool = False
    is_cached: bool = False
    message: str = ""

def calculate_streak(daily_counts: Dict[str, int]) -> int:
    if not daily_counts:
        return 0
    today = datetime.datetime.now(datetime.timezone.utc).date()
    yesterday = today - datetime.timedelta(days=1)

    start_date = None
    if today.strftime("%Y-%m-%d") in daily_counts:
        start_date = today
    elif yesterday.strftime("%Y-%m-%d") in daily_counts:
        start_date = yesterday
    else:
        return 0

    streak = 0
    curr = start_date
    while curr.strftime("%Y-%m-%d") in daily_counts:
        streak += 1
        curr -= datetime.timedelta(days=1)
    return streak

def fetch_hackerrank_data(username: str, timeout: int = 15) -> HackerRankData:
    username = username.strip()
    result = HackerRankData(username=username, display_name=username)

    if not username:
        result.message = "No username provided"
        return result

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Referer": f"https://www.hackerrank.com/{username}",
    }

    cache_file = CACHE_DIR / f"hackerrank_{username}_cache.json"

    # 1. Fetch submission histories
    hist_url = f"{HACKERRANK_BASE}/hackers/{username}/submission_histories"
    sub_histories: Dict[str, int] = {}
    network_ok = False

    try:
        r_hist = requests.get(hist_url, headers=headers, timeout=timeout)
        if r_hist.status_code == 200:
            raw_hist = r_hist.json()
            if isinstance(raw_hist, dict):
                network_ok = True
                for k, v in raw_hist.items():
                    try:
                        sub_histories[str(k)] = int(v)
                    except (ValueError, TypeError):
                        pass
        elif r_hist.status_code == 404:
            result.message = "User not found or no public profile"
            return result
    except requests.exceptions.RequestException as e:
        print(f"[HackerRank] Network error: {e}")

    # Fallback to cache if network failed
    if not network_ok and cache_file.exists():
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
                sub_histories = cached_data.get("sub_histories", {})
                result.display_name = cached_data.get("display_name", username)
                result.country = cached_data.get("country")
                result.badges_count = cached_data.get("badges_count", 0)
                result.total_solved = cached_data.get("total_solved", 0)
                result.is_cached = True
                network_ok = True
        except Exception:
            pass

    if not network_ok:
        result.message = "Unable to connect to HackerRank API"
        return result

    # 2. Fetch Profile metadata
    profile_url = f"{HACKERRANK_BASE}/contests/master/hackers/{username}/profile"
    try:
        r_prof = requests.get(profile_url, headers=headers, timeout=timeout)
        if r_prof.status_code == 200:
            prof_data = r_prof.json().get("model") or {}
            real_name = prof_data.get("name")
            if real_name and real_name.strip():
                result.display_name = real_name.strip()
            result.country = prof_data.get("country")
    except Exception:
        pass

    # 3. Fetch Badges
    badges_url = f"{HACKERRANK_BASE}/hackers/{username}/badges"
    total_solved = 0
    badges_count = 0
    try:
        r_badge = requests.get(badges_url, headers=headers, timeout=timeout)
        if r_badge.status_code == 200:
            b_list = r_badge.json().get("models") or []
            badges_count = len(b_list)
            for b in b_list:
                total_solved += int(b.get("solved", 0))
            result.badges_count = badges_count
            result.total_solved = total_solved
    except Exception:
        pass

    now_utc = datetime.datetime.now(datetime.timezone.utc)
    one_year_ago = now_utc - datetime.timedelta(days=370)
    year_str_threshold = one_year_ago.strftime("%Y-%m-%d")

    year_submissions = 0
    active_days_year = 0

    for d_str, count in sub_histories.items():
        if d_str >= year_str_threshold:
            year_submissions += count
            if count > 0:
                active_days_year += 1

    result.daily_counts = sub_histories
    result.total_submissions_year = year_submissions
    result.total_active_days = active_days_year
    result.streak = calculate_streak(sub_histories)
    result.is_valid = True
    result.message = "OK"

    # Save to local cache
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump({
                "username": username,
                "display_name": result.display_name,
                "country": result.country,
                "badges_count": result.badges_count,
                "total_solved": result.total_solved,
                "sub_histories": sub_histories,
                "cached_at": now_utc.isoformat(),
            }, f, indent=2)
    except Exception:
        pass

    print(
        f"[HackerRank] Loaded {username}: {result.total_submissions_year} submissions in past year, "
        f"{len(sub_histories)} all-time active days."
    )
    return result
