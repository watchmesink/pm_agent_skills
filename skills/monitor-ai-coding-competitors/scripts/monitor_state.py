#!/usr/bin/env python3
"""Checkpoint helper for monitor-ai-coding-competitors.

The monitor itself researches through Codex web tools. This script provides a
small, deterministic, atomic state boundary around those runs.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import tempfile
from pathlib import Path
from typing import Any


DEFAULT_STATE = "~/.cache/codex/monitor-ai-coding-competitors/state.json"
SCHEMA_VERSION = 1


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def parse_time(value: str) -> dt.datetime:
    value = value.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc).replace(microsecond=0)


def iso(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def state_path(raw: str | None) -> Path:
    return Path(raw or os.environ.get("MONITOR_AI_CODING_STATE", DEFAULT_STATE)).expanduser()


def default_state() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "created_at": iso(utc_now()),
        "last_successful_run_at": None,
        "last_official_rescan_at": None,
        "sources": {},
        "events": {},
    }


def load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return default_state()
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"unsupported state file: {path}")
    data.setdefault("sources", {})
    data.setdefault("events", {})
    return data


def atomic_write(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, prefix=".state-", suffix=".tmp", delete=False)
    temp = Path(handle.name)
    try:
        with handle:
            json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def command_window(args: argparse.Namespace) -> None:
    path = state_path(args.state_path)
    state = load(path)
    end = parse_time(args.until) if args.until else (parse_time(args.now) if args.now else utc_now())
    if args.since:
        start = parse_time(args.since)
        source_windows = {}
    elif state["sources"] and not args.reset_window:
        source_windows = {}
        overlap = dt.timedelta(hours=args.overlap_hours)
        for source_id, row in sorted(state["sources"].items()):
            checkpoint = row.get("covered_through")
            if checkpoint:
                source_windows[source_id] = {"start": iso(parse_time(checkpoint) - overlap), "end": iso(end)}
        start = end - dt.timedelta(days=args.days)
    else:
        start = end - dt.timedelta(days=args.days)
        source_windows = {}
    result = {
        "state_path": str(path),
        "first_run": not bool(state["sources"]),
        "start": iso(start),
        "end": iso(end),
        "overlap_hours": args.overlap_hours,
        "source_windows": source_windows,
        "historical": end < utc_now() - dt.timedelta(hours=24),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


def command_status(args: argparse.Namespace) -> None:
    path = state_path(args.state_path)
    print(json.dumps({"state_path": str(path), "state": load(path)}, indent=2, sort_keys=True))


def command_commit(args: argparse.Namespace) -> None:
    manifest_path = Path(args.manifest).expanduser()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("success") is not True:
        raise SystemExit("refusing to commit an unsuccessful run")
    if manifest.get("historical") and not manifest.get("commit_historical", False):
        print(json.dumps({"committed": False, "reason": "historical run"}, indent=2))
        return
    path = state_path(args.state_path)
    state = load(path)
    completed_at = parse_time(manifest.get("completed_at") or iso(utc_now()))
    state["last_successful_run_at"] = iso(completed_at)
    if manifest.get("official_rescan"):
        state["last_official_rescan_at"] = iso(completed_at)
    for source_id, update in (manifest.get("sources") or {}).items():
        existing = state["sources"].get(source_id, {})
        merged = {**existing, **update, "last_attempted_at": update.get("last_attempted_at", iso(completed_at))}
        if update.get("status") in {"blocked", "partial"} and not update.get("covered_through"):
            merged["covered_through"] = existing.get("covered_through")
        state["sources"][source_id] = merged
    for event_id, event in (manifest.get("events") or {}).items():
        state["events"][event_id] = event
    atomic_write(path, state)
    print(json.dumps({"committed": True, "state_path": str(path), "completed_at": iso(completed_at)}, indent=2))


def command_self_test(_: argparse.Namespace) -> None:
    with tempfile.TemporaryDirectory(prefix="monitor-state-") as directory:
        path = Path(directory) / "state.json"
        state = load(path)
        assert not state["sources"]
        first_end = parse_time("2026-07-20T12:00:00Z")
        first_start = first_end - dt.timedelta(days=7)
        manifest = {"success": True, "completed_at": iso(first_end), "sources": {"cursor:official": {"status": "covered", "covered_through": iso(first_end)}}}
        manifest_path = Path(directory) / "manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        args = argparse.Namespace(manifest=str(manifest_path), state_path=str(path))
        command_commit(args)
        updated = load(path)
        assert updated["last_successful_run_at"] == iso(first_end)
        assert updated["sources"]["cursor:official"]["covered_through"] == iso(first_end)
        assert first_start < first_end
        print(json.dumps({"ok": True, "checks": ["first_run", "atomic_commit", "source_checkpoint"]}, indent=2))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--state-path")
    sub = root.add_subparsers(dest="command", required=True)
    window = sub.add_parser("window")
    window.add_argument("--now")
    window.add_argument("--since")
    window.add_argument("--until")
    window.add_argument("--days", type=int, default=7)
    window.add_argument("--overlap-hours", type=int, default=48)
    window.add_argument("--reset-window", action="store_true")
    window.set_defaults(func=command_window)
    status = sub.add_parser("status")
    status.set_defaults(func=command_status)
    commit = sub.add_parser("commit")
    commit.add_argument("--manifest", required=True)
    commit.set_defaults(func=command_commit)
    test = sub.add_parser("self-test")
    test.set_defaults(func=command_self_test)
    return root


if __name__ == "__main__":
    arguments = parser().parse_args()
    arguments.func(arguments)
