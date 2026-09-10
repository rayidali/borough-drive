# Borough Drive session checkpoints

[CODEX-HANDOFF.md](CODEX-HANDOFF.md) holds the current resume state. This log preserves dated milestones in **newest-first order**. Add a checkpoint after meaningful progress and before a planned session handoff; record partial work during long tasks as well. Preserve older entries and record corrections in a later entry.

Use the exact gameplay/source commit as the reproducible baseline. Git history records the commit that saves each checkpoint document:

```sh
git log --oneline -- CODEX-HANDOFF.md SESSION-LOG.md
```

Checkpoint notes describe observed state, not a live monitor. Recheck local files, remote branches and deployment status when resuming. Keep necessary artifacts in the repository and record reproducible commands; temporary directories and old tool/process IDs are not durable checkpoints. Store no tokens, passwords or authentication cookies here.

## 2026-09-10-08 — Browser corner pass and offline block workflow committed locally

**Recorded:** 2026-09-10T05:57:24-04:00 (America/New_York).
**User objective and decisions:** Browser-first smoothness inspired by slowroads.io; defer Unreal, improve First & 7th and prepare economical block work using cheaper AI. Current corner quality is the working benchmark; no wider modeling or paid execution now.
**Completed work:** [Browser pass 09](model-source/BROWSER-PASS-09.md): depth-reused contact shading, adaptive Automatic default, authored clouds/corner road variation and interpolated driving presentation. [Offline workflow](model-source/BLOCK-WORKFLOW.md): 1,348 ownership items, three-facade pilot plan, compact source packets, permission registry and proposal validation. Updated current Markdown/credits, saved before/after profiles, preservation proof, 26-view review and 11 unedited game captures. Opened local preview and confirmed HTTP 200/revision 09.
**Gameplay/source baseline:** New local `main` source `c76dccebc143960498d21eeab8c55c2d0dbcc5ce`; prior model/source `219d4e9ccec8e019351d3a27d7dff6dcaf07237d`. All 72 checked models/images/JSON manifests and preserved physics/collision/spatial/glass/texture modules remain byte-identical. No Blender/source compilation or new imagery request this turn.
**Local changes:** All implementation, offline workflow, current reports and evidence committed. Only `CODEX-HANDOFF.md` and `SESSION-LOG.md` were modified before this separate checkpoint commit, identifiable through Git history. Ignored `.env` stays local/mode 0600. No required runtime check or model export pending.
**Remote state:** No fetch or push. Cached origin/main remains `477fcdb524407e189f67eb59771d8da84c4a16fe`; source commit is four ahead and this subsequent checkpoint adds one unpublished commit.
**Deployment state:** No deployment, CI or live verification. Last verified production source `522cd1de77b72186dc98e06a3b9f6ce4db761d8b` at https://borough-drive.vercel.app is historical September 9 evidence. Passes 08/09 remain local.
**Validation:** Final `npm run verify` passed (30 modules, 2,308 road samples, vehicle/export/material/spatial and new presentation tests); offline workflow tests and current saved-packet validation passed. Final 26-view browser review passed controls, resets, fresh Automatic/saved quality, idle wake and both forced-load recovery paths with zero unexpected errors/failed requests. Final full/shop/driving captures visually inspected for presentation regressions, not fresh photographic accuracy. Before checkpoint: whitespace clean, 308 relative Markdown links valid, 336 eligible files scanned with zero credential matches.
**Performance:** Chrome 152/M1, 1440×1000 DPR 1, local HTTP: Detailed Saifee 48.9→52.4 FPS, submissions 3.83M→1.92M triangles / 596→301 calls; Detailed drive 27.1→32.9, core SE 29.3→33.9. Warm Automatic corner 60.0; additional warm drive 48.0 overall / 55.9 last 120 rendered frames, ratio 0.70/contact shading off; stopped quality restored and zero idle redraws. Short samples/fixed-frame routes differ; no universal 60 FPS or slowroads.io comparison claim.
**Unresolved issues:** Dense driving remains below consistent 60 FPS. Existing architectural/artwork/dimension/occlusion uncertainty remains. New source registry has no approved images; Google standard terms restrict the proposed bulk/derived-content processing, so Google batch is disabled without suitable additional permission. GPT-5.4 Mini has not been evaluated; $0.162 is illustrative three-job Batch token arithmetic only. Zero paid jobs/model requests; no auto merge/build dispatcher or accepted-work ledger. Actual patch records and rendered quality still need coordinator review; older compiler render-height reset issue remains documented.
**Next action:** Restart with `npm run dev`, review First & 7th in Graphics → Automatic on the user's device, register suitable dated full/oblique images, then qualify the cheaper worker on three facades and measure corrections/cost before expanding. No automatic migration, publishing, paid batch or wider modeling.

## 2026-09-10-07 — Browser-first direction selected; runtime and workflow underway

**Recorded:** 2026-09-10T05:22:41-04:00 (America/New_York).
**User objective and decisions:** Defer Unreal; improve First & 7th while prioritizing smooth browser play, then prepare a repeatable block process suitable for cheaper AI workers. Current corner quality is the working map-wide reference.
**Completed work:** Baseline profile and source inspection; initial depth-reused shading, sky/road presentation, driving interpolation and adaptive Automatic implementation. Investigated official OpenAI mini/Batch options and Google imagery restrictions.
**Gameplay/source baseline:** `219d4e9ccec8e019351d3a27d7dff6dcaf07237d`; initial main HEAD `4682fef`, clean and three commits ahead of cached origin/main.
**Local changes:** Runtime modules/viewer/road renderer/index and these checkpoints uncommitted. Offline workflow implementation pending. All existing GLBs/source geography/vehicle physics preserved.
**Remote state:** No fetch or push.
**Deployment state:** No deployment/live check; prior September 9 public verification remains historical.
**Validation:** Baseline browser profile completed; first depth-reuse profile completed and inspected. Initial npm checks passed; final runtime/Automatic/visual checks pending. No paid AI job or new imagery request.
**Unresolved issues:** Smooth 60 FPS across dense views is not established. Google standard terms do not authorize the proposed bulk/derived-content workflow; automation needs suitable imagery rights. Mini model quality has not been evaluated on this task.
**Next action:** Finish the local browser pass and finite offline task workflow, test validation/recovery/budget behavior, record results and local commits, and open the preview.

