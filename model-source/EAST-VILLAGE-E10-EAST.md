# East Tenth, First Avenue–Avenue A — October 25, 2026

<!-- current-project-status -->
> **Current status:** The [project handoff](../CODEX-HANDOFF.md) governs current scope, publication and next work. This file retains its dated observations, evidence or specialist instructions. See [browser scaling](../docs/BROWSER-SCALING.md) for the current loading/rendering work; older model counts and paused states describe their original checkpoints.
<!-- /current-project-status -->

**Assignment close, October 25:** All three assigned blocks are now complete locally. This report preserves its block-specific build/review boundary; the [latest Eleventh report](EAST-VILLAGE-E11-BLOCK.md) and [current handoff](../CODEX-HANDOFF.md) record final integrated state. Earlier continuation instructions below are historical.

The second block of the authorized three-block assignment is complete locally. Both sides have **36 reviewed facade planes / 30 new owners**, with **619 scheduled openings, 37 entries and 26 shopfront/community records**. Final candidate: `2026-10-25T07:57:01.795Z`. The local game now contains 352 ordinary models plus 23 protected core building owners and one shared-detail scene: **375 buildings / 376 scenes**. New block work remains uncommitted; main/origin/live remain the verified 295-model release `e1155e58e6084052b592c291a4cabd67281a3b21`.

Continue the assigned third block, **Eleventh Second–First (`01-E11-21`), both sides**. No stage permission is needed. Its 26-plane/22-owner inventory is prepared; source inspection and implementation follow this checkpoint.

## Geometry and individual detail

[Schedule](east-village-e10-east/schedule.json), [observations](east-village-e10-east/observations.json), [junction review](east-village-e10-east/junction-massing.json) and [per-face/business review](east-village-e10-east/face-review.json) retain the exact scope and source links. Distinct access, cellar wells, flaking base paint, lintels, cornices, fire escapes, paired 280 escapes and church/club roof steps are modeled. The church has separate low wing, nave, recessed porch, tower and rectory masses; its Avenue windows are cut through the correct wall, with connected roof planes, dormers, carving, leadwork and raised entrance. Concealed roof depths remain estimates.

Shop review includes each business within shared facades. Examples include Le Phin’s filters and illustrated board, Kavasutra’s striped pitch and bench, Live Live’s pale blue wood and bottles, Lucie’s pink curtain and bistro furniture, niconeco’s book wreath and globe lights, Eastside Story’s classical framing, Whistle’s lattice bench, Bleach’s discs and colored lettering, the alteration shop’s black door, Clash’s outlined lower lettering, distinct vacant units, Crops’ curtains, the dog-wash emblem and bench, Body Evolutions’ grid and canopy, four separate 280 units, and the laundromat’s curved canopy, service line, clothes and mismatched chairs. The Baths and Church of Christ have separately reviewed entry compositions.

## Review and repairs

Actual inspections: **169 candidate03 + 126 candidate04 + 119 candidate05 + 15 candidate06 images**. These are inspection records, not all captured images and not an accuracy score. [Continuity](east-village-e10-east/review-continuity.json) connects inspected filenames to package hashes. Every business has inspected front and both oblique views matching its final compiled scene. All 29 ordinary non-church owners are byte-identical between candidate05 and final06. The final church change adds attic relief and roof-edge trim, inspected in front and both obliques; earlier church access reviews remain explicitly tied to their candidate.

Repairs addressed unsupported address labels, lettering hidden by glass/trim, generic or incorrect door paint, curtains, display heights, sign depth, grille construction, furniture, a clipped lease poster, stair contrast, and a duplicate church side wall that concealed Avenue windows. Initial failed exports are retained. Building 280 initially exceeded its 8 MiB scene allowance; removing hidden backs from attached carved relief preserved its visible outline and reduced it to 8,171,295 bytes. It received no new size exception. The church uses its measured 16 MiB allowance; final scene is 8,792,090 bytes.

## Integration, preservation and performance

[Validation](east-village-e10-east/validation.json) records exact build boundaries and raw evidence. Original-game and export verification pass: **396 runtime files / 184 source hashes**. All **322 preceding ordinary GLB/SCN pairs**, **24 protected core scenes**, original-game baseline files and both private screenshots remain byte-identical. The protected-core package reuses frozen reviewed scenes and validates their source/texture hashes; it does not reserialize the accepted core during ordinary block exports. Preserve the Godot cache and local tools.

Candidate05 passes eight native routes and eight browser routes, including both full Tenth directions, eight boundaries, four camera modes/reset and new/protected model ownership checks. No new collision or loading hold occurred. Three of its 21 gameplay images were inspected. Candidate06 changes non-colliding church ornament only; these route tests were not repeated. Final06 passes all 17 address cases; address display remains scoped to the existing Seventh segment.

Final06 measurements on the local M4 Max, unthrottled, 1440×1000: 15 driving samples across three weather states measured **117.23–120.02 engine fps**, RAF p95 **8.8–9.9 ms**, largest sampled gap **25.3 ms**, with no console errors or failed requests. Five cold startups had median **12.661 s**; five warm startups **12.756 s**. “Cold” disables the browser cache, not OS/GPU caches. All 376 scenes initially load; these results do not prove remote-network or low-powered-device performance.

## Evidence limits

References include September 2024 / July 2022 views, June 2014 architecture supplements and a 2022 Le Phin supplement. They do not establish universal 2026 occupancy. Tenant identities remain unresolved at the green porthole unit at 265, closed east unit at 271, shingled east unit at 273, and dark west unit at 280. Photographed vacancies remain vacancies in this dated reconstruction.

Fine logos, graffiti, sculpture, product labels and letterforms are authored approximations. Trees and dining frames obscure some road views; adjacent or inside-frame views were inspected separately. Rear roofs, exact depths and some cellar geometry remain estimated. The 276 cellar door is approximately central/right with an adjacent low window; source perspective does not establish surveyed dimensions. No calibrated 1:1 photographic acceptance is claimed. Source pixels remain private under `.tools/`, separate from distributable game captures.

Preview: `http://127.0.0.1:5181/` — north on First, right onto Tenth.
