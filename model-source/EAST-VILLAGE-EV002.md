# EV-002 — bounded browser loading proof

**October 12, 2026 — complete locally; uncommitted.** The user's “go ahead” after [EV-001](EAST-VILLAGE-EV001.md) authorized this existing-asset implementation and review. No new street/facade authoring, EV-003 integration, paid work or publication is included. [Current handoff](../CODEX-HANDOFF.md) · [baseline and allowlist](east-village-ev002/baseline.json) · [progress and unsuccessful trials](east-village-ev002/progress.json).

The player now uses a shared PCK and 203 separately fetched compiled building scenes. The 12 existing west-context buildings can unload together with their collision bodies and reload before they are needed. The other 191 remain resident for this proof. This is the bounded package/lifecycle test from the plan, not a neighborhood-wide streaming conversion.

## Implementation

- [Area export](../engine/first-seventh/scripts/export_areas.gd) copies the existing Godot 4.7.2 compiled `.scn` bytes and computes full transformed visual bounds. Every file has a SHA256 URL and explicit building/area ownership. The same manifest is embedded in the base pack and published alongside the external assets; the build manifest binds both hashes. Model/texture/observation recipes are unchanged.
- [Area loader](../engine/first-seventh/scripts/area_streamer.gd) bounds requests and staging, validates every response's length and SHA256, creates and deletes its own volatile cache files, and rejects stale callbacks using request tokens. Failed requests retry up to three times; the existing reset control retries failed assets. The camera/current area remain usable while a new area is prepared; movement or a requested view waits before exposing missing geometry.
- [World ownership](../engine/first-seventh/scripts/world.gd) stages each unchanged model and its footprint collision under one identity-transform parent. Activation inserts both together; retirement removes both and their strong references. Existing shared materials, streets, props, basement envelopes and batching are built once.
- [Readiness hooks](../engine/first-seventh/scripts/main.gd) cover startup, reset/review relocation and telemetry. The [camera hook](../engine/first-seventh/scripts/cameras.gd) tests the proposed view before rendering and retains the last complete pose when necessary. Lens/range/handling and existing camera gestures are preserved.
- [Exporter](../scripts/export-seventh.mjs) excludes building payload from the base pack, stages and verifies all outputs, copies only its owned file set, and removes obsolete files listed by the prior manifest. Its ignored staging directory now has a `.gdignore` marker. [Verification](../scripts/verify-seventh.mjs) checks the embedded/external manifest, every asset hash, exact 12/191 ownership, visual bounds, absence of duplicated packed building payload and stale area files, and the existing geographic/architectural invariants.

The 445 m retain / 475 m eviction thresholds use full model bounds and a three-second dwell. Actual frustum intersection takes priority: a camera far plane is measured along its viewing axis, so a circular distance threshold alone cannot protect wider off-axis views. The hook uses the real frustum's outward planes and a margin, without shortening the camera range. [Godot camera semantics](https://docs.godotengine.org/en/stable/classes/class_camera3d.html).

The published architecture remains revision 09. Branch `main` / cached `origin/main` still points to `a2a90a3e08540e15f40e0ede0f8af14921f54675`; reviewed architecture is `0de4b54dc9d0e711f11962688f0e6fca3aa01c50`. The candidate source/export/evidence is uncommitted. `build.json.checkoutCommit` now identifies the checkout separately from its inherited geographic `sourceCommit`; file/source hashes identify these local edits.

## Browser-only failure and measured repair

The first two browser trials received successful HTTP responses but found no temporary file to verify. The loader rejected them. In the pinned engine's EOF/disconnected path, `HTTPRequest` can complete without setting its download-complete flag; cleanup then removes `download_file` before the callback. Receiving the bounded response body and writing the loader-owned file resolves this in the actual browser. The length/hash check still runs before scene decoding. [Pinned 4.7.2 implementation](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/scene/main/http_request.cpp). An unreviewed intermediate build briefly tried an upstream-only option; pinned-source inspection caught that version mismatch and it was removed before browser testing. Failed results remain separate from passing evidence.

The first successful smoke test used two concurrent requests throughout and opened in **16.76 seconds**, failing the startup gate. Eight opening requests reduced that to **7.05 seconds**. The current opening-only limit is **16**, with the same **32 MiB reservation cap**. The loading screen can process up to three small scenes per frame under a soft 3 ms budget; an individual synchronous load cannot be preempted. During driving the limits remain **two requests and one scene decode per frame**. Each serialized scene is capped at 8 MiB; the largest current scene is 5.49 MiB.

