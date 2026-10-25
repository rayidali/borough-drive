# East Tenth: Second Avenue–First Avenue, both sides

<!-- current-project-status -->
> **Current status:** The [project handoff](../CODEX-HANDOFF.md) governs current scope, publication and next work. This file retains its dated observations, evidence or specialist instructions. See [browser scaling](../docs/BROWSER-SCALING.md) for the current loading/rendering work; older model counts and paused states describe their original checkpoints.
<!-- /current-project-status -->

**Assignment close, October 25:** All three assigned blocks are now complete locally. This report preserves its block-specific build/review boundary; the [latest Eleventh report](EAST-VILLAGE-E11-BLOCK.md) and [current handoff](../CODEX-HANDOFF.md) record final integrated state. Earlier continuation instructions below are historical.

## October 25, 2026 — Complete locally; continuing the two assigned blocks

Tenth Second–First now has **29 individually reviewed planes / 27 new building owners**, 667 scheduled openings, 28 residential/access entries and 22 shopfront/return records. The source ledger contains 97 inspected dated views. All 295 preceding authored/compiled pairs remain byte-identical. The separately reused protected core adds 23 physical building owners plus one shared-detail scene without reconstructing protected facades: **322 ordinary models, 345 physical buildings, 346 runtime scenes**.

The final served candidate is `2026-10-25T05:30:04.052Z` (366 runtime files). [Validation](east-village-e10-block/validation.json) records exact bytes and checks. [Review continuity](east-village-e10-block/review-continuity.json) links 198 inspected views to unchanged final compiled-scene hashes; all 29 planes have an inspected elevation and both mass obliques. Individual shop closeups/obliques and repair decisions are recorded in the versioned review notes. Full ground crops supplement long-storefront spans. Three of 21 gameplay images were visually inspected; the other captures are not claimed as inspected.

Repairs include missing escapes/window rows, grouped sash openings, carved and arched masonry, 204’s real upper notch/construction net, individual shop signage/shutters/curtains/seating, and visible basement wells. The final two-shop pass corrects Shabu-Tatsu’s projecting tilted plaque and closes shallow display recesses at Rai Rai Ken and Shabu-Tatsu. Protected core views retain the original appearance and texture provenance. The road uses uninterrupted coplanar collision rectangles; earlier failed seam/raised-plane/grid repairs remain in the diagnostic evidence. The final Second-facing pavement supports both assigned corner returns without opening Second Avenue.

`npm run verify` passes on candidate06; original-game source stayed unchanged afterward. Final `npm run seventh:verify` passes all runtime/source hashes and 295-model preservation. Candidate06 browser integration passes eight driving routes, eight boundaries, four camera modes with orbit/pan/zoom/reset and owner checks, with zero console errors/failed requests. Candidate09 native tests pass eight routes; its weather drives pass with no contacts or streaming holds. Seventeen address cases pass, retaining the Seventh-only address HUD. Later changes are limited to two shops’ sign/recess geometry; controls, road surfaces and streaming limits match the measured candidate09.

On this Apple M4 Max, Brave at 1440×1000, local HTTP, five cache-disabled startup runs have median **11.764 s** (11.626–12.149); five cache-enabled runs have median **11.789 s** (11.573–12.580). This is browser cache control, not OS/GPU cold start. All 346 scenes initially load. Twelve weather/route samples report 118.4–120.0 engine fps and 8.5–9.9 ms RAF p95. Two Seventh east runs have **116.6/116.7 ms isolated frame gaps**, cause unresolved. Tenth samples have 10.2–16.6 ms maxima. These measurements precede the final sign/recess-only corrections; they are not a final-byte retest or proof of slower-device/CDN performance. Detailed raw intervals and conditions remain in `performance-09` and `startups-09`.

Limits: imagery is dated and does not establish October 2026 occupancy. The closed 214, east 220 and shuttered 204 unit identities remain unresolved. Fine artwork, lettering and decorative carving are authored approximations; broad sash counts at 225–227 and foliage-interrupted 233–235, and portions of 206’s lower carving, retain evidence limits. Basement model/native checks show five descending treads and no covering pavement, but steps have low contrast in shadow. No calibrated 1:1 acceptance is claimed.

