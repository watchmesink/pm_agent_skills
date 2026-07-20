# Source policy

## Source order

1. First-party changelogs, release notes, documentation, repository releases, status pages, and official announcements.
2. Maintainer/employee statements and official community forums.
3. Reputable news reporting that adds product or strategic context.

For date-indexed first-party archives, inspect the year/date path implied by the run window before relying on the archive landing page. For example, Warp publishes its release archive under `https://docs.warp.dev/changelog/YYYY/`; use the release page’s displayed date as the announcement date and retain the canonical per-release URL when available.
4. Public Reddit and X pages discovered through web search.

Use the highest available source tier for factual claims. Search snippets are leads only until the underlying page is accessible. Preserve the URL, platform/post ID when available, author, publication time, and access status.

## Window and dates

- Use UTC for checkpoints and display dates in the user's Europe/Berlin timezone.
- Treat intervals as start-inclusive and end-exclusive.
- First run: seven days. Later runs: each source's `covered_through` minus 48 hours.
- Explicit dates override the default window. Historical runs do not advance live state by default.
- Prefer event/publication time to crawl time. Keep `event_at`, `published_at`, and `observed_at` distinct.
- On a successful run, rescan 30 days of official sources when the last official rescan is older than 30 days. Cap community backfills at 30 days and disclose older gaps.

## Confidence and lifecycle

- `confirmed`: first-party changelog, release, documentation, repository, status, or official account.
- `strongly_supported`: maintainer/employee statement plus corroboration, or two independent reputable sources.
- `community_signal`: independent user reports meeting the problem threshold.
- `anecdotal_watch`: one credible, concrete report; never present as representative.

Keep lifecycle separate: `announced`, `preview`, `rolling_out`, `ga`, `deprecated`, `retired`, `reported`, `acknowledged`, `fixed`.

## Community sampling

- Run product-alias and dedicated-community searches for every family; also run cross-product searches for switching, comparisons, pricing, outages, and regressions.
- Inspect up to five recent and three high-engagement surfaced Reddit threads per family, with comment review for up to three problem-heavy threads.
- Inspect official X handles plus up to ten relevant surfaced community posts per family, excluding reposts when possible.
- Label successful Reddit/X passes `sampled`, never `complete`. A public-web pass cannot establish “no complaints.”
- Do not scrape Reddit, X, or logged-in websites. Do not rely on unauthenticated Reddit JSON/RSS or browser automation.

Put a problem in the main digest only when one of these holds:

- An official source acknowledges it.
- Three distinct first-person reporters describe the same product/version/symptom across two threads, with concrete detail.
- Two independent reporters describe it on two different platforms.
- One concrete report concerns security, data loss, destructive behavior, unauthorized spend, or account lockout; mark it as high-impact anecdotal watch.

Do not count copied text, reposts, employee posts, affiliate promotion, or vague “same here” comments as independent evidence.

## Deduplication

- Remove tracking parameters, fragments, mobile-host variants, and redirect noise from URLs.
- Deduplicate exact URLs and platform IDs.
- Cluster the same family, surface, version/feature/symptom, and 72-hour publication neighborhood into one event.
- Attach changelog/blog/news/social items as evidence on the same event.
- Re-report an existing event only for a material lifecycle, scope, pricing, or availability transition.
- Normalize renamed products into one family and retain aliases for search.

## Coverage language

Use `covered`, `sampled`, `partial`, or `blocked` per channel. Say “changes surfaced” and “no relevant reports surfaced,” never “all changes,” “no complaints,” or “the community thinks.”
