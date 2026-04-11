#!/usr/bin/env python3
"""
GitHub Streak Keeper 🔥
Automatically makes a daily commit to maintain your GitHub contribution streak.
Designed to run via GitHub Actions — no local setup needed.
"""

import os
import json
from datetime import datetime, timezone
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────────────────
REPO_DIR = Path(__file__).parent  # The directory where this script lives
LOG_FILE = REPO_DIR / "streak_log.json"


def update_log() -> dict:
    """Update the streak log file with today's entry."""
    # Load existing log or create new one
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            log_data = json.load(f)
    else:
        log_data = {
            "project": "GitHub Streak Keeper 🔥",
            "description": "Automated daily commits to maintain GitHub contribution streak",
            "started": datetime.now(timezone.utc).isoformat(),
            "total_commits": 0,
            "entries": [],
        }

    # Add today's entry
    now = datetime.now(timezone.utc)
    today_str = now.strftime("%Y-%m-%d")

    # Check if we already committed today
    if log_data["entries"] and log_data["entries"][-1].get("date") == today_str:
        print(f"✅ Already committed today ({today_str}). Skipping.")
        return None

    entry = {
        "date": today_str,
        "timestamp": now.isoformat(),
        "day_number": log_data["total_commits"] + 1,
    }

    log_data["entries"].append(entry)
    log_data["total_commits"] += 1
    log_data["last_commit"] = now.isoformat()

    # Calculate current streak
    log_data["current_streak"] = log_data["total_commits"]

    # Write the updated log
    with open(LOG_FILE, "w") as f:
        json.dump(log_data, f, indent=2)

    return log_data


def update_readme(log_data: dict) -> None:
    """Update the README with current streak stats."""
    readme_path = REPO_DIR / "README.md"
    total = log_data["total_commits"]
    last = log_data.get("last_commit", "N/A")

    # Create a nice streak bar visualization
    streak_bar = "🟩" * min(total, 30)  # Show up to 30 green squares
    if total > 30:
        streak_bar += f" +{total - 30} more"

    content = f"""# 🔥 GitHub Streak Keeper

> Automated daily commits to maintain my GitHub contribution streak.

## 📊 Stats

| Metric | Value |
|--------|-------|
| **Total Commits** | {total} |
| **Current Streak** | {total} days |
| **Last Commit** | {last[:10] if last != "N/A" else "N/A"} |
| **Started** | {log_data.get("started", "N/A")[:10]} |

## 📈 Streak Visualization

{streak_bar}

## ⚙️ How It Works

This repo uses **GitHub Actions** to automatically run every day:
1. Update `streak_log.json` with today's timestamp
2. Update this README with current stats
3. Commit and push the changes

No local setup needed — GitHub handles everything! ☁️

---

*Powered by [GitHub Streak Keeper](https://github.com) 🚀*
"""

    with open(readme_path, "w") as f:
        f.write(content)


def main():
    print("=" * 50)
    print("🔥 GitHub Streak Keeper")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    is_ci = os.environ.get("GITHUB_ACTIONS") == "true"
    print(f"🌐 Running in: {'GitHub Actions' if is_ci else 'Local'}")
    print("=" * 50)

    # Update the log file
    log_data = update_log()
    if log_data is None:
        return  # Already committed today

    # Update README
    update_readme(log_data)

    print(f"✅ Updated streak_log.json and README.md")
    print(f"🔥 Streak: {log_data['total_commits']} days!")
    print("=" * 50)


if __name__ == "__main__":
    main()
