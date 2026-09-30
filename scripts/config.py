import os
import json
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = REPO_ROOT / "config.json"
ASSETS_DIR = REPO_ROOT / "assets"

def load_config():
    config = {
        "leetcode_username": "harshsinghtomar",
        "hackerrank_username": "harshsinghtomar1"
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    config.update(data)
        except Exception as e:
            print(f"[Warning] Failed to read {CONFIG_FILE}: {e}")
    return config

def get_settings():
    file_cfg = load_config()

    parser = argparse.ArgumentParser(description="Generate coding contribution graphs for LeetCode and HackerRank.")
    parser.add_argument("--leetcode-user", type=str, default=None, help="LeetCode username")
    parser.add_argument("--hackerrank-user", type=str, default=None, help="HackerRank username")
    parser.add_argument("--out-dir", type=str, default=str(ASSETS_DIR), help="Output directory for generated SVGs")
    args, _ = parser.parse_known_args()

    lc_user = (
        args.leetcode_user
        or os.getenv("LEETCODE_USERNAME")
        or file_cfg.get("leetcode_username")
        or "harshsinghtomar"
    ).strip()

    hr_user = (
        args.hackerrank_user
        or os.getenv("HACKERRANK_USERNAME")
        or file_cfg.get("hackerrank_username")
        or "harshsinghtomar1"
    ).strip()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    return {
        "leetcode_username": lc_user,
        "hackerrank_username": hr_user,
        "assets_dir": out_dir,
        "leetcode_svg": out_dir / "leetcode-contribution.svg",
        "hackerrank_svg": out_dir / "hackerrank-contribution.svg",
    }