## 2026-09-10-06 — Assessed browser versus Unreal for the final game

**Recorded:** 2026-09-10T05:02:39-04:00 (America/New_York).
**User objective and decisions:** Asked about improving sky, roads and driving to a PS5-game standard versus using Unreal later and retaining the model pipeline. No migration choice has been confirmed.
**Completed work:** Inspected runtime and export structure; checked official Epic references. Added [ENGINE-DIRECTION.md](model-source/ENGINE-DIRECTION.md) recommending an early single-corner Unreal test, modular model export, retained browser preview and explicit hardware/delivery tradeoffs. This is advice, not an implemented visual/driving pass.
**Gameplay/source baseline:** Unchanged local `219d4e9ccec8e019351d3a27d7dff6dcaf07237d`; session-start documentation HEAD `179c994` on clean `main`.
**Local changes:** Assessment plus handoff/session documentation only, saved in their own local checkpoint commit. No sky, road, vehicle, model or export edits.
**Remote state:** No fetch or push. Started two commits ahead of cached origin/main `477fcdb524407e189f67eb59771d8da84c4a16fe`; the following documentation commit is also local.
**Deployment state:** No deployment or live check. September 9 source `522cd1d` remains the last verified public version; pass 08 remains local.
**Validation:** Read-only source/GLB inspection and official documentation review. No new runtime tests or Unreal import/benchmark; prior pass 08 evidence remains dated history.
**Unresolved issues:** User's engine direction and visual acceptance pending. AAA fidelity is not achieved by changing engines alone. Current merged/compressed browser exports need an import test and a separate modular export path; runtime roads, vehicle, sky and UI do not transfer automatically. M1 feature limits and potential streamed-browser GPU costs need consideration.
**Next action:** Follow the user's engine-direction choice. Proposed Unreal test is five corner buildings, one road segment and one vehicle before scaling. No automatic migration, expansion or paid hosting.

## 2026-09-10-05 — Street View corner refinement verified and committed locally

**Recorded:** 2026-09-10T04:36:37-04:00 (America/New_York).
**User objective and decisions:** Use the working Street View key to improve all four corners of First Avenue/East 7th toward Assassin’s Creed Unity-level detail. Keep the accepted minimum and speed improvements. No new publishing or geographic expansion instruction.
**Completed work:** Implemented dated facade, shop and street-detail corrections; exported only three affected sections. Corrected Burger glazing and retained masonry detail with lower-cost surface bands. Saved 37 unedited game captures, 26-view browser review, 11 reference-position comparisons, source observations, preservation proof and final performance data. Current source/docs are committed; local preview opened. See [pass 08](model-source/FIRST-SEVENTH-PASS-08.md).
**Gameplay/source baseline:** New local source `219d4e9ccec8e019351d3a27d7dff6dcaf07237d` on `main`; prior published source `522cd1de77b72186dc98e06a3b9f6ce4db761d8b`. Initial checkpoint HEAD `477fcdb524407e189f67eb59771d8da84c4a16fe`; existing uncommitted access setup and notes preserved.
**Local changes:** Source commit contains all implementation, assets, helpers, reports and screenshots. Only `CODEX-HANDOFF.md` and `SESSION-LOG.md` remained modified before this separate checkpoint commit. No pending export, image capture or required technical check. Ignored `.env` stays local; all temporary Google reference JPEGs deleted.
**Remote state:** No fetch or push this turn. Cached origin/main remains `477fcdb524407e189f67eb59771d8da84c4a16fe`; source and following checkpoint commit are unpublished.
**Deployment state:** No new deployment/live recheck. September 9 verified production source `522cd1d` remains historical. Local preview is http://127.0.0.1:5173; reopen with `npm run dev`.
**Validation:** Final `npm run verify` passed after metadata refresh (26 modules, 2,308 road samples, collision/navigation/source checks, 63 maximum batches); clean reproduction matched 615 buildings and three audits. Twenty-four protected files and three final asset hashes verified. Browser controls/loading/error-recovery checks passed; only the deliberately injected failure warning appeared. Final corrected Burger and Saifee mortar views inspected. M1 local samples: 48.9 FPS Detailed Saifee, 60.0 Faster, 26.8 driving, 27.8 core SE; 38.86 MiB initial transfer, zero idle redraws. All 251 relative links in 19 Markdown files resolved before final checkpoint edits; diff whitespace clean. Private credential scan: zero leaks across 302 eligible repository files, `.env` ignored and mode 0600.
**Unresolved issues:** Visual acceptance of 08 pending. The result remains stylized, below a perfect 1:1 or AAA-production claim. Artwork, lettering, dimensions, occluded shop details and interiors still contain approximations. Source-position comparisons reveal proportion/framing differences. Compiler still resets three unrelated exported render heights; the report records preservation steps.
**Next action:** Review local chapter 08 with the user, compare dated angles and address their specific remaining corner feedback. Keep the existing accepted 06 baseline until they accept the refinement; do not start expansion or publish solely because this checkpoint exists.

## 2026-09-10-04 — Corner export and speed verified; final capture in progress

**Recorded:** 2026-09-10T04:21:22-04:00 (America/New_York).
**User objective and decisions:** Same authorized four-corner refinement; preserve the speed improvements. No wider map expansion or new deployment requested.
**Completed work:** Corrected the paint layer covering Burger’s glazing; added red dining structure and tactile paving. Shared matte vertex colors fixed the 64-batch limit. Replaced raised mortar boxes with surface bands to recover performance, preserving running bond and window exclusions. Final three GLBs exported. Current docs and photographic credits refreshed.
**Gameplay/source baseline:** `522cd1de77b72186dc98e06a3b9f6ce4db761d8b`; main HEAD remains `477fcdb524407e189f67eb59771d8da84c4a16fe`.
**Local changes:** Implementation, assets, observations, reports and docs remain uncommitted. No key or Google photograph enters Git or game assets.
**Remote state:** No commit, fetch or push in this refinement turn.
**Deployment state:** No deployment or live recheck; September 9 evidence remains historical.
**Validation:** Final npm verification passed: 26 modules, 2,308 road samples, collision/source/export checks, 63 maximum batches; 9,435,099 actual neighborhood triangles. Core/runtime/eleven other GLBs and all mapped footprints/roads preserved. Earlier clean reproduction matched three audits. Final M1 profile measured 48.9 FPS Detailed Saifee, 60.0 Faster, 26.8 driving, 27.8 core SE; 38.86 MiB initial transfer and zero idle redraws. See `first-seventh-08-performance.json` for conditions and limitations.
**Unresolved issues:** Final capture/inspection and source-status refresh pending. AAA quality, exact artwork, dimension matching and occluded current details are not established; report 08 lists those limits.
**Next action:** Finish and inspect final browser/reference-position captures, save durable evidence, run final source checks after status changes, checkpoint local commits and open the local review version.

