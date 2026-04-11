#!/usr/bin/env python3
"""
Setup script to install/uninstall the cron job for GitHub Streak Keeper.
Usage:
    python3 setup_cron.py install    # Install the cron job
    python3 setup_cron.py uninstall  # Remove the cron job
    python3 setup_cron.py status     # Check if cron job is active
"""

import subprocess
import sys
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
AUTO_COMMIT_SCRIPT = SCRIPT_DIR / "auto_commit.py"
CRON_MARKER = "# GITHUB_STREAK_KEEPER"

# Run daily at 10:00 AM local time
CRON_SCHEDULE = "0 10 * * *"


def get_python_path() -> str:
    """Get the full path to python3."""
    result = subprocess.run(["which", "python3"], capture_output=True, text=True)
    return result.stdout.strip() or "/usr/bin/python3"


def get_current_crontab() -> str:
    """Get the current crontab contents."""
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    if result.returncode != 0:
        return ""
    return result.stdout


def install():
    """Install the cron job."""
    python_path = get_python_path()
    cron_line = f'{CRON_SCHEDULE} {python_path} "{AUTO_COMMIT_SCRIPT}" >> "{SCRIPT_DIR}/cron.log" 2>&1 {CRON_MARKER}'

    current = get_current_crontab()

    # Check if already installed
    if CRON_MARKER in current:
        print("⚠️  Cron job already installed. Updating...")
        lines = [l for l in current.splitlines() if CRON_MARKER not in l]
        current = "\n".join(lines) + "\n" if lines else ""

    # Add the new cron job
    new_crontab = current.rstrip("\n") + "\n" + cron_line + "\n"

    # Install it
    process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
    process.communicate(input=new_crontab)

    if process.returncode == 0:
        print("=" * 50)
        print("✅ Cron job installed successfully!")
        print("=" * 50)
        print(f"📅 Schedule: Every day at 10:00 AM")
        print(f"📂 Script:   {AUTO_COMMIT_SCRIPT}")
        print(f"📝 Log:      {SCRIPT_DIR}/cron.log")
        print(f"🐍 Python:   {python_path}")
        print()
        print("💡 To change the time, edit CRON_SCHEDULE in this file.")
        print("   Format: minute hour day month weekday")
        print("   Examples:")
        print("     '0 9 * * *'   → Every day at 9:00 AM")
        print("     '30 20 * * *' → Every day at 8:30 PM")
        print("     '0 */6 * * *' → Every 6 hours")
    else:
        print("❌ Failed to install cron job.")


def uninstall():
    """Remove the cron job."""
    current = get_current_crontab()

    if CRON_MARKER not in current:
        print("ℹ️  No cron job found to remove.")
        return

    lines = [l for l in current.splitlines() if CRON_MARKER not in l]
    new_crontab = "\n".join(lines) + "\n" if lines else ""

    process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
    process.communicate(input=new_crontab)

    if process.returncode == 0:
        print("✅ Cron job removed successfully!")
    else:
        print("❌ Failed to remove cron job.")


def status():
    """Check if the cron job is active."""
    current = get_current_crontab()

    if CRON_MARKER in current:
        for line in current.splitlines():
            if CRON_MARKER in line:
                print("✅ Cron job is ACTIVE")
                print(f"   {line.replace(CRON_MARKER, '').strip()}")
                break
    else:
        print("❌ Cron job is NOT installed")
        print("   Run: python3 setup_cron.py install")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 setup_cron.py [install|uninstall|status]")
        print()
        print("Commands:")
        print("  install    Install the daily cron job")
        print("  uninstall  Remove the cron job")
        print("  status     Check if cron job is active")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "install":
        install()
    elif command == "uninstall":
        uninstall()
    elif command == "status":
        status()
    else:
        print(f"❌ Unknown command: {command}")
        print("   Use: install, uninstall, or status")
        sys.exit(1)


if __name__ == "__main__":
    main()