Main/live remain the verified **295-model `e1155e5` release**. This completed block is local/uncommitted. Continue **Tenth First–Avenue A (`01-E10-1A`)**, then **Eleventh Second–First (`01-E11-21`)**, both complete blocks, under the existing user authorization. Preserve all preceding model bytes, `.godot/`, `.tools/`, original game and private screenshots/workspace. Preview: north on First, left on Tenth.

The dated candidate/preparation sections below are history.


## October 25, 2026 — First Tenth browser candidate reviewed; targeted repairs in progress

The three-block assignment remains active: Tenth Second–First, Tenth First–Avenue A, then Eleventh Second–First. Main/live remain the verified 295-model release `e1155e5`; all new work is local/uncommitted.

First Tenth candidate `2026-10-25T04:13:31.350Z` built and passed export verification (366 runtime files, 177 source hashes). All 295 prior authored/compiled pairs remain byte-identical. Runtime has 322 ordinary models plus 23 protected core buildings and one shared-detail scene: 345 physical buildings / 346 model scenes. The isolated core geometry/material/ownership proof also passes. This does not establish browser performance.

The source ledger now records 97 inspected dated views. First-candidate visual review has inspected 65 captures, including one unusable core-theater camera now corrected in the harness. Review found missing 205/209 escapes, 205's fifth upper row, incorrect 237/204 window grouping, missing ground arches/carved relief, stretched lettering, concealed shutter tags, and basement shop access. Repairs are authored and the 27 affected models are re-exporting; 667 scheduled openings / 28 entries / 22 shopfront records. No repair has been awarded served acceptance yet. The 204 upper notch is visibly open in both inspected obliques. Core approach views are inspected, with the theater replacement and broader visual coverage still pending.

Next: finish the second export/build; complete per-face, per-shop and oblique review/repair; run driving, boundary, camera/reset, address and startup/performance checks. Then continue both remaining assigned blocks. No routine stage approval is needed. Preserve `.godot/`, `.tools/`, previous model bytes and private screenshots/workspace.

**October 25 implementation in progress:** 29 planes /27 new owners are authored with 661 scheduled openings, 28 entrances and 22 shopfronts, based on 91 individually inspected dated views. First full export: 322 ordinary models, all 295 prior GLBs/SCNs unchanged. No served facade acceptance or browser integration pass yet. Four architecture count/occlusion limits and unresolved tenant identities remain in the schedule/observations.

