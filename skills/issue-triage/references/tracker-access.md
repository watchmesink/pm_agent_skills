# Tracker Access

Use this reference only when fetching or normalizing issue data.

## Jira

Use `scripts/jira_issues.py` from this skill directory when Jira API access is available.

Supported environment variables:

- `JIRA_BASE_URL`: base URL such as `https://example.atlassian.net`
- `JIRA_EMAIL` plus `JIRA_API_TOKEN`: Jira Cloud basic auth
- `JIRA_BEARER_TOKEN`: bearer token for Jira instances that support it

Example prioritization fetch:

```bash
python3 scripts/jira_issues.py --top 100 --jql 'project = ABC AND resolution = Unresolved ORDER BY updated DESC' --json
```

Example duplicate search:

```bash
python3 scripts/jira_issues.py --top 50 --jql 'project = ABC AND resolution = Unresolved AND text ~ "important phrase" ORDER BY updated DESC' --json
```

Jira custom fields vary by instance. If affected customers, revenue, support tickets, or license counts are custom fields, inspect returned field names or ask the user for their field IDs.

## Generic Trackers

When no API helper exists, ask for an export or pasted issue list with as many normalized fields as possible:

```text
key, url, title, description, status, type, severity, priority, project, component, created, updated, votes, comments, support_tickets, affected_customers, paid_licenses, revenue, labels
```

If the tracker has an API, adapt the workflow but keep these invariants:

- Use API data rather than scraping when possible.
- Fetch more than the final requested top N.
- Search duplicate candidates in the same project first.
- Default to open issues unless the user asks to include resolved or closed issues.