## 2026-09-10-03 — Street View corner refinement authored; export/review underway

**Recorded:** 2026-09-10T03:52:43-04:00 (America/New_York).
**User objective and decisions:** Use the saved Street View key to improve First Avenue/East 7th across all four corners, aiming for Assassin’s Creed Unity-level detail. Keep the accepted standard and speed gains; no new expansion.
**Completed work:** Inspected April 2026 intersection views and closer September 2024 west/Yubu views; rejected a November 2017 selection. Recorded eight panorama sources and uncertainty. Authored current shop signs, side storefronts, facade/window corrections, canopy changes, open steel escapes, paint approximations and street hardware in the reproducible corner recipe. Baseline browser review completed 26 views without errors.
**Gameplay/source baseline:** `522cd1de77b72186dc98e06a3b9f6ce4db761d8b`; main HEAD `477fcdb524407e189f67eb59771d8da84c4a16fe`.
**Local changes:** Corner recipes/schedules, compiler/signature integration, manifest/audits, access helpers, verification and checkpoint files uncommitted. Export of three affected sections underway. The ignored local key remains private; temporary reference images are excluded from the game and repository.
**Remote state:** No commit, fetch or push this turn.
**Deployment state:** Not deployed or rechecked; September 9 remains the latest published verification.
**Validation:** Python syntax and compiler succeeded. Only three corner tile signatures changed. Three unrelated exported heights were restored after compilation. Baseline browser checks passed. Final exports, model verification, matched-view review, reproduction and performance checks are pending.
**Unresolved issues:** Geometry has not yet been visually reviewed. Some art, lettering, dimensions, interiors and occluded Yubu/Burger details remain estimates. AAA quality and 1:1 perfection are not established by source access or compilation.
**Next action:** Finish Blender export; run verification, inspect the actual game and correct defects. Preserve the core/runtime, finalize evidence/docs and open the local result for review.

## 2026-09-10-02 — Google Street View API and actual image access confirmed

**Recorded:** 2026-09-10T03:24:49-04:00 (successful API response; America/New_York).
**User objective and decisions:** The user saved the local API key and asked whether Street View access works. Scope remains a bounded access test.
**Completed work:** Google's metadata returned `OK` for First & 7th, panorama `3KfZRLIHzFKvx7gJYrDH-w`, imagery date `2026-04`. A single 640×640 image request returned HTTP 200 and 95,415 bytes. The JPEG was opened and visually inspected: E7 Deli's corner, upper facade and street details are visible. Attribution: © Google. The temporary preview is removed after inspection; no Google imagery enters game assets or Git.
**Gameplay/source baseline:** `522cd1de77b72186dc98e06a3b9f6ce4db761d8b`; main HEAD remains documentation `477fcdb524407e189f67eb59771d8da84c4a16fe`.
**Local changes:** Access checker and two checkpoint documents uncommitted; populated `.env` remains ignored and owner-only. Key values and authenticated URLs are never recorded. No game/model changes.
**Remote state:** Not fetched or pushed this turn; cached origin/main matches HEAD.
**Deployment state:** No new deployment or live check. September 9 publication remains the latest verified state.
**Validation:** Node syntax, empty-key behavior, ignore rule and file permissions checked. One metadata and one image request succeeded; actual visual inspection confirms image access. Game verification was not needed for this local utility.
**Unresolved issues:** This proves access to one April 2026 panorama, not newest-imagery availability everywhere, a full-corner comparison or completed model corrections. Earlier modeling used the recorded alternative sources. Broader imagery use and batch processing need the later workflow discussion.
**Next action:** Report successful access. Follow the user's next modeling/planning instruction; use the bounded checker for future connectivity checks and keep the credential local.

## 2026-09-10-01 — Street View credential file opened; access test awaits saved key

**Recorded:** 2026-09-10T03:23:53-04:00 (America/New_York).
**User objective and decisions:** Prepare and open a local file with the Google API key name filled in; the user will paste its value. Test actual Street View access afterward. No modeling or new publication requested.
**Completed work:** Created the ignored, owner-only root `.env`, preserving existing values, and opened it in TextEdit. Added `scripts/check-street-view-access.mjs`: metadata-only by default, with `--image` retrieving at most one image for First & 7th into a temporary owner-only directory. Requests go directly to Google's official API; keys and request URLs are not logged.
**Gameplay/source baseline:** `522cd1de77b72186dc98e06a3b9f6ce4db761d8b`; branch `main`, documentation HEAD `477fcdb524407e189f67eb59771d8da84c4a16fe`. Resumed clean.
**Local changes:** Checker, handoff and this log uncommitted. Ignored `.env` is local only; its value was still empty at the checkpoint. No game/model changes.
**Remote state:** Not fetched or pushed this turn; cached origin/main matches HEAD.
**Deployment state:** Not deployed or rechecked. September 9 source publication and live verification remain the latest evidence.
**Validation:** Node syntax check passed; the empty-key path sent no network request. Git ignores `.env`. Google's official metadata/image request documentation was consulted. No game verification run for this local access utility.
**Unresolved issues:** Key entry and API access are pending. No Google Street View imagery has been accessed or used to modify the game.
**Next action:** Once the key is saved, run `node scripts/check-street-view-access.mjs --image`; inspect a successful preview and delete it afterward. Report the actual image date or Google's denial reason without exposing credentials, and update this checkpoint.

## 2026-09-09-03 — Accepted corner and speed pass pushed; live files verified

