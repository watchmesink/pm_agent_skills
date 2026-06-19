---
name: issue-triage
description: Prioritize, triage, and deduplicate issues across Jira and generic issue trackers using a separate Markdown strategy document. Use when Codex needs to fetch or analyze tracker issues, rank the most important open or recent tickets on demand, compare new or recent issues against existing open issues in the same project, report likely duplicates, or prepare issue tracker actions based on product strategy, votes, comments, severity, affected customers, paid licenses or revenue, support tickets, and recency.
---

# Issue Triage

## Overview

Use this skill to turn tracker data into a strategy-aware issue ranking and duplicate report. It supports Jira and other trackers through APIs, local helper scripts, pasted issue lists, or exported issue data.

## Core Rules

- Use `strategy.md` in the current project root as the default strategy document unless the user gives another path.
- If the project-root strategy document is missing, blank, or still marked `Status: UNFILLED`, interview the user before ranking issues. Collect at least: investment areas, non-investment areas, high-priority signals, and low-priority signals. Update the strategy document before continuing unless the user explicitly says to proceed without it.
- Fetch live tracker data through APIs when possible. Do not scrape tracker web UI unless the API cannot represent the needed view.
- For Jira, use `scripts/jira_issues.py` when a Jira API is available. Provide credentials through environment variables or the agent runtime's secret-injection mechanism. Do not inline, print, or store credentials.
- Default to read-only behavior. Report duplicate candidates and recommended actions, but do not comment, link, transition, merge, reprioritize, or otherwise update tracker issues unless the user explicitly asks and confirms the specific mutation.
- Keep conclusions grounded in returned fields. Mark uncertain duplicate matches and strategic inferences clearly.
- For support-triage runs, exclude issues already marked as triaged, deferred, parked, or intentionally waiting unless the user explicitly asks to include them.
- For support-triage prioritization, treat issues created within the last 14 days as the primary priority bucket. Rank recent issues before older issues, then order within the recent bucket by strategic fit, severity, support/customer evidence, paid-license or revenue impact, votes/comments, and duplicate/cluster signal. Call out older high-impact issues separately only when their evidence clearly outweighs normal recency.

## Workflow

1. Clarify the target: tracker, project or query, requested number of prioritized issues, and whether the user wants prioritization, duplicate detection, or both.
2. Read the strategy document. If it is unfilled, run the strategy interview and update it first.
3. Fetch candidate issues:
   - Prioritization: fetch open and recent issues from the target project. Pull more than the requested top N so judgment is not limited to the first page returned by the tracker.
   - Duplicate detection: for new or recent issues, search existing open issues in the same project. Use title keywords, exact error messages, components/subsystems, affected versions, stack traces, and customer wording where available.
   - When reusing saved tracker filters, apply any additional user or strategy tag exclusions after fetching if the saved query cannot express them exactly.
   - For support-triage prioritization, compute the 14-day recent cutoff from the run date and annotate whether each candidate is inside or outside that window.
4. Normalize issue fields before judging: key, URL, title, description excerpt, status, type, severity or priority, project, component/subsystem, assignee, created/updated dates, votes, comments, support tickets, affected customers, paid licenses or revenue, affected versions, labels/tags, and source tracker.
5. Prioritize with the applicable support-triage recency bucket first, then strategy fit and evidence. Consider investment areas, non-investment areas, customer impact, severity, regressions, security/privacy risk, affected customers, paid licenses or revenue, support tickets, votes, comments, recency, and blocked work. A numeric score is optional; the ranking must include plain-language rationale either way.
6. Detect duplicates conservatively. Prefer likely shared root cause over superficial keyword overlap. Compare repro steps, error text, environment, affected versions, subsystem/component, user goal, and existing discussion. Classify confidence as `High`, `Medium`, or `Low`.
7. Report data limits: query used, tracker scope, number of issues fetched, whether closed issues were excluded, and any fields unavailable from the API.

## Strategy Interview

Ask concise questions, then write the answers into the project-root `strategy.md`.

Required questions:

- Which product areas, customer segments, workflows, or technical themes are we actively investing in?
- Which areas are explicitly not investment priorities right now?
- What makes an issue high priority even if votes are low?
- What makes an issue low priority even if votes or comments are high?
- Which customer, revenue, paid-license, affected-customer, or support-ticket signals should strongly influence ranking?

Optional questions when useful:

- Are there severity definitions, escalation rules, regulatory or security risks, or known must-fix classes?
- Are there current product bets, launches, deprecations, or blocked internal teams that should change prioritization?
- Are there examples of issues that were ranked well or poorly in the past?

If the user gives partial answers, write the known parts and leave explicit `Unknown` entries instead of inventing strategy.

## Output Shape

For prioritization, return a compact table or list with:

- Rank
- Issue key and link
- Title
- Why it matters now
- Evidence: severity, votes, comments, support tickets, affected customers, licenses/revenue, recency, strategic fit
- Caveat or suggested next action

For duplicate detection, return:

- New or recent issue
- Existing possible duplicate
- Confidence
- Shared evidence
- Important differences
- Recommendation, report-only by default

## Resources

- Read `references/tracker-access.md` for Jira and generic tracker command patterns.
- Read or update the project-root `strategy.md` whenever strategy-guided ranking is requested.
- Use `scripts/jira_issues.py` for Jira searches when a Jira API is available.
