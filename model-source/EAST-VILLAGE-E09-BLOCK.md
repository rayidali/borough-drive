# East Ninth, Second–First: full block delivery

<!-- current-project-status -->
> **Current status:** The [project handoff](../CODEX-HANDOFF.md) governs current scope, publication and next work. This file retains its dated observations, evidence or specialist instructions. See [browser scaling](../docs/BROWSER-SCALING.md) for the current loading/rendering work; older model counts and paused states describe their original checkpoints.
<!-- /current-project-status -->

October 14, 2026. Completed local geographic pass with recorded source limitations. No publication.

The user requested more progress per session without reducing quality, then reported another laptop shutdown. This session implements all **34 remaining faces** of `01-E09-21`, across N02A/N02B/N03/S01/S02/S03 as internal groups. The eight completed Ninth faces and separate P03 corner return are preserved, along with every other preceding model. There are now **255 models**, up from 221. This is complete geographic coverage of the assigned block, with the source uncertainties below still open; it is not calibrated photographic acceptance.

## Scope and distinctive work

The new north side runs 331–303 Ninth, including the 146 Second return; the south side runs 350 Ninth to Veselka's Ninth frontage at 144 Second. The [inventory](east-village-e09-block/inventory.json), [schedule](east-village-e09-block/schedule.json), [observations](east-village-e09-block/observations.json) and [face/business review](east-village-e09-block/face-review.json) preserve exact ownership and evidence.

- 34 individually scheduled elevations, 572 upper/ground architectural window openings, 33 residential/access doors and 34 shopfronts. Glass divisions within shops are additional geometry, not extra businesses.
- Distinct tenement bands, cornices, pediments, sash rhythms, escapes and equipment; 327's light stone/garage composition, 319's construction net and boards, 336's shallow carriage-house cap and diamond frieze, and the paired terracotta arches of 328/324.
- Basement wells cut the ground and retain stairs/railings and clear approaches. The 305/303 junction has a 2.657 m mapped gap, a low green street wall and open air above. 327's effective facade includes its missing 1.555 m garage edge without changing the source polygon. Hidden stair depth and decorative dimensions remain estimates.
- Separate business compositions include Source Unltd's pitched canopy and shutter artwork; Frida's retained fascia/vacancy display; March Hare's toys; Rosemary's glass lettering; Davey's multicolor sign and threshold; MUD's storefront/shelter; Pillow Cat's books; Jane's cookware; Cerney's grille/blade; Sakaya's bottle display; and Veselka's long dining frontage, grouped upper windows and shelter. These are observed, individually authored arrangements with simplified lettering/artwork, not photographic textures.
- New street dressing adds ten trees, curb details and manholes. Ninth opens west to terminal x=−213 (outer −217), center z=−154.7. North/south outer bounds remain −164/−144.3. First stays −166/−171; other avenue ends remain −119. East Ninth remains closed at x=10.75 (backup 13). MUD/Veselka shelters share their building's collision owner. The address HUD remains Seventh-only.

## Research and visual review

Forty-three source records include ordinary browser Street View, targeted repeat inspections and supplemental public/official photographs. Primary imagery is September 2024; some obstructed features use dated 2012/2016/2017/2022/2023 evidence as recorded. This is **not an October 2026 occupancy survey**. A proposed rendering for 327 was rejected as evidence of the built exterior. Reference pixels were temporary and are not distributed as game textures or assets.

The [visual ledger](east-village-e09-block/visual-review.json) distinguishes capture from actual inspection. Round 04 captured 384 views; 205 were inspected: all 34 elevations, all shop fronts/left approaches (78 views, including overlapping long-front sections), 68 mass approaches, 18 wells and seven protected neighbors. Two Veselka mass views were obstructed by the opposite building and were replaced in round 06. Round 05 inspected eight revised elevations and the 314 entry closeup. Round 06 inspected three elevations and six mass approaches. Earlier review/diagnostic images and repairs remain separate; no claim is made that every captured image was inspected.

Six repair exports address actual discrepancies: portal depth and door clearance, side-letter orientation, carriage-house frieze placement, equipment, molding and floor spacing, paired arches/bay grouping, shade/display construction, and 314's vertical numerals. [Preservation and review transfer](east-village-e09-block/preservation.json) verifies that 247 models are byte-identical to round 04 and 253 to round 05, so their unchanged geometry retains the earlier review; changed features were reviewed again.