**Recorded:** 2026-09-09T01:19:25-04:00 (America/New_York).
**User objective and decisions:** First & 7th revision 06 is the minimum completion standard. Speed optimization, main publication and Markdown refresh authorized. Economical block/street work for East Village, then Manhattan/NYC, awaits the next planning discussion; no expansion/jobs/services now.
**Completed work:** Published the accepted corner plus runtime speed pass. Retained all existing models/photographs/recipes and mapped geometry. Saved 28 final local captures, before/after profiling, preservation hashes, source acceptance and all 18 Markdown updates. Live browser smoke passed: the production Saifee view rendered with all five starting sections loaded and zero errors/failed requests.
**Gameplay/source baseline:** `522cd1de77b72186dc98e06a3b9f6ce4db761d8b`. Accepted visual/model baseline `0f40856c9c576d1648ddae9c6e76bb550a98b42a`; resumed checkpoint `e86a480`.
**Local changes:** Implementation/evidence committed in `522cd1d`; this publication checkpoint and its verification JSON follow in a separate documentation-only commit, identifiable through Git history. No unfinished source/model work.
**Remote state:** Fetched existing main, preserved both unpublished commits and fast-forward pushed `a44257a..522cd1d`; no force push or new repository.
**Deployment state:** Vercel success for `522cd1d`, deployment `6CxayAae3s7cYSh1cHWNHUy7YA18`. All 20 changed live game files matched the commit over HTTPS; eight additional core/photo/decoder assets matched. Evidence: `model-source/publication-review-2026-09-09.json`. Existing URL: https://borough-drive.vercel.app.
**Validation:** npm verification passed locally; both GitHub Node.js 22/24 jobs passed in run `34314169298`. Road/model/source checks, exact street subset and lossless spatial tests passed. Clean preparation/compilation reproduced all source data and three audits. Final 26-view browser review, two travel captures, resets/graphics/idle wake-up and both deliberate load failure recoveries passed; no unexpected errors. 212 relative Markdown links checked before publication.
**Performance:** M1 1440×1000 DPR 1, local HTTP: Detailed Saifee 25.2→50.2 fps, core SE 17.9→28.6, driving stress 20.7→28.1. Faster 56.5→60.0. Initial transfer 89.61→38.24 MiB, surface requests 42→9, zero settled scene redraws. Single-device short samples; driving route duration/distance varies with frame rate.
**Unresolved issues:** Dense driving/retina views need further performance work for a universal 60 fps target. Prior imagery/dimension/hidden-surface uncertainty and wider fidelity backlog remain. No claim of newest Google panorama verification or citywide completion.
**Next action:** Review speed on the user's device and discuss the block/street process using the accepted corner standard. Do not automatically start expansion or paid batch work.

## 2026-09-09-02 — Speed pass verified; final publication preparation

**Recorded:** 2026-09-09T01:13:31-04:00 (America/New_York).
**User objective and decisions:** Accepted First & 7th revision 06 as the minimum completion standard; optimize speed, push to main and update all Markdown. Wider economical street/block work and Manhattan/NYC remain a later planning discussion.
**Completed work:** Deferred core loading using exact street-material subset; shared surface image download/decode; lossless spatial batching; thin-pane reflections without extra city render; idle render gating, visible-light culling and lazy fallback. Recorded acceptance in source metadata and refreshed all 18 Markdown files. Preserved all original model/photographic assets; restored three compiler-reset export-height fields.
**Gameplay/source baseline:** `0f40856c9c576d1648ddae9c6e76bb550a98b42a`; current checkpoint HEAD `e86a480` before the new source commit.
**Local changes:** Runtime, scripts, metadata, performance report, source hashes and 28 game captures uncommitted. Final preserved-manifest review repetition also passed. No Blender export.
**Remote state:** Fetched origin/main remains `a44257a`; nothing pushed yet this task.
**Deployment state:** No new live check/deployment yet; existing site still uses pass 05.
**Validation:** npm verification passed, including new material-subset/spatial-preservation checks and 2,308 road samples. Clean prepare/compile reproduced source fields and all three audits. Browser reviews passed controls, resets, all core/corner views, quality persistence, idle wake-up, map travel and deliberate load failure retries; no unexpected errors. 211 relative Markdown links checked.
**Performance:** Final M1 1440×1000 Detailed: Saifee 25.2→50.2 fps, core SE 17.9→28.6, driving stress 20.7→28.1. Initial reconstruction transfer 89.61→38.24 MiB; texture requests 42→9; zero idle scene redraws. Single-device local HTTP measurements, short samples and different stress-route distances; not a universal 60 fps result.
**Unresolved issues:** Push/deployment verification pending. Dense views/driving still have performance headroom. Prior photographic uncertainties and whole-map fidelity backlog remain; no automatic batch or paid service configured.
**Next action:** Finish review evidence, commit/push source to main, verify CI/Vercel and live hashes, then save and push the publication checkpoint.

## 2026-09-09-01 — First & 7th accepted; authorized speed optimization and publication

**Recorded:** 2026-09-09 (America/New_York).
**User objective and decisions:** First & 7th revision 06 is accepted as the minimum completion standard. Optimize website speed, preserve visual quality, push to main and refresh all Markdown. Discuss economical street/block processing for the rest of East Village and later Manhattan/NYC after this task; no expansion or jobs now. User also asked how to supply Street View references and whether Firecrawl would help.
**Completed work:** Inspected checkpoint, clean branch/history and fetched origin. Added an isolated-browser performance harness. Baseline identifies large material batches and repeated glass/AO rendering as substantial costs. Research found official Google API setup and extraction/derived-content restrictions; Firecrawl does not establish imagery access or rights.
**Gameplay/source baseline:** `0f40856c9c576d1648ddae9c6e76bb550a98b42a`; initial checkpoint HEAD `e86a480`.
**Local changes:** Uncommitted profiling harness and spatial batch runtime optimization; implementation and validation underway. Existing GLBs, vehicle and source recipes unchanged.
**Remote state:** Fetched origin; main remains two local commits ahead of `a44257a`. No push yet.
**Deployment state:** No new deployment or live verification; prior pass 05 remains production.
**Validation:** Baseline M1 / ANGLE Metal, 1440×1000 Detailed: 25.2 fps at Saifee, 20.7 fps driving; full baseline and final comparison pending. No new npm verification claimed yet.
**Unresolved issues:** Runtime optimization must be measured and visually reviewed before publication. Imagery dates/dimensions retain prior uncertainty despite user acceptance. Map-wide completion remains future work.
**Next action:** Complete and test optimizations, preserve durable performance evidence, update docs, commit/push and verify the existing Vercel deployment.