The reservation cap covers requested/verified serialized asset sizes, not all process memory. Response buffers, temporary file copies, decoded mesh data, the WASM heap and GPU resources are different allocations. Tests below report exposed counters and reference release rather than claiming a total RAM ceiling or heap shrinkage.

## Paired startup result

The control is the unchanged 102,660,112-byte revision-09 PCK, SHA256 `8da68329347228060231d47f46e80c9d6233b6afb0469fd43611bdc83204b1d0`. The measured candidate PCK SHA256 is `c8df3784f3bb0d38b4c4d55e8064fc2781bfc336b9443fbde4b42ac5469724dc`. Machine: Apple M1, 8 GiB RAM, macOS 26.6.2 / 25G83; Chrome 155.0.8059.40, 1440×1000, DPR 1. No competing game render or export ran during timed travel. Focus was emulated except in the explicit focus-loss test.

[Raw control](east-village-ev002/control/startups.json) · [raw candidate](east-village-ev002/candidate/startups.json) · [computed comparison](east-village-ev002/startup-comparison.json).

| Condition, five samples each | Control median | Candidate median | Control p95 | Candidate p95 | Proposed gate |
| --- | ---: | ---: | ---: | ---: | --- |
| Network cache disabled | 6.086 s | 6.193 s | 7.097 s | 6.305 s | Pass |
| Network cache enabled | 6.971 s | 6.862 s | 7.978 s | 7.623 s | Pass |

The p95 here is the maximum of five samples, not a large-sample estimate. The gates allow at most 10% median / 20% p95 regression against the corresponding control. The cold median is about 1.7% higher. “Cold” does not reset OS, shader or compiled-WASM caches. Local cache-enabled runs still transferred the bodies because of server behavior; they are not a production immutable-cache benchmark.

All 203 models are still opened initially in this bounded proof. Splitting the files therefore does not materially reduce opening bytes: observed transfer totals were 142,898,551 bytes for the control and 142,973,900 for this candidate. The shared pack is about **7.61 MiB**, safely below the 16 MiB proof budget, and all 203 external compiled scene hashes match the prior census. This creates package room without removing detail; it is not a startup speedup claim.

## Driving, memory, recovery and visual review

The control and timed candidate each completed **20 normal-key legs / ten round trips**, with zero route contacts, game errors or ordinary-network movement holds. All 20 paired p95 frame-gap gates pass; candidate p95 spans 17.4–18.6 ms. These measurements are frame intervals, not a claim of universal 60 FPS. [Raw control](east-village-ev002/control/journey.json) · [raw candidate](east-village-ev002/candidate/journey.json) · [comparison](east-village-ev002/journey-comparison.json).

Two eastbound legs contain isolated **100.5 and 100.8 ms** gaps. Every sample throughout both legs has all 203 buildings resident, zero pending requests/staged bytes, and unchanged activation/retirement counters; they did not coincide with streaming work. Their cause is not established. They remain in the raw maximum and are not discarded as warm-up. Westbound reload legs have no such gap. The gate specifically rejects newly introduced loading-caused >100 ms hitches; this evidence does not justify claiming that the browser never stalls.

Every east stop settles at 191 models; every west stop restores 203. Verbose tree snapshots confirm each resident's model and collider share one owner. All **45** retired weak references clear. Renderer buffer bytes change **251,854,392 → 234,497,894 → 251,854,392**. All ten normalized east checkpoints are identical: 1,250 resources, 234,497,894 buffer bytes and 61,860,901 texture bytes, with zero pending/staged work and zero live retired references. Cycles 2 and 10 therefore meet the no-growth gate. These are exposed live-resource counters, not total process RAM or reserved WASM heap capacity.

