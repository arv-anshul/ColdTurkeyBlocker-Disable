"""
Only For Mac
------------
Disable or Enable all your Cold Turkey Blockers in one command.
"""

import json
import logging
import os
import sqlite3
from pathlib import Path
from typing import Any

MAC_DB_PATH = Path("/Library/Application Support/Cold Turkey/data-app.db")

logging.basicConfig(level=logging.INFO, format="%(levelname)s -> %(message)s")


def blocker_summary(blocks: dict[str, Any]) -> None:
    """Shows a summary of all blocker present in the app in terminal."""
    logging.critical("Blockers Summary...")
    print("--" * 40)
    for blocker in blocks:
        if blocker == "Frozen Turkey":  # Ignore Frozen Turkey block
            continue
        if blocks[blocker]["enabled"] == "true":
            logging.info(f"Block Enabled:  {blocker}")
        else:
            logging.info(f"Block Disabled: {blocker}")
    print("--" * 40)


def disable_blocker(blocks: dict[str, Any]) -> dict[str, Any]:
    print()
    logging.critical("Disabling the blocker...")
    print("--" * 40)
    for blocker in blocks:
        if blocker == "Frozen Turkey":  # Ignore Frozen Turkey block
            continue
        if blocks[blocker]["enabled"] == "true":
            blocks[blocker]["enabled"] = "false"
            logging.info(f"Block Disabled: {blocker}")
    print("--" * 40)
    return blocks


def main():
    # TODO: Configure this program for Windows as well.
    db_path = MAC_DB_PATH

    if not db_path.exists():
        logging.info(f"{db_path = !s}")
        logging.error("Database does not exists.")
        exit(1)

    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()

            s = c.execute(
                "SELECT value FROM settings WHERE key = 'settings'"
            ).fetchone()[0]

            data = json.loads(s)
            blocks = data["blocks"]
            blocker_summary(blocks)  # Display blocks summary in terminal
            blocks = disable_blocker(blocks)
            data["blocks"] = blocks  # Replace the blocks if modified

            c.execute(
                """UPDATE settings set value = ? WHERE "key" = 'settings'""",
                (json.dumps(data),),
            )
        conn.commit()
    except sqlite3.Error:
        logging.error("Failed to Connect with Cold Turkey blocker.")
        raise
    finally:
        os.system("/usr/bin/killall 'Cold Turkey Blocker'")  # noqa: S605


if __name__ == "__main__":
    main()