## 2026-09-08-08 — First & 7th comparison pass verified and saved locally

**Recorded:** 2026-09-08T22:20:14-04:00 (America/New_York).
**User objective and decisions:** Resume only First Avenue / East 7th Street, using the most recent accessible view, to establish a detailed benchmark before extending block by block. Google Street View comparison is the user's standard; Assassin's Creed Unity refers to desired detail. No migration or new publication instruction.
**Completed work:** Five individual building profiles, nine elevations and eight shop treatments; revised Saifee and 113 proportions/materials, individual architectural elements, storefront openings/signs, Tile Bar tilework and joined canopy, plant racks, furniture and street hardware. E7 Deli, Saifee, Monkey Sushi and Burger identities supported by explicit sources; old Unique small exterior notice retained from the dated photo. Added four corner view buttons and graphics modes, physical glass/reflections and display lights. Saved all 22 final unedited game captures, source dates/access limitations, checks and a new pass report. Refreshed all current Markdown pointers while preserving historical entries and license terms.
**Gameplay/source baseline:** New local source/gameplay commit `0f40856c9c576d1648ddae9c6e76bb550a98b42a`. Previous published gameplay `63757cbbb13749584e761e4bf7a8e655f90b1bd4`; initial clean documentation HEAD `a44257a0a45c627176ed618f179cba53e5820940` on `main`.
**Local changes:** Source, exports, runtime, observations, report and captures committed. This checkpoint is a following documentation commit identified by Git history. No pending model export or known failing check. Source data and all review artifacts are tracked; temporary images/processes are unnecessary to resume.
**Remote state:** Not pushed; remote not fetched; cached `origin/main` is `a44257a`. Local commits are separate from remote publication.
**Deployment state:** No new deployment or live check. Existing Vercel production remains the previously published pass 05. Review revision 06 through the local server.
**Validation:** Final `npm run verify` passed on Node.js 24.15.0, including 2,308 road samples, source/model signatures, five-profile/nine-elevation checks, safe starts, navigation and walking collision. Clean prepare/compile reproduced source fields and all three generated audits. Final 22-viewpoint browser review had zero uncaught exceptions, console errors and failed HTTP responses; start, northbound driving, both resets, corner controls and quality persistence passed. Existing RGBELoader warning remains. Fourteen GLBs total 51.78 MiB / 9,389,484 triangles, maximum 62 material batches. Core GLB/recipe/vehicle/six photos and all mapped geometry/heights/roads/bounds preserved. Six signature-only exports verified binary payload-identical to pass 05. Whitespace checks and 191 relative Markdown links passed.
**Performance:** Two sequential 120-frame stationary samples at the southeast corner, Chrome/Apple M1/ANGLE Metal, 1440×1000, pixel ratio 1: 25.0 fps Detailed (AO, four samples, physical glass) and 56.3 fps Faster (no AO, two samples, simpler glass). Not sustained driving or multi-device performance evidence.
**Unresolved issues:** User acceptance and exact Street View matching remain pending. Google panorama access failed; dates differ by reference. Obscured artwork, tiny labels/fonts, full interiors/return surfaces, material scans and measured dimensions are incomplete or inferred. The whole-map backlog is still 177 supported non-core names with estimated designs; source coverage is not equivalent to complete fidelity.
**Next action:** Review the local four-corner buttons and saved images with the user. Apply their concrete discrepancies within First & 7th before expanding. Check a new publishing instruction before pushing; preserve the accepted First & 10th core.

## 2026-09-08-07 — First & 7th exports reviewed; corrections in progress

**Recorded:** 2026-09-08T21:50:54-04:00 (America/New_York).
**User objective and decisions:** Most recent accessible view; four-corner First & 7th benchmark, compare with Street View before extending. No engine migration or new publication instruction.
**Completed work:** Added five individual building profiles/nine elevations, eight shop recipes and dated sources, corrected tenant identities and proportions, exported three corner sections. Implemented review viewpoints and manual graphics quality. First real-browser review captured 22 views and found specific depth/join/lettering defects; correction source now authored.
**Gameplay/source baseline:** `63757cbbb13749584e761e4bf7a8e655f90b1bd4`; checkout HEAD remains `a44257a0a45c627176ed618f179cba53e5820940` on `main`.
**Local changes:** Revision 06 runtime, source JSON/Python, compiler, three GLBs and checkpoint files uncommitted. Six other previously detailed sections are being re-exported solely because the shared recipe integration changed their provenance signature. After that, recompile and rebuild the three corner sections for current corrections.
**Remote state:** No fetch or push in this task.
**Deployment state:** No new deployment/live check; production remains the previously published pass.
**Validation:** Initial 22-view review, zero uncaught exceptions/HTTP failures, start and driving/reset checks passed. Preliminary 120-frame stationary M1 samples 42.1 fps Detailed / 60.0 Faster at 1440×1000. Full verifier reports expected stale six-section signatures; final export, source reproduction and final visual review pending. These performance figures predate the latest glass reflection/detail corrections.
**Unresolved issues:** Google panorama unavailable; latest accessible exterior photographs differ in date and some dates are unknown. Estimated dimensions, obscured murals and return elevations remain explicit. Corner-room side walls were obscuring recessed doors; Tile Bar tiles were behind paint and awning letters floated; fixes require fresh exports and inspection. Do not call the benchmark 1:1 or user accepted.
**Next action:** Complete regeneration, compile/rebuild affected three corners, inspect final running-game views, perform checks, preserve evidence/captures and refresh all current documentation before handoff.

## 2026-09-08-06 — First & 7th corner benchmark resumed

**Recorded:** 2026-09-08T21:00:17-04:00 (America/New_York).
**User objective and decisions:** Explicitly resume modeling at First Avenue / East 7th Street, establish a highly detailed intersection benchmark, then extend step by step after user review. User will compare with Google Street View and confirmed the most recent accessible view. Previous pause superseded; no engine migration or geographic expansion requested.
**Completed work:** Read resume documents and inspected clean checkout; identified all four corner footprints and current sparse/generic treatments. Started real-view acquisition and baseline rendering review.
**Gameplay/source baseline:** `63757cbbb13749584e761e4bf7a8e655f90b1bd4`; clean documentation HEAD `a44257a0a45c627176ed618f179cba53e5820940` on `main`.
**Local changes:** Checkpoint and active scope instructions updated. No new mesh exported yet.
**Remote state:** No push; remote not fetched; cached `origin/main` equals HEAD.
**Deployment state:** No new deployment or live check. Prior `a44257a` documentation deployment is separate from this work.
**Validation:** Git inspection and prior actual-game capture inspection. New model/browser comparison and `npm run verify` pending.
**Unresolved issues:** Need recent accessible imagery, explicit two-street corner schedules, southeast tenant/architecture correction and matched-view visual review. Exact dimensions and unseen features remain unmeasured.
**Next action:** Complete reference acquisition, implement all four corner faces and storefront detail, export affected sections, and review the running game.

