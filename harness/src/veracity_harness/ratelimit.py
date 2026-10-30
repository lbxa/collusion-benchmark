"""Machine-wide sliding-window request limits per model, shared by every process.

Workers AI limits its larger models to about 20 requests a minute per account and
model; parallel agents and sessions otherwise exhaust retries on HTTP 429.
"""

import asyncio
import os
import random
import sqlite3
import time
from contextlib import closing
from pathlib import Path

WINDOW_SECONDS = 60.0


def default_path() -> Path:
    configured = os.environ.get("VERACITY_RATE_DB")
    return (
        Path(configured)
        if configured
        else Path.home() / ".cache/veracity-harness/request-rate.sqlite"
    )


def try_acquire(path: Path, model: str, per_minute: int, now: float) -> float:
    """Record a request start and return 0, or return the seconds until a slot frees."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path, timeout=30, isolation_level=None)) as database:
        database.execute("CREATE TABLE IF NOT EXISTS starts (model TEXT NOT NULL, at REAL)")
        database.execute("BEGIN IMMEDIATE")
        database.execute("DELETE FROM starts WHERE at <= ?", (now - WINDOW_SECONDS,))
        starts = [
            row[0]
            for row in database.execute(
                "SELECT at FROM starts WHERE model = ? ORDER BY at", (model,)
            )
        ]
        if len(starts) < per_minute:
            database.execute("INSERT INTO starts VALUES (?, ?)", (model, now))
            database.execute("COMMIT")
            return 0.0
        database.execute("COMMIT")
        return starts[len(starts) - per_minute] + WINDOW_SECONDS - now


async def acquire(model: str, per_minute: int, path: Path | None = None):
    # Slots free up in other processes, so poll the shared file rather than an event.
    path = path or default_path()
    while True:
        wait = await asyncio.to_thread(try_acquire, path, model, per_minute, time.time())
        if not wait:
            return
        await asyncio.sleep(wait + random.uniform(0, 0.5))