All six final-pack recovery scenarios pass: missing file, corrupted body, offline, retry while downloads are held, pause/focus during delay, and cancellation/backtracking. Expected offline fetch errors are retained separately; no unexpected game errors or interception errors remain. [Recovery evidence](east-village-ev002/candidate/failures.json). The existing camera-control review also passes all four modes on the root route. The wide-orbit delayed-load test also passes: the last complete camera view and car remain stationary until west assets are ready. Seventeen address cases and settings persistence, real focus loss, resize, postcard, missing-base-pack retry and graphics-context recovery pass. [Camera controls](east-village-ev002/camera/review.json) · [delayed orbit](east-village-ev002/candidate/camera-hold.json) · [address](east-village-ev002/address/review.json) · [settings/recovery](east-village-ev002/settings/review.json). The first combined recovery trial exposed an intermittent R-retry race: an outstanding response from the failed wave could finish after R had reset only already-failed records. A focused repeat passed, demonstrating intermittency. Explicit retry now cancels and invalidates all outstanding requests and resets their attempt budgets, while retaining verified and active resources. The final pack is **7,981,516 bytes**, SHA256 `fa4d32a0ece9c56bdd4b67e2c94f11c2a01f5dce272bdb675313e8285928cffc`. Startup and ten-trip evidence above belongs to the preceding `c8df3784…` pack; their sole runtime difference is this retry-only repair. All final recovery/control/visual checks identify the repaired pack separately. The timed paths were unchanged; the ten-trip/startup benchmark was not relabeled or repeated after the retry-only repair.

All **27 paired views / 54 images** were inspected: four approach/seam/edge poses, four facade closeups and Tile Bar’s First Avenue entrance, each in golden, dusk and rain. Individual signs/fonts, canopies, surface patterns, display layers, furniture, stairs/railings and street fixtures match the control. Rain, shader time and weather interpolation are not pixel-locked. This is preservation review, not a fresh photographic fidelity pass. [Image hashes and findings](east-village-ev002/visual-review.json).

`npm run seventh:verify` passes **222 required runtime files / 112 source hashes**, all 203 buildings, 82 Seventh frontages and 102 First/St. Marks faces. `npm run verify` passes for the preserved original game. [Preservation](east-village-ev002/preservation.json) checks all 203 authored GLBs/compiled scene hashes, 2,374 other tracked non-Markdown files and both private images. The only additional reviewer change aligns address-runner focus emulation with the existing full/streaming runners after a startup watchdog timeout; the unsuccessful trial remains recorded. Exact [local root, Seventh, legacy and manifest route hashes](east-village-ev002/local-routes.json) pass. [Final validation](east-village-ev002/validation.json) also passes JavaScript syntax, skill structure, documentation links and whitespace. No CI or production result is implied.

## Reproduction and remaining scope

Use the installed engine and existing isolated Chromium review profile on port 9222. Start the local player with `npm run dev`. The browser harness uses real driving keys and explicit review-only starting poses; failed trials are saved with their actual build hashes.

```sh
npm run seventh:build
npm run seventh:verify
npm run verify
node scripts/review-seventh-streaming.mjs renders/ev002/startup startups
node scripts/review-seventh-streaming.mjs renders/ev002/travel journey
node scripts/review-seventh-streaming.mjs renders/ev002/recovery failures
node scripts/review-seventh-streaming.mjs renders/ev002/overview views
node scripts/review-seventh-streaming.mjs renders/ev002/details details
node scripts/review-seventh-streaming.mjs renders/ev002/entry tilebar-entry
node scripts/review-seventh-streaming.mjs renders/ev002/camera-delay camera-hold
```

The control player is reproducible from the baseline commit; a scratch copy under ignored `engine/first-seventh/exports/ev002-control/` is convenient but is not the only evidence. Durable control results include exact runtime/source hashes. To compare a separately served control, set `BOROUGH_REVIEW_URL` and `BOROUGH_REVIEW_BUILD` to its URL and manifest. Do not run competing browser renderers or an export during timed measurements.

**Next session: EV-003**, on the next user instruction. It remains a separate integration session: production/cache-header checks, old-release behavior and broader spatial ownership/route integration need their own evidence before geographic growth. Current roads/props and 191 models remain shared/resident; this test cannot establish whole-East-Village memory or draw-call scaling. Current address/map coverage, photographic fidelity limits, all licenses and both private untracked screenshots remain in force. Nothing has been committed, pushed or deployed by EV-002. This session completes the bounded 12/191 proof, not expansion readiness. The overall 390–725-session / 300–1,100+ model/tool-hour allowance remains provisional; technical debugging time is not storefront throughput. Resize was tested with all assets loaded; changing viewport aspect while west assets are absent still belongs in broader integration coverage.