## 2026-09-08-05 — All Markdown synchronized for closing and resuming the session

**Recorded:** 2026-09-08T17:51:23-04:00 (America/New_York).
**User objective and decisions:** Update all project Markdown so work can resume after closing this session. The earlier instruction to pause modeling for review still applies. The full-map fidelity objective remains unfinished; the user has not chosen an engine migration. The assistant's Blender/Three.js recommendation is recorded as a recommendation, not a user decision.
**Completed work:** Refreshed all 16 tracked Markdown files: README, start guide, agent instructions, contribution guide, PR template, handoff/log, neighborhood/pass notes, core reference notes, asset credits and third-party notices. Corrected the README reset to First & 7th, current published pass/counts, linked the new actual-game captures, mapped source/provenance records and reproduction/review commands, and marked older reports as historical. Clarified that old temporary research filenames may not be bundled. Removed automatic-continuation wording that conflicted with the review pause. Preserved dated history, architectural observations, all attributions and license terms.
**Gameplay/source baseline:** Unchanged `63757cbbb13749584e761e4bf7a8e655f90b1bd4` on `main`. This documentation task began with clean `main` equal to fetched `origin/main` at `ab9b12b851826bdfebfc10a9f9589c767b7f20ad`.
**Local changes:** Markdown only, saved in a separate documentation commit identified through Git history. No edits to runtime code, GLBs, evidence JSON, fonts or photographs; no pending model rebuild. The Markdown asset-credits file under `dist/` is served content, so its documentation bytes change while gameplay remains at the stated baseline.
**Remote state:** Prior gameplay/source/checkpoints confirmed pushed through `ab9b12b`; this Markdown refresh is the following documentation commit. On resuming, compare its Git history with fetched `origin/main` rather than inserting its own hash into the checkpoint.
**Deployment state:** Existing site `https://borough-drive.vercel.app`; Vercel success confirmed for both `43910e6` and the following documentation commit `ab9b12b`. The 17-file comparison at 17:37 on September 8 is preserved in `model-source/publication-review-2026-09-08.json`. That is a dated check of the then-current files, including the older credits Markdown. This refresh adds no new game/model deployment; a documentation deployment can follow its push.
**Validation:** All 16 tracked Markdown files updated, with no non-Markdown working changes. Checked 175 relative links and six heading anchors: no failures. Current counts match the saved manifest/coverage inventory. Earlier session-log entries, historical pass contents and core architectural observations were preserved; attributions/license terms reviewed unchanged. `git diff --check` passed. No new local `npm run verify`, Blender export, clean compile or browser review in this Markdown-only task; prior implementation and publication checks remain in their dated records.
**Unresolved issues:** The same map-wide gaps remain: 178 of 200 supported non-core names still use estimated shop designs; all 641 non-core frontages are inventoried and the revised designs also contain estimates. Recording those gaps is not fixing them. The individual First & 10th standard was not applied throughout the map, and the prior limited cutoff was not an engine limit. Current photography, measured dimensions, exact artwork/material samples and unseen elevations remain incomplete.
**Next action:** Reopen the repository, read `AGENTS.md`, this latest entry, `CODEX-HANDOFF.md`, `START-HERE.md` and neighborhood notes, inspect Git state, and follow the user's review/new instruction. If no new instruction is supplied, keep modeling paused. Existing exports and tracked source/review records are sufficient to resume; old processes, temporary downloads or chat history are not required.

## 2026-09-08-04 — Existing storefront pass pushed and verified live; modeling paused

**Recorded:** 2026-09-08T17:37:54-04:00 (America/New_York).
**User objective and decisions:** User asked why the detailed First & 10th treatment had not been applied to the whole map and what photo sources were used. They explicitly said not to continue modeling now, authorized pushing the completed work for review, and will decide the next step. The prior limited-pass scope decision did not fulfill their map-wide request.
**Completed work:** Confirmed a clean checkout and existing repository/hosting configuration, fetched `origin`, pushed the completed local commits to `main`, checked Vercel/GitHub status, and compared every changed live game file against the gameplay commit. No models, runtime code or source observations changed in this publication turn. Photo source explanation uses the existing credits, core reference inventory and storefront schedule.
**Gameplay/source baseline:** `63757cbbb13749584e761e4bf7a8e655f90b1bd4`. Published Git HEAD was `43910e6ce72b6f0a46e11e8e0109ce913a8a49e8`, which adds only the earlier checkpoint to that gameplay commit.
**Local changes:** Publication evidence saved in `model-source/publication-review-2026-09-08.json`; this log and handoff refreshed. These records are committed separately; identify their commit through Git history. No unfinished export or new feature work.
**Remote state:** Fast-forward push to existing `rayidali/borough-drive` `main` succeeded, from `5753989` through `43910e6`. Publication documentation follows in its own pushed commit; no force push or new repository.
**Deployment state:** Vercel reported deployment completed for `43910e6`: `https://vercel.com/rayidalis-projects/borough-drive/BgBbueBJUDVDnGMDfrt1cXcJcLM4`. `https://borough-drive.vercel.app` served all 17 changed published files byte-identical to gameplay `63757cb`, including nine GLBs, the manifest, page, runtime modules, sources and notices. Documentation-only deployments can follow without changing the verified game files.
**Validation:** `npm run verify` passed again before pushing (2,308 road samples; source/model references and signatures; vehicle/navigation/collision checks). GitHub Actions Node.js 22 and 24 both succeeded. Live SHA-256 comparisons passed for all 17 changed files. System curl used normal TLS verification; Python urllib initially lacked its local issuer certificate, so retrieval switched clients without disabling verification. No new full browser/visual/performance review; the earlier 56-viewpoint review remains separately recorded.
**Unresolved issues:** The full digital-twin objective remains unfinished: 178 supported non-core names still use estimated shop designs; revised shops and building dimensions also contain estimates. Archived photos have varying/unknown capture dates. Source archives and business websites provide references, not an automatic complete street-level survey. These gaps were not fixed by documenting them.
**Next action:** Await the user’s review of the published game. Do not expand modeling or migrate engines until their next instruction.

