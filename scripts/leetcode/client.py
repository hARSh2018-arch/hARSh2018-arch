import json
import datetime
from dataclasses import dataclass, field
from typing import Dict, Optional, List
import requests

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

CALENDAR_QUERY = """
query userProfileCalendar($username: String!, $year: Int) {
  matchedUser(username: $username) {
    username
    profile {
      realName
      ranking
    }
    submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
        submissions
      }
    }
    userCalendar(year: $year) {
      activeYears
      streak
      totalActiveDays
      submissionCalendar
    }
  }
}
"""

@dataclass
class LeetCodeData:
    username: str
    display_name: str
    daily_counts: Dict[str, int] = field(default_factory=dict)
    total_submissions_year: int = 0
    total_solved: int = 0
    easy_solved: int = 0
    medium_solved: int = 0
    hard_solved: int = 0
    streak: int = 0
    total_active_days: int = 0
    ranking: Optional[int] = None
    active_years: List[int] = field(default_factory=list)
    is_valid: bool = False
    message: str = ""

def fetch_leetcode_data(username: str, timeout: int = 15) -> LeetCodeData:
    username = username.strip()
    result = LeetCodeData(username=username, display_name=username)

    if not username:
        result.message = "No username provided"
        return result

    headers = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
        "Referer": f"https://leetcode.com/{username}/",
    }

    try:
        response = requests.post(
            LEETCODE_GRAPHQL_URL,
            json={"query": CALENDAR_QUERY, "variables": {"username": username}},
            headers=headers,
            timeout=timeout,
        )
    except requests.exceptions.RequestException as e:
        result.message = f"Network error: {e}"
        return result

    if response.status_code != 200:
        result.message = f"HTTP {response.status_code}"
        return result

    try:
        data = response.json()
    except Exception:
        result.message = "Invalid JSON response"
        return result

    errors = data.get("errors")
    if errors:
        result.message = errors[0].get("message", "GraphQL error") if isinstance(errors, list) else "GraphQL error"
        return result

    matched_user = data.get("data", {}).get("matchedUser")
    if not matched_user:
        result.message = "User not found or profile is private"
        return result

    profile = matched_user.get("profile") or {}
    real_name = profile.get("realName")
    if real_name and real_name.strip():
        result.display_name = real_name.strip()
    result.ranking = profile.get("ranking")

    submit_stats = matched_user.get("submitStatsGlobal") or {}
    for ac in (submit_stats.get("acSubmissionNum") or []):
        diff = ac.get("difficulty")
        cnt = int(ac.get("count", 0))
        if diff == "All":
            result.total_solved = cnt
        elif diff == "Easy":
            result.easy_solved = cnt
        elif diff == "Medium":
            result.medium_solved = cnt
        elif diff == "Hard":
            result.hard_solved = cnt

    user_calendar = matched_user.get("userCalendar") or {}
    result.streak = int(user_calendar.get("streak", 0))
    result.total_active_days = int(user_calendar.get("totalActiveDays", 0))
    active_years = user_calendar.get("activeYears") or []
    result.active_years = active_years

    # Parse primary calendar
    all_daily_counts: Dict[str, int] = {}
    sub_cal_str = user_calendar.get("submissionCalendar") or "{}"
    try:
        raw_calendar = json.loads(sub_cal_str) if isinstance(sub_cal_str, str) else sub_cal_str
        for ts_str, count in raw_calendar.items():
            dt = datetime.datetime.fromtimestamp(int(ts_str), tz=datetime.timezone.utc)
            all_daily_counts[dt.strftime("%Y-%m-%d")] = int(count)
    except Exception:
        pass

    # If current calendar has 0 submissions but user has active years, fetch all active years
    if not all_daily_counts and active_years:
        for y in active_years:
            try:
                r_y = requests.post(
                    LEETCODE_GRAPHQL_URL,
                    json={"query": CALENDAR_QUERY, "variables": {"username": username, "year": y}},
                    headers=headers,
                    timeout=timeout,
                )
                if r_y.status_code == 200:
                    y_cal_str = r_y.json().get("data", {}).get("matchedUser", {}).get("userCalendar", {}).get("submissionCalendar") or "{}"
                    y_cal = json.loads(y_cal_str) if isinstance(y_cal_str, str) else y_cal_str
                    for ts_str, count in y_cal.items():
                        dt = datetime.datetime.fromtimestamp(int(ts_str), tz=datetime.timezone.utc)
                        all_daily_counts[dt.strftime("%Y-%m-%d")] = int(count)
            except Exception:
                pass

    result.daily_counts = all_daily_counts
    result.total_submissions_year = sum(all_daily_counts.values())
    if result.total_active_days == 0 and all_daily_counts:
        result.total_active_days = len(all_daily_counts)

    result.is_valid = True
    result.message = "OK"

    print(
        f"[LeetCode] Loaded {username}: {result.total_solved} solved, "
        f"{result.total_submissions_year} submissions across {len(all_daily_counts)} active days."
    )
    return result
