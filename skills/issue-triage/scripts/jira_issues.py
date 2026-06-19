#!/usr/bin/env python3
"""Fetch Jira issues for issue triage."""

from __future__ import annotations

import argparse
import base64
import json
import os
import urllib.error
import urllib.request


DEFAULT_FIELDS = (
    "summary,status,priority,issuetype,assignee,reporter,created,updated,"
    "description,comment,votes,watches,components,labels,fixVersions,versions"
)


def env_required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing {name}. Configure it in the environment or secret store.")
    return value


def auth_header() -> str:
    bearer = os.environ.get("JIRA_BEARER_TOKEN")
    if bearer:
        return f"Bearer {bearer}"

    email = os.environ.get("JIRA_EMAIL")
    token = os.environ.get("JIRA_API_TOKEN")
    if email and token:
        raw = f"{email}:{token}".encode("utf-8")
        return "Basic " + base64.b64encode(raw).decode("ascii")

    raise SystemExit(
        "Missing Jira credentials. Set JIRA_BEARER_TOKEN or JIRA_EMAIL plus JIRA_API_TOKEN."
    )


def request_json(url: str, payload: dict[str, object], authorization: str) -> object:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": authorization,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "codex-issue-triage-skill",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def search_page(
    base_url: str,
    api_path: str,
    authorization: str,
    jql: str,
    fields: list[str],
    start_at: int,
    max_results: int,
) -> dict[str, object]:
    url = base_url.rstrip("/") + api_path
    payload: dict[str, object] = {
        "jql": jql,
        "startAt": start_at,
        "maxResults": max_results,
        "fields": fields,
    }
    data = request_json(url, payload, authorization)
    if not isinstance(data, dict):
        raise SystemExit(f"Jira returned unexpected response: {data!r}")
    return data


def fetch_issues(
    base_url: str,
    jql: str,
    fields: list[str],
    top: int,
    page_size: int,
    api_paths: list[str],
) -> list[dict[str, object]]:
    authorization = auth_header()
    issues: list[dict[str, object]] = []
    start_at = 0
    last_error: str | None = None
    api_path_index = 0

    while len(issues) < top:
        page_top = min(page_size, top - len(issues))
        api_path = api_paths[api_path_index]
        try:
            page = search_page(base_url, api_path, authorization, jql, fields, start_at, page_top)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            last_error = f"Jira HTTP {exc.code} from {api_path}: {body[:1000]}"
            if exc.code in {404, 410} and api_path_index + 1 < len(api_paths):
                api_path_index += 1
                start_at = 0
                issues = []
                continue
            raise SystemExit(last_error) from exc
        except urllib.error.URLError as exc:
            raise SystemExit(f"Jira request failed: {exc}") from exc

        page_issues = page.get("issues", [])
        if not isinstance(page_issues, list):
            raise SystemExit(f"Jira response did not include an issues list: {page!r}")
        issues.extend([issue for issue in page_issues if isinstance(issue, dict)])

        if not page_issues:
            break

        total = page.get("total")
        if isinstance(total, int) and start_at + len(page_issues) >= total:
            break
        if len(page_issues) < page_top:
            break

        start_at += len(page_issues)

    if not issues and last_error:
        raise SystemExit(last_error)
    return issues[:top]


def issue_title(issue: dict[str, object]) -> str:
    key = issue.get("key") or issue.get("id") or "(unknown)"
    fields = issue.get("fields")
    summary = "(no summary)"
    if isinstance(fields, dict):
        summary = str(fields.get("summary") or summary)
    return f"{key}\t{summary}"


def parse_fields(value: str) -> list[str]:
    return [field.strip() for field in value.split(",") if field.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=os.environ.get("JIRA_BASE_URL"))
    parser.add_argument("--jql", required=True, help="Jira JQL query")
    parser.add_argument("--fields", default=DEFAULT_FIELDS)
    parser.add_argument("--top", type=int, default=50)
    parser.add_argument("--page-size", type=int, default=50)
    parser.add_argument("--api-path", action="append", help="Override Jira search API path")
    parser.add_argument("--json", action="store_true", help="Print raw JSON")
    args = parser.parse_args()

    base_url = args.base_url or env_required("JIRA_BASE_URL")
    api_paths = args.api_path or ["/rest/api/3/search", "/rest/api/2/search"]
    issues = fetch_issues(
        base_url=base_url,
        jql=args.jql,
        fields=parse_fields(args.fields),
        top=args.top,
        page_size=min(max(args.page_size, 1), 100),
        api_paths=api_paths,
    )

    if args.json:
        print(json.dumps(issues, ensure_ascii=False, indent=2))
        return 0

    for issue in issues:
        print(issue_title(issue))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