## 2026-09-08-03 — First & 7th and storefront pass 05 verified; saved locally

**Recorded:** 2026-09-08T17:26:41-04:00 (America/New_York).
**User objective and decisions:** Start at First Avenue/East 7th and make the existing map faithful down to signs/neon, boards, furniture, paint, proportions and architectural elements. Preserve First & 10th. Keep Blender asset authoring plus the existing Three.js browser runtime; Unreal is a possible future desktop evaluation, not an implemented migration. No new publication requested.
**Completed work:** Start/reset in both modes and a map shortcut; 22 explicit shop designs, 26 separate elevation controls and 29 source records across nine rebuilt sections. Corrected Ralph's/Danny & Coop's duplicate identities and the latter's building join. Added ten sidewalk object colliders, licensed script lettering, source signatures, coverage/reproduction/browser-review scripts, credits and three unedited game captures. Visual refinements include Tile Bar stripes, door/base/furniture and side bay spacing, sign readability and projecting signs. Details and limits: `model-source/STOREFRONT-PASS-05.md`; durable test/asset records: `model-source/storefront-review-2026-09-08.json`.
**Gameplay/source baseline:** Current local `63757cbbb13749584e761e4bf7a8e655f90b1bd4` on `main`. Session began clean at documentation `5753989`, following gameplay `835ea6cb53f7b88ebc0edc9586080f9c371b9d20`.
**Local changes:** Gameplay/source/models/reviews committed in `63757cb`. Checkpoint documents saved separately; identify their own commit with Git history. No pending export or known failing check. All necessary source and reviewed game captures are in the repository; ignored `renders/` and temporary browser processes are optional conveniences.
**Remote state:** New work not pushed. Remote not fetched; cached `origin/main` remains `5753989`.
**Deployment state:** No deployment or new live verification. Historical production verification of `835ea6c` on September 6 remains separate from this local pass.
**Validation:** Final `npm run verify` passed on Node.js 24.15.0: 2,308 road samples, source/model signatures, module/asset references, spawns/vehicle invariants and walking object collision. Nine final Blender exports succeeded; fourteen neighborhood GLBs total 49.14 MiB, 8,906,922 actual GLB triangles, maximum 50 material batches. Chrome on Apple M1 reviewed 56 viewpoints (start, 22 shops, seven projecting-sign angles, 26 elevations), with zero uncaught exceptions/failed HTTP responses. Start `(0,228)` northbound, driving and both reset modes passed. Disposable clean prepare/compile matched all source fields for 615 buildings and three generated audits, excluding Blender-written render heights and tile export metadata. Eight implementation Python files parsed, reproduction verifier executed, staged whitespace checks passed. Core GLB/recipe/vehicle module and six photographs are byte-identical to revision 04; all mapped footprints/heights, roads and bounds preserved. Font-license whitespace normalized while retaining the complete text; source/runtime notices match.
**Unresolved issues:** The user's full 1:1 objective remains open. Of 200 supported non-core names, 178 still have estimated designs; all 641 non-core street frontages are listed in `digital-twin-coverage.json`. Current photo coverage, exact dimensions/material samples/artwork, secondary elevations and small details remain incomplete. Some review views are partly occluded. The browser disabled ambient occlusion through its existing quality adjustment; no frame-rate benchmark was performed. Older image dates do not establish current occupancy or outdoor configurations.
**Next action:** Continue First Avenue/East 7th toward St Marks using the coverage inventory and dated head-on/oblique photographs. Record measurements and exact sign/material artwork where available, expand the explicit schedules, rebuild affected sections and compare equivalent real/game views. Read the current publishing request before any push/deployment.

## 2026-09-08-02 — Observed storefronts and nine sections exported; validation in progress

**Recorded:** 2026-09-08T17:02:43-04:00 (America/New_York).
**User objective and decisions:** Full neighborhood fidelity down to outdoor furniture, neon/signs, boards, materials and building details; start at First & 7th. Keep the core. No publishing or migration request.
**Completed work:** 22 individually authored storefront designs, 26 elevation schedules, 29 source records, nine rebuilt GLBs. Corrected duplicate Ralph’s and misplaced/duplicate Danny & Coop’s identities (210 named places). Added portable OFL script font, credits, source signatures and walking collision for ten photographed furniture/board objects. Details/limits in `model-source/STOREFRONT-PASS-05.md`.
**Gameplay/source baseline:** `835ea6cb53f7b88ebc0edc9586080f9c371b9d20` on `main`; initial documentation HEAD `5753989`.
**Local changes:** All new work remains uncommitted; affected paths include runtime modules, model/source manifests, scripts, fonts/notices, nine neighborhood GLBs and documentation. Actual review tool is checked into `scripts/review-storefronts.mjs`; screenshots in ignored `renders/` are not the only resume record.
**Remote state:** Not pushed; remote not fetched.
**Deployment state:** Not deployed; current live state not checked. September 6 verification of `835ea6c` remains historical.
**Validation:** Python files parse; initial actual-browser start, northbound driving and resets passed with zero uncaught errors/failed responses. Nine Blender exports succeeded. Blender initially crashed before script execution in sandbox graphics-device initialization; escalation succeeded. Final `npm run verify` and actual-browser review pending.
**Unresolved issues:** Visually inspect final exports and correct any clipping/placement issues. Reproduction and preservation checks pending. Full 1:1 remains unestablished: 22 detailed shops do not cover the map; exact measurements, many current photos/artwork and secondary elevations remain missing.
**Next action:** Read final validation output, inspect browser captures, fix failures, then update the checkpoint with actual results and publishing state.

## 2026-09-08-01 — First & 7th start; storefront fidelity work begun

