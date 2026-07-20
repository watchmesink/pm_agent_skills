#!/usr/bin/env python3
"""Validate normalized findings and coverage artifacts before checkpoint commit."""

from __future__ import annotations

import argparse
import json
import tempfile
import datetime as dt
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


REQUIRED = {"event_id", "family_id", "category", "title", "summary", "lifecycle", "confidence", "sources"}
ALLOWED_CONFIDENCE = {"confirmed", "strongly_supported", "community_signal", "anecdotal_watch"}
ALLOWED_STATUS = {"covered", "sampled", "partial", "blocked"}


def canonical_url(raw: str) -> str:
    parts = urlsplit(raw.strip())
    query = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True) if not key.lower().startswith(("utm_", "ref", "source"))]
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), urlencode(query), ""))


def valid_timestamp(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def validate_findings(path: Path) -> dict[str, object]:
    errors: list[str] = []
    ids: set[str] = set()
    urls: set[str] = set()
    count = 0
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        count += 1
        try:
            item = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_no}: invalid JSON ({exc.msg})")
            continue
        missing = REQUIRED - set(item)
        if missing:
            errors.append(f"line {line_no}: missing {sorted(missing)}")
        event_id = item.get("event_id")
        if not isinstance(event_id, str) or not event_id:
            errors.append(f"line {line_no}: event_id must be non-empty")
        elif event_id in ids:
            errors.append(f"line {line_no}: duplicate event_id {event_id}")
        else:
            ids.add(event_id)
        if item.get("confidence") not in ALLOWED_CONFIDENCE:
            errors.append(f"line {line_no}: invalid confidence")
        if not valid_timestamp(item.get("event_at")) and not valid_timestamp(item.get("published_at")):
            errors.append(f"line {line_no}: event_at or published_at must be an ISO timestamp")
        sources = item.get("sources")
        if not isinstance(sources, list) or not sources:
            errors.append(f"line {line_no}: sources must be a non-empty list")
        else:
            for source in sources:
                url = source.get("url") if isinstance(source, dict) else None
                if not isinstance(url, str) or not url.startswith(("http://", "https://")):
                    errors.append(f"line {line_no}: source URL must be HTTP(S)")
                elif canonical_url(url) in urls:
                    continue
                else:
                    urls.add(canonical_url(url))
    return {"count": count, "errors": errors, "ok": not errors}


def validate_coverage(path: Path) -> dict[str, object]:
    errors: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data if isinstance(data, list) else data.get("coverage", [])
    if not isinstance(rows, list):
        return {"count": 0, "errors": ["coverage must be a list or an object with coverage"], "ok": False}
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict) or not row.get("family_id"):
            errors.append(f"coverage row {index}: family_id is required")
            continue
        channels = row.get("channels", {})
        for channel, details in channels.items():
            if details.get("status") not in ALLOWED_STATUS:
                errors.append(f"coverage row {index} channel {channel}: invalid status")
    return {"count": len(rows), "errors": errors, "ok": not errors}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("findings", type=Path, nargs="?")
    parser.add_argument("--coverage", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        with tempfile.TemporaryDirectory(prefix="monitor-validator-") as directory:
            root = Path(directory)
            finding = {
                "event_id": "fixture-event",
                "family_id": "cursor",
                "category": "feature",
                "title": "Fixture feature",
                "summary": "A test finding.",
                "event_at": "2026-07-20T00:00:00Z",
                "lifecycle": "ga",
                "confidence": "confirmed",
                "sources": [{"url": "https://example.com/release?utm_source=test"}],
            }
            findings_path = root / "findings.jsonl"
            findings_path.write_text(json.dumps(finding) + "\n", encoding="utf-8")
            coverage_path = root / "coverage.json"
            coverage_path.write_text(json.dumps([{"family_id": "cursor", "channels": {"official": {"status": "covered"}}}]), encoding="utf-8")
            result = {"findings": validate_findings(findings_path), "coverage": validate_coverage(coverage_path)}
            assert result["findings"]["ok"] and result["coverage"]["ok"]
            print(json.dumps({"ok": True, "checks": ["finding_schema", "source_url", "coverage_status", "url_normalization"]}, indent=2))
        return
    if not args.findings:
        parser.error("findings is required unless --self-test is used")
    result = {"findings": validate_findings(args.findings)}
    if args.coverage:
        result["coverage"] = validate_coverage(args.coverage)
    result["ok"] = all(section["ok"] for section in result.values())
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
