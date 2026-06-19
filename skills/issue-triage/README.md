# Issue Triage

`issue-triage` is a product-management skill for ranking tracker issues and finding likely duplicates through a strategy document.

## How It Behaves

- Reads `strategy.md` from the current project root by default.
- Interviews the user and updates `strategy.md` if the strategy is missing, blank, or marked `Status: UNFILLED`.
- Fetches issues from Jira, generic tracker APIs, exports, or pasted issue lists.
- Prioritizes recent support-triage issues first, then weighs strategy fit, severity, customer evidence, business impact, votes, comments, and duplicate/cluster signals.
- Finds duplicates conservatively by comparing the likely root cause, repro details, error text, environment, subsystem, affected versions, and user goal.
- Defaults to read-only behavior. It reports recommended actions but does not mutate tracker issues unless the user explicitly asks and confirms.

## Strategy Document

Create a `strategy.md` file in the project root, or let the skill interview you and create one. A useful strategy covers:

- Investment areas.
- Non-investment areas.
- High-priority signals.
- Low-priority signals.
- Customer, revenue, paid-license, affected-customer, or support-ticket signals that should influence ranking.

## Usage

Ask Codex to use `$issue-triage` when you want to prioritize open issues, triage recent support reports, or compare new issues against existing open issues.

Example prompts:

- `Use $issue-triage to rank the top 10 open issues in project ABC.`
- `Use $issue-triage to find likely duplicates for these new issue reports.`
- `Use $issue-triage with this CSV export and our strategy.md.`