**Recorded:** 2026-09-08T16:40:55-04:00 (America/New_York).
**User objective and decisions:** Start at First Avenue/East 7th. Improve businesses and buildings throughout the existing map toward minute real-world detail, including outdoor seating, neon, boards, paint, proportions and architecture. Explain whether Blender or an engine is appropriate. Preserve the accepted First & 10th core; no deployment or migration requested.
**Completed work:** Inspected clean checkout and prior accuracy sources. Edited start/reset to derive the First & 7th location from the map in both modes; added map shortcut and matching control text.
**Gameplay/source baseline:** `835ea6cb53f7b88ebc0edc9586080f9c371b9d20` on `main`; documentation HEAD `5753989`.
**Local changes:** `viewer.js`, `neighborhood-world.js`, `neighborhood-map.js`, `dist/index.html`, `START-HERE.md` and checkpoints uncommitted; storefront research/geometry work in progress.
**Remote state:** Not pushed; remote not fetched. Cached `origin/main` matches session-start HEAD.
**Deployment state:** Not deployed. Previous live revision `835ea6c` was verified September 6; not rechecked today.
**Validation:** Git/context inspection only. Local preview setup pending sandbox escalation; `npm run verify` and browser review pending.
**Unresolved issues:** Generic shop templates omit details already recorded in photographic notes. A complete dated street-level survey and measured dimensions are not available; full 1:1 fidelity remains unverified.
**Next action:** Complete photo inspection and implement explicit shop/frontage detail records, then rebuild affected sections and review exported game assets.

## 2026-09-06-01 — Revision 04 published; session continuity established

**Recorded:** September 6, 2026, 22:52 EDT (`2026-09-06T22:52:44-04:00`). This first entry summarizes the completed work leading into the checkpoint; it does not invent boundaries for earlier sessions.

**User objective and decisions:** Improve the realism of the entire existing East Village map, preserve the accepted First Avenue/East 10th Street core, publish the complete latest version to `main` and Vercel, and preserve enough context to resume after closing a session. Blue & Gold was an example of map-wide fidelity problems. The user chose GitHub owner `rayidali` and MIT for original contributions; third-party terms remain in their notices. No new geographic expansion or further feature was selected.

**Completed work:** Published all fourteen rebuilt neighborhood sections, restored five missing buildings, added the facade/business evidence and corrections, updated street facilities and map place/address search, and included the reproducible recipes and README screenshots. The active map has 615 building objects, 410 photo-observed non-core building records and 212 supported named places. Added the Vercel static hosting configuration and a public play link. This checkpoint adds the current-state summary, session log/template and agent instructions for keeping both updated.

**Code and publishing state:**

| Milestone | Commit | Result |
| --- | --- | --- |
| Initial public repository | [`e44c343`](https://github.com/rayidali/borough-drive/commit/e44c3431faff77acac14fdaad8d4d6c959ea2ddc) | Original exported map and open-source repository setup |
| Vercel 404 correction | [`0ed0d53`](https://github.com/rayidali/borough-drive/commit/0ed0d53ed1acea382282c601fc9685f34be0b69f) | Served `dist/` at `/`; map still matched the initial public version |
| Complete neighborhood accuracy revision 04 | [`835ea6c`](https://github.com/rayidali/borough-drive/commit/835ea6cb53f7b88ebc0edc9586080f9c371b9d20) | Pushed to `main` and `origin/main`; Vercel deployment completed successfully |

**Production verification:** [borough-drive.vercel.app](https://borough-drive.vercel.app) served the latest homepage. SHA-256 comparisons matched all 35 changed game files, including the fourteen rebuilt section GLBs, against `835ea6c`. The live manifest reported revision `04`, 615 buildings, 410 observed non-core buildings, 212 named places and the `blue_gold` ground profile. The successful Vercel status for this gameplay commit was rechecked while preparing this checkpoint.

**Validation and limits:** Local `npm run verify` passed before publication, including 2,308 road samples, model/texture references, vehicle/navigation invariants, restored buildings, courtyard collision and business partitions. GitHub Actions passed on Node.js 22 and 24. All eight changed Python files parsed, and the final staged diff passed whitespace checks. Earlier local browser review, source reproduction and performance observations are recorded in [the accuracy audit](model-source/ACCURACY-PASS-04.md) and [its review record](model-source/accuracy-review-2026-09-06.json). The deployment comparison establishes file identity; it is not a new visual or frame-rate assessment. This handoff task changes documentation only, so it does not require another model or vehicle test run.

**Local work and blockers:** Gameplay work was fully committed and pushed; the working tree was clean before the checkpoint documentation edits. No unfinished feature, pending model rebuild or known blocker remains. The checkpoint documents are saved in their own Git commit; use the command above to identify it. Local servers and browser processes are not required to recover the project.

**Known limitations:** This remains an uneven reconstruction, with 142 non-core objects having mapped frontages but no individual photographic observation. Unseen geometry, several dimensions, shop partitions, interiors and street dressing remain estimates. Current business evidence is dated September 6, 2026 and photographs may be older. Preserve these distinctions and all original asset credits. Package version `0.4.0` and the page's chapter label are insufficient to identify which map was deployed.

**Next action:** Read the current handoff, inspect the actual Git state, and continue with the user's next request from revision 04. Use `npm run dev` for local review. If the next request concerns accuracy, start from the audit's unresolved coverage and dated evidence. Existing exports are included; do not rebuild the complete neighborhood merely to reopen it.

## Template for the next checkpoint

Add the new entry above the latest checkpoint, update the current-state section of `CODEX-HANDOFF.md`, and replace every placeholder with an observed value, `none`, `not checked`, or `pending` as appropriate. Keep the entry concise and link detailed reports instead of copying them. A documentation-only follow-up can retain the same gameplay commit; its own revision is found through Git history.

```markdown
## YYYY-MM-DD-NN — Concrete milestone or stopping point

**Recorded:** Date, time and time zone.
**User objective and decisions:** Scope, accepted preferences and publishing instructions.
**Completed work:** Changes and relevant files or reports.
**Gameplay/source baseline:** Full commit SHA and branch; identify any later uncommitted work separately.
**Local changes:** Modified/untracked files, unfinished work and necessary artifacts.
**Remote state:** Which commit was pushed, to which branch; or not pushed/not checked.
**Deployment state:** URL and exact commit verified; pending/not deployed/not checked when applicable.
**Validation:** Commands, results and the commit/files tested; distinguish earlier evidence from new checks.
**Unresolved issues:** Failures, uncertainty, blockers and any pending user answer.
**Next action:** The first concrete step and enough context to continue safely.
```
