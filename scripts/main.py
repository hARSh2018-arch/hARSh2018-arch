import sys
import datetime
from pathlib import Path

# Add project root to sys.path so modules can be imported directly or via scripts
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.config import get_settings
from scripts.leetcode.client import fetch_leetcode_data
from scripts.hackerrank.client import fetch_hackerrank_data
from scripts.generate_graph.theme import LEETCODE_THEME, HACKERRANK_THEME
from scripts.generate_graph.svg_builder import build_contribution_svg

def main():
    print("=" * 65)
    print("  CODING ACTIVITY CONTRIBUTION GRAPH GENERATOR")
    print("  (LeetCode & HackerRank Contribution Heatmaps)")
    print("=" * 65)

    settings = get_settings()
    lc_user = settings["leetcode_username"]
    hr_user = settings["hackerrank_username"]
    lc_svg_path = settings["leetcode_svg"]
    hr_svg_path = settings["hackerrank_svg"]

    print(f"[Config] LeetCode Username  : {lc_user}")
    print(f"[Config] HackerRank Username: {hr_user}")
    print(f"[Config] Output Directory   : {settings['assets_dir']}")
    print("-" * 65)

    # 1. Fetch LeetCode Data
    print(f"\n[1/2] Fetching LeetCode data for '{lc_user}'...")
    lc_data = fetch_leetcode_data(lc_user)

    # Generate LeetCode SVG (aligned with 53-week GitHub calendar)
    lc_svg = build_contribution_svg(
        theme=LEETCODE_THEME,
        username=lc_data.username,
        display_name=lc_data.display_name,
        daily_counts=lc_data.daily_counts,
        total_submissions=lc_data.total_submissions_year,
        streak=lc_data.streak,
        total_active_days=lc_data.total_active_days,
        solved_count=lc_data.total_solved,
        easy_solved=lc_data.easy_solved,
        medium_solved=lc_data.medium_solved,
        hard_solved=lc_data.hard_solved,
        rank=lc_data.ranking,
        is_valid=lc_data.is_valid,
        status_message=lc_data.message or "OK",
        unit_name="submission",
    )

    lc_svg_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lc_svg_path, "w", encoding="utf-8") as f:
        f.write(lc_svg)
    print(f"  [LeetCode] Successfully generated {lc_svg_path.name}")

    # 2. Fetch HackerRank Data
    print(f"\n[2/2] Fetching HackerRank data for '{hr_user}'...")
    hr_data = fetch_hackerrank_data(hr_user)

    # Generate HackerRank SVG (aligned with 53-week GitHub calendar)
    hr_svg = build_contribution_svg(
        theme=HACKERRANK_THEME,
        username=hr_data.username,
        display_name=hr_data.display_name,
        daily_counts=hr_data.daily_counts,
        total_submissions=hr_data.total_submissions_year,
        streak=hr_data.streak,
        total_active_days=hr_data.total_active_days,
        solved_count=hr_data.total_solved,
        badges_count=hr_data.badges_count,
        is_valid=hr_data.is_valid,
        status_message=hr_data.message or "OK",
        unit_name="submission",
    )

    hr_svg_path.parent.mkdir(parents=True, exist_ok=True)
    with open(hr_svg_path, "w", encoding="utf-8") as f:
        f.write(hr_svg)
    print(f"  [HackerRank] Successfully generated {hr_svg_path.name}")

    print("\n" + "=" * 65)
    print("  SUMMARY:")
    print(f"  LeetCode   : {lc_data.total_solved} solved, {lc_data.total_submissions_year} submissions")
    print(f"  HackerRank : {hr_data.total_solved} solved, {hr_data.total_submissions_year} submissions ({hr_data.badges_count} badges)")
    print("  Both contribution graphs generated successfully!")
    print("=" * 65)

if __name__ == "__main__":
    main()
