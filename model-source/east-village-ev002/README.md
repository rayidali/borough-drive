# EV-002 evidence

Read [the session report](../EAST-VILLAGE-EV002.md) and [current handoff](../../CODEX-HANDOFF.md) for final state. This directory contains local browser tests using unchanged revision-09 building assets; it is not new photographic research or production acceptance.

- `baseline.json`: frozen checkout, original package/source/model/private-image hashes and intended change scope.
- `control/`: original package, five cold/five warm startup samples, ten round trips and matched views. The ignored scratch player can be recreated from baseline `a2a90a3`; evidence does not depend on a running server.
- `candidate/`: timed 16-slot-opening candidate startup/travel and final repaired candidate's recovery/visual checks. Every browser report embeds its own build. Do not relabel the timed `c8df3784…` results as the retry-repaired `fa4d32a0…` package.
- `startup-comparison.json`, `journey-comparison.json`: paired gates and normalized memory comparisons, including the two isolated 100 ms non-loading gaps.
- `trial-01/`, `trial-02/`, `trial-04/`, `trial-05/`, `recovery-trial-02/` and `candidate/failures-trial-*.json`: unsuccessful/diagnostic trials retained with actual outcomes. [Progress](progress.json) distinguishes implementation defects from harness assertions and injected network errors.
- `preservation.json`: unchanged 203 authored GLBs and 203 compiled scenes; final-vs-timed source difference; protected original/UI/audio/handling files and private images.
- `visual-review.json`: all 27 paired views / 54 images inspected, including Tile Bar’s First Avenue entrance; preservation findings and hashes. Additional settings/camera diagnostic images are not included in that count.
- `camera/`, `address/`, `settings/` and `candidate/camera-hold.json`: final-pack control, address, settings/focus/resize/recovery and delayed-wide-orbit evidence.
- `validation.json`, `seventh-verify.txt`, `original-verify.txt`: final structural, documentation and preservation validation.
- `local-routes.json`: exact localhost root, Seventh, legacy and manifest comparisons, not a live-site check.

Use the existing review profile on port 9222 and `npm run dev`. The harness creates/closes its own tab. Example:

```sh
node scripts/review-seventh-streaming.mjs renders/ev002/startups startups
node scripts/review-seventh-streaming.mjs renders/ev002/journey journey
node scripts/review-seventh-streaming.mjs renders/ev002/recovery failures
node scripts/review-seventh-streaming.mjs renders/ev002/views views
node scripts/review-seventh-streaming.mjs renders/ev002/details details
node scripts/review-seventh-streaming.mjs renders/ev002/entry tilebar-entry
node scripts/review-seventh-streaming.mjs renders/ev002/camera-delay camera-hold
```

`BOROUGH_REVIEW_URL` selects a separately served control; `BOROUGH_REVIEW_BUILD` must select its matching `build.json`. `BOROUGH_REVIEW_FAULTS` optionally narrows the comma-separated fault cases during diagnosis. The default runs missing-file, corrupted-body and offline cases plus retry during delay, pause/focus and cancellation/backtracking. Injected responses never alter asset files. Real driving uses normal keys; review pose commands only place the car before a route/reset scenario.

Do not render another game or rebuild during timed startup/travel. Cold means browser network cache disabled, not reset OS/shader/WASM caches. Local warm runs still transferred bodies under the local server's revalidation policy. Renderer memory/resource counts measure live resources, not total process memory or reserved WASM capacity. All 203 scenes still open initially; 191 remain pinned throughout this bounded proof. Broader grouping, deployment/cache behavior and old-release compatibility belong to EV-003.