Five shop records retain `needs-evidence`: the unresolved east shop at 321, current SHW exterior, partially obscured Raw Spirit/Art + Ray at 305, and the obscured east shop at 318. Physical frontage is represented, but dated identity or inferred display is not a verified current composition. Rice Bird's small Chinese copy, exact fonts/artwork/product packaging, hidden roofs/rears/interiors and survey dimensions remain unresolved or approximate. These limits are not erased by successful runtime checks.

## Package and validation

Build **`2026-10-14T17:30:33.776Z`**, 255 models / 274 runtime files / 151 source hashes. Shared PCK **8,096,788 bytes**, SHA256 **`56af68394e3cc27156124b0b360a99096a16dacba4220c6637abf86c2a136638`**; full required runtime **196,791,273 bytes** and 6,473,778 authored model triangles. External `dist/seventh/areas/` files are required. The partition is 12 west / 243 pinned; all 255 scenes still load initially.

[Validation](east-village-e09-block/validation.json) records `npm run verify` and `npm run seventh:verify`; 221 preceding GLB/SCN pairs and both private screenshots; six real-key driving legs without contacts/holds; seven held-throttle boundaries; four camera modes with orbit/zoom without moving the car, vehicle reset and 34 shared visual/collision owners; 17 address cases; five cache-disabled/five cache-enabled startups; eight inspected Blue hour/Passing rain material views; four served root/Seventh/legacy route hashes and all 274 served runtime file hashes. All 18 gameplay captures were inspected. Original game, UI/audio/handling sources remain unchanged from the session baseline. Close canopy/outer-sidewalk approaches can occlude the chase camera; this is not a universal no-clipping guarantee.

Two checker repairs are retained: trial01 braked too close to the terminal after a much longer acceleration run; trial02's last boundary spawn was against the newly modeled corner building. Six routes and six boundaries passed in trial02; the corrected boundary and remaining controls/ownership passed in the tail run on the identical build. The [combined gameplay report](east-village-e09-block/gameplay/captures.json) identifies both source runs. No game geometry or controls were changed to satisfy these fixtures.

[Final timing](east-village-e09-block/metrics.json): cold median/p95 **9.928/11.592 s**, warm **12.593/15.343 s**; all 255 scene responses were browser-cache hits in every warm run. The historical N01B values were 6.971/7.226 and 9.061/11.170 s. Loading is slower; this is a historical comparison, not a fresh paired before/after experiment. Route p95 is **18.6–18.7 ms** on five legs and **31.4 ms** eastbound on Ninth, with that leg's maximum **35.3 ms**. Keep this cost visible before further expansion; no storefront detail was removed for the measurements. One desktop browser/profile, local unthrottled network, sequential runs; cache-disabled does not reset OS/GPU/WASM caches. No whole-area/mobile/RAM scalability claim.

The first full-block continuation took **168.2 minutes wall elapsed**, including the reported shutdown/recovery; active work time is unmeasured. It adds 34 faces while reusing eight prior Ninth faces and the P03 corner. This is one interrupted sample, so no fixed per-block rate or revised citywide completion promise follows. Current [workflow](east-village-block-workflow.json) continues at about one assigned block per session; collect several uninterrupted samples before replacing historical packet-hour allowances.

## Save state and continuation

All work is local/uncommitted on `main`; checkout and cached origin remain `a2a90a3e08540e15f40e0ede0f8af14921f54675`. Published architecture is `0de4b54`; the previously verified revision09 release is `3457a29`. There was no fetch, commit, push, CI/deployment or production recheck. Preserve all preceding dirty work and both private screenshots. The laptop shutdown cause is unknown; saved sources survived and work resumed with two-thread exports and serialized browser/build phases.

Preview **http://127.0.0.1:5181/**; restart with `npm run dev -- 5181`. Drive north on First, then left onto Ninth. The proposed next delivery is **01-E09-1A, Ninth between First and Avenue A, both sides**, on the next user instruction. Its exact ownership/evidence must be prepared then, including the deferred 148 First Ninth return; do not begin it automatically.
