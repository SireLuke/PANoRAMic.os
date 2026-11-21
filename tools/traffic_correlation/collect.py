#!/usr/bin/env python3
"""Collect and correlate GitHub repository traffic with development activity.

Traffic endpoints are owner/collaborator-only. Missing permission is recorded as
an unavailable source; it is never replaced with guessed or inferred values.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

API = "https://api.github.com"
REPO = os.environ["GITHUB_REPOSITORY"]
TOKEN = os.environ["GITHUB_TOKEN"]
TRAFFIC_TOKEN = os.environ.get("TRAFFIC_TOKEN") or TOKEN
NOW = dt.datetime.now(dt.timezone.utc)
SINCE = NOW - dt.timedelta(days=14)
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "PAN-traffic-correlation-audit",
}


def get(path: str, traffic: bool = False):
    headers = dict(HEADERS)
    if traffic:
        headers["Authorization"] = f"Bearer {TRAFFIC_TOKEN}"
    req = urllib.request.Request(API + path, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read()), None
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:1000]
        return None, {"status": exc.code, "message": detail}
    except Exception as exc:  # network failures should be visible in the artifact
        return None, {"status": None, "message": str(exc)}


def collect(name: str, path: str, list_key: str | None = None, traffic: bool = False):
    data, error = get(path, traffic=traffic)
    if error:
        return {"available": False, "error": error, "data": None}
    if list_key:
        data = data.get(list_key, [])
    return {"available": True, "error": None, "data": data}


def day_key(value: str) -> str:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()


def main():
    since = SINCE.isoformat().replace("+00:00", "Z")
    encoded_since = urllib.parse.quote(since)
    base = f"/repos/{REPO}"
    sources = {
        "clones": collect("clones", base + "/traffic/clones", traffic=True),
        "views": collect("views", base + "/traffic/views", traffic=True),
        "commits": collect("commits", base + f"/commits?since={encoded_since}&per_page=100", None),
        "pull_requests": collect("pull_requests", base + "/pulls?state=all&sort=updated&direction=desc&per_page=100", None),
        "workflow_runs": collect("workflow_runs", base + f"/actions/runs?created=%3E%3D{encoded_since}&per_page=100", "workflow_runs"),
    }

    daily = defaultdict(lambda: {"clones": 0, "views": 0, "commits": 0,
                                 "pull_requests_updated": 0, "workflow_runs": 0})
    for metric in ("clones", "views"):
        source = sources[metric]
        if source["available"]:
            for row in source["data"].get("clones" if metric == "clones" else "views", []):
                daily[day_key(row["timestamp"])][metric] = row.get("count", 0)

    if sources["commits"]["available"]:
        for row in sources["commits"]["data"]:
            date = row.get("commit", {}).get("committer", {}).get("date")
            if date:
                daily[day_key(date)]["commits"] += 1

    if sources["pull_requests"]["available"]:
        for row in sources["pull_requests"]["data"]:
            date = row.get("updated_at")
            if date and dt.datetime.fromisoformat(date.replace("Z", "+00:00")) >= SINCE:
                daily[day_key(date)]["pull_requests_updated"] += 1

    if sources["workflow_runs"]["available"]:
        for row in sources["workflow_runs"]["data"]:
            date = row.get("created_at")
            if date:
                daily[day_key(date)]["workflow_runs"] += 1

    dates = sorted(daily)
    output = {
        "schema": "pan.github_traffic_correlation.v1",
        "repository": REPO,
        "generated_at": NOW.isoformat(),
        "window_days": 14,
        "interpretation": {
            "clones_are_not_people": True,
            "unique_cloners_are_not_verified_humans": True,
            "correlation_is_not_causation": True,
            "traffic_requires_repository_owner_or_collaborator_access": True,
        },
        "sources": sources,
        "daily_correlation": [{"date": date, **daily[date]} for date in dates],
    }
    out = Path(os.environ.get("OUTPUT_FILE", "traffic-correlation.json"))
    out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {out}; source availability: " +
          ", ".join(f"{k}={v['available']}" for k, v in sources.items()))
    # Fail only when every source is unavailable; partial data remains useful.
    if not any(v["available"] for v in sources.values()):
        print("No source data available; inspect recorded API errors.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
