---
name: monitor-ai-coding-competitors
description: Monitor AI coding tools and adjacent prompt-to-app builders for official releases, product changes, strategic initiatives, pricing and availability moves, reliability problems, and observed Reddit/X/news signals. Use for a PM-focused digest of changes since the last successful run, a specified date range, or the previous week; preserve per-source checkpoints and cite every finding.
---

# Monitor AI Coding Competitors

Run a stateful, evidence-first market scan for the configured competitor families in [the competitor registry](references/competitors.json). The default audience is a Product Manager looking for neutral product patterns and feature inspiration. Keep factual observations, community signals, and interpretation visibly separate.

## Run the monitor

1. Read the source registry and the [source policy](references/source-policy.md).
2. Open a run window with `scripts/monitor_state.py window`. Use the first-run default of seven days; on later runs use each source's checkpoint with a 48-hour overlap. Explicit dates or a `--days` override take precedence.
3. Check every configured family’s official changelog, release notes, blog, documentation, repository releases, status page, and issue tracker when present. Prefer RSS/Atom/API surfaces, then paginated official HTML.
4. Search public web results for Reddit, X, forums, GitHub issues, and reputable news using the registry's aliases and disambiguators. Public social results are sampled, not exhaustive; do not scrape sites or automate logged-in pages.
5. When available, fan out research by category with subagents. Require each researcher to return normalized findings plus a coverage record. Continue sequentially if subagents are unavailable.
6. Normalize findings using [the report format](references/report-format.md). Record event date, publication date, lifecycle, confidence, product surface, source URLs, and whether the item is a new event or a material update. Preserve every distinct version/release published inside the selected window; never replace a family’s in-window history with only its latest item.
7. Canonicalize URLs and cluster mirrored coverage. Attach community reactions to the official event instead of creating duplicate events. Do not count cross-posts by one author as independent evidence.
8. Apply the community-problem threshold in the policy. Treat one concrete security, data-loss, destructive, unauthorized-spend, or account-lockout report as an anecdotal high-impact watch, not a confirmed trend.
9. Validate the findings and coverage artifacts with `scripts/validate_findings.py`. Render a Markdown report using the required sections below and a companion self-contained HTML dashboard when the workspace output is enabled.
10. In the rendered Markdown and HTML, hide families with no relevant finding or qualified signal; retain them only in the coverage ledger and structured run artifacts. Group all distinct in-window releases/events under their product, ordered by announcement date, with each version/date visible. Keep the HTML dashboard intentionally minimal: a compact header, search, and the dated product-update list only. Do not add top metrics, “most consequential moves,” pattern cards, community panels, strategy sections, or evidence-trail sections to the HTML unless the user explicitly requests them. Save the report, dashboard, and structured run artifacts under the workspace archive, then commit checkpoints with `scripts/monitor_state.py commit`. Never advance a blocked source or commit an unsuccessful run.

## Supported requests

- “Monitor the competitors” means since the last successful run; first use means the previous seven days.
- “Monitor the last N days” changes the window without changing the normal checkpoint rule.
- “Monitor from DATE to DATE” performs an explicit range. Historical ranges do not change live checkpoints unless the user explicitly requests a commit.
- Accept product/category filters and preview/no-commit requests.

## Evidence and wording rules

- Every product feature or release asserted as fact needs at least one first-party source.
- Mark claims as `confirmed`, `strongly_supported`, `community_signal`, or `anecdotal_watch`.
- Mark lifecycle separately: `announced`, `preview`, `rolling_out`, `ga`, `deprecated`, `retired`, `reported`, `acknowledged`, or `fixed`.
- Use publication or event time, not crawl time. Include late-indexed items only as late discoveries or material updates.
- Treat “no content found” as a coverage result, not a product-ledger item: keep the family in `coverage.json`, but omit it from rendered Markdown/HTML unless the user explicitly asks for a complete zero-result inventory.
- Do not collapse multiple versions from the same family into a single “latest update.” Deduplicate only exact mirrors or the same event; keep separate version releases and material updates visible within the window.
- Never write “all changes,” “no complaints,” or “the community thinks.” Say “changes surfaced,” “no relevant reports surfaced,” or “observed community signal.”
- English is the systematic search language. If a high-signal non-English item appears, preserve the original URL and provide a concise English translation with an explicit translation note.

## Report layout

Write a PM-oriented digest with:

1. Window, run time, and one-paragraph coverage caveat.
2. Most consequential moves, ranked by product impact and novelty.
3. Cross-competitor product patterns and neutral inspiration themes: user job, observed approach, evidence, and open product questions.
4. Product-by-product release and initiative ledger containing only families with at least one relevant release, initiative, lifecycle change, status event, or qualified community signal. Do not render empty “no relevant official change surfaced” rows in the user-facing digest or HTML. Preserve zero-result and partial/blocked checks in the machine-readable coverage ledger, and mention the omission once in the coverage caveat.
5. Community pain, reliability, status, and unmet-need signals with reporter/platform counts and confidence.
6. Pricing, model, availability, partnership, deprecation, and ownership changes.
7. Coverage ledger showing `covered`, `sampled`, `partial`, or `blocked` for every family and channel.
8. Evidence appendix containing all normalized surfaced findings and clickable sources.

## Runtime files

- Store private checkpoints at `~/.cache/codex/monitor-ai-coding-competitors/state.json` (override with `MONITOR_AI_CODING_STATE`).
- Store reports under the workspace’s `competitor-intelligence/reports/` directory (or the configured workspace archive directory).
- Store the companion dashboard at the workspace’s `competitor-intelligence/index.html` (or a run-specific `.html` beside the report when requested).
- Store per-run `findings.jsonl`, `coverage.json`, and `run.json` beside the report under `competitor-intelligence/runs/`.
- Keep metadata, short paraphrases, IDs, timestamps, and links; do not archive a raw Reddit/X corpus.

## Checkpoint semantics

Keep one checkpoint per `competitor × channel`, plus cross-product Reddit/X searches. A completed accessible query, including zero results, advances its channel. A login wall, robots block, unavailable page, or skipped query leaves that channel unchanged and marks it `blocked` or `partial`. Successful report creation is the commit boundary. Use an overlap to catch delayed indexing, then suppress unchanged events by canonical URL, platform ID, or event fingerprint.