Protected-core conversion and isolated runtime ownership/material checks pass: 521 meshes /424,497 triangles, 23 colliding building owners and one non-colliding detail owner. [Proof](east-village-e10-block/core-ownership-proof.json). Nine original encoded texture images share one 11.84 MB library; exact source pixels/mipmap state survive runtime rebinding. Failed initial external-texture bundling and duplicate-image packaging were diagnosed before player export. No new reference imagery becomes game texture. See [Godot embedded-image semantics](https://docs.godotengine.org/en/latest/classes/class_gltfstate.html) and [reproducible conversion](export_protected_core.py). Shared PCK allowance is now 24 MiB; 8 MiB ordinary scene /32 MiB aggregate staging remain, with a 16 MiB per-owner exception for the 14.79 MB 204 corner. Recompression did not reduce that already-compressed scene. Browser loading/performance remains unmeasured for this candidate.

The following October 24 preparation is historical; the newest handoff and progress JSON govern current implementation. Full rendered facade/core comparison, repairs, street checks and performance remain before this block is complete; the two authorized successor blocks follow.

**October 24, 2026 — assigned, ownership preparation in progress.** The user requested publishing the latest existing work and continuing the agreed East Village plan. This is the next full-block implementation, not a new publication request for its later result.

The initial mapped inventory has **27 new building owners / 29 editable street faces**: 27 Tenth primary faces plus the two same-building Second Avenue returns. **Six Tenth planes on four accepted core buildings remain protected.** All 295 current model/compiled-scene pairs and both private screenshots match their frozen baselines.

## Exact ownership

| Face | Mapped address | Role |
| --- | --- | --- |
| `247851894:0` | 205 East 10th Street | assigned-primary |
| `247851895:0` | 209 East 10th Street | assigned-primary |
| `247851896:0` | 211 East 10th Street | assigned-primary |
| `247851897:0` | 213 East 10th Street | assigned-primary |
| `247851898:0` | 215 East 10th Street | assigned-primary |
| `247851899:0` | 217 East 10th Street | assigned-primary |
| `247851900:0` | 219 East 10th Street | assigned-primary |
| `247851901:0` | 221 East 10th Street | assigned-primary |
| `247851902:0` | 223 East 10th Street | assigned-primary |
| `247851903:0` | 225 East 10th Street | assigned-primary |
| `247851904:0` | 229 East 10th Street | assigned-primary |
| `247851906:0` | 231 East 10th Street | assigned-primary |
| `247851908:0` | 233-235 East 10th Street | assigned-primary |
| `247851911:0` | 237 East 10th Street | assigned-primary |
| `247851935:0` | 160 2nd Avenue | assigned-primary |
| `247852656:0` | 206 East 10th Street | assigned-primary |
| `247852658:0` | 208 East 10th Street | assigned-primary |
| `247852659:0` | 210 East 10th Street | assigned-primary |
| `247852660:0` | 212 East 10th Street | assigned-primary |
| `247852662:0` | 214 East 10th Street | assigned-primary |
| `247852663:0` | 220 East 10th Street | assigned-primary |
| `247852664:0` | 222 East 10th Street | assigned-primary |
| `247852665:0` | 224 East 10th Street | assigned-primary |
| `247852667:0` | 226 East 10th Street | assigned-primary |
| `247852668:0` | 228 East 10th Street | assigned-primary |
| `247852693:1` | 204 East 10th Street | assigned-primary |
| `247852694:0` | 216 East 10th Street | assigned-primary |
| `247851935:1` | 160 2nd Avenue | same-building-corner-return |
| `247852693:0` | 204 East 10th Street | same-building-corner-return |

The following primary faces are already authored in the original protected core and are not assigned for reconstruction:

| Face | Mapped address |
| --- | --- |
| `247851912:0` | 239 East 10th Street |
| `247851944:1` | 163 1st Avenue |
| `247852692:0` | 242 East 10th Street |
| `247852695:1` | 155 1st Avenue |
| `247852695:2` | 155 1st Avenue |
| `247852695:3` | 155 1st Avenue |

## Supporting runtime work

The current Godot exporter excludes all `core` buildings. Therefore preservation of the original First/Tenth GLB alone is insufficient to display the protected eastern end of this new block. The adapter must reuse the accepted source geometry and preserve its individual face/mass ownership; it must not rebuild protected facades using the ordinary new-building recipe. A read-only Blender audit decoded all 590 source meshes: 23 named building owners and 78 shared architectural/street meshes. The original GLB remains byte-identical. Shared-detail ownership still needs a precise integration audit. See [source audit](east-village-e10-block/core-source-audit.json) and its [reproducible script](east-village-e10-block/audit_core.py).

Keep the original core GLB and recipe unchanged. Establish exact imported geometry/material evidence and a single owner for each rendered core building/collision before opening Tenth. Record any context needed on the First Avenue connection as preserved/supporting context, not newly reviewed facade work.

The [candidate adapter contract](east-village-e10-block/core-adapter-contract.json) retains 512 named building meshes and all nine shared architectural-detail meshes (424,497 triangles total). Those shared details include corner address lettering and hardware; their material batches span several buildings. A separate protected, non-colliding detail owner avoids cutting or assigning the batches from their aggregate bounds. The remaining 69 source meshes contain street surfaces and illustrative dressing and need a separate overlap audit. This contract is preparation only; conversion, material preservation, collision ownership and matched-view review remain unproven.

First Avenue currently stops at runtime z = −166; Tenth is centered near z = −228 in the same frame. Derive the connection and Tenth road/sidewalk bounds from the exact assigned geometry. Keep the separate Second Avenue block and Tenth east of First closed. Retain the Seventh-only address HUD and unchanged UI/audio/handling.

## Evidence and next action

No fresh Tenth source images have been inspected and no new models have been authored. The inventory contains dated mapped business leads and candidate Maps locators only. Inspect full elevations, both obliques, each entrance/storefront and every neighbor junction, then transcribe the individual feature schedules before modeling. Preserve the real setbacks and protected 239/Tenth edge. Mixed imagery dates and unresolved tenants must remain explicit.

[Inventory](east-village-e10-block/inventory.json) · [Baseline](east-village-e10-block/baseline.json) · [Protected models](east-village-e10-block/protected-models.json) · [Current progress](east-village-e10-block/progress.json).

Complete the whole assigned block after the publication/permission setup is resolved. Internal facade groups are working units, not stopping points or claims that the block is complete.
