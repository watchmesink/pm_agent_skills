# Finding and report format

## Finding JSONL schema

Each line is one normalized event:

```json
{
  "event_id": "stable-fingerprint",
  "family_id": "cursor",
  "surface": "desktop|cli|cloud|ide|api|model|enterprise|community",
  "category": "feature|initiative|model|pricing|availability|integration|reliability|security|deprecation|ownership|news",
  "title": "Short factual title",
  "summary": "Cited paraphrase of what changed or was observed.",
  "pm_pattern": "Neutral user job or product pattern this may inspire.",
  "event_at": "2026-07-18T00:00:00Z",
  "published_at": "2026-07-18T00:00:00Z",
  "observed_at": "2026-07-20T00:00:00Z",
  "lifecycle": "ga",
  "confidence": "confirmed",
  "impact": 1,
  "novelty": 1,
  "update_of": null,
  "community": {"reporters": 0, "threads": 0, "platforms": [], "sentiment": "mixed"},
  "sources": [{"url":"https://example.com/source","kind":"official","title":"Source title","published_at":"2026-07-18T00:00:00Z"}]
}
```

Required fields are `event_id`, `family_id`, `category`, `title`, `summary`, `event_at` or `published_at`, `lifecycle`, `confidence`, and at least one HTTP(S) source. Keep scores directional and explain ranking in the report.

## Coverage JSON

```json
{
  "family_id": "cursor",
  "channels": {
    "official": {"status":"covered","attempted_at":"...","covered_through":"...","items":3},
    "reddit": {"status":"sampled","attempted_at":"...","covered_through":"...","items":2},
    "x": {"status":"partial","attempted_at":"...","error":"public results unavailable"}
  }
}
```

## Markdown report

Use these sections in order: window and coverage caveat; consequential moves; cross-competitor patterns; product ledger; community pain and reliability; strategy/pricing/lifecycle; coverage ledger; evidence appendix. The rendered product ledger must include only families with at least one relevant finding or qualified signal. Group every distinct in-window version/event beneath its family, ordered by announcement date; do not show only the latest release. Keep no-result families in the machine-readable coverage ledger, not as empty user-facing rows.

When an HTML dashboard is requested or enabled, keep it self-contained, link back to the Markdown report and run artifacts, and apply the same omission rule: no-content families stay out of the visible product ledger while remaining represented in coverage metadata.

The default HTML view is intentionally a product-update reader: compact header, search field, and one grouped list per family. Each update block shows its announcement date, all factual bullets captured for that event, and a direct source link. Do not render the Markdown report’s analytical sections in the default HTML view.
