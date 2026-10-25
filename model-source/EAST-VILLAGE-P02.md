# P02 — 138–148 First Avenue

**October 13, 2026 — complete locally; awaiting user review.** Five east-side First Avenue faces and five businesses are implemented between St. Marks and Ninth. The user's stronger attention to gaps, shape differences and texture is now part of the reconstruction skill and its work packet. P03, the 145 First / southwest Ninth corner, is next on the next instruction. No publication is requested.

All 207 preceding GLBs and compiled scenes are byte-identical. P02 brings the slice to 212 models; all load initially, with 12 west-context scenes releasable and 200 pinned. First Avenue's existing terminal at −145 / outer cap −150 is sufficient; other avenue terminals stay −119 and Ninth remains closed. Original game, interface/audio/controls and both private untracked screenshots are preserved.

## Buildings and individual shops

| Face / address | Modeled and inspected details |
| --- | --- |
| `248142657:0` / 138 | Low three-story dark brick mass; six upper windows, keyed white lintels, dentil course and dark bracketed cornice. East Village Wines has a folded ivory sign with lettering on both planes, burgundy fascia, projecting lights, copper mesh, recessed shop leaf, bottle display/poster, cartons and wood board. Separate cream security-grille residence entrance. |
| `248142658:0` / 140 | Nine upper windows, faded pink brick, salmon cornice and escape spanning two bays. Area 140 First has a shallow olive BAR shade, string bulbs, circular window mark, rainbow OPEN, green leaf with one long pull, four folding chairs, red wire stool and dark mat. Separate north residence with frosted panels, steps, light and intercom. |
| `248142659:0` / 142 | Nine upper windows with dark lintels; wide escape platforms with narrower observed stair runs. Cosmos Launderama has red condensed lettering and stars on white fascia, folded gray canopy, silver rail, washer drums and an open glass leaf with its handle. Separate brown numbered entry, ribbed glass and low louver. |
| `248142660:0` / 144 | Six upper windows, bracketed cornice, wide lower escape platforms and narrow top landing. Separate WASH & DRY and green serif Cosmos Dry Cleaners signs, thin silver framing, brown lower door panel, ATM screen/keypad/notice and independent north residence. |
| `248142713:0` / mapped 148, municipal 146 | Irregular footprint with cream stucco, twelve upper windows, shallow parapet notch/railing, northern escape centered on the second bay and a separate southern escape with a narrow top landing. Lime Tree Market's First face has a projecting glazed enclosure, unequal panes, off-center entry, red lower panels, burgundy sloping canopy with correctly oriented lettering on top and valance, plus dated poster/shelf cues. Its Ninth return is deferred; no generic return shop is invented. |

The [five junction records](east-village-p02/schedule.json) distinguish touching party walls from the **0.503 m mapped setback at 144/148**, which leaves a short exposed return. There is no observed open alley between these five properties. The lower 138 roof exposes the protected southern neighbor's wall; heights, cornices and material transitions remain distinct. Footprints and height inputs are inherited municipal/mapped data, not new survey measurements. Visible trim, stair, enclosure and fixture dimensions are estimated from images.

Two differently sized trees, the open square tree guard, M15 bus-stop pole/pictogram and notice-covered utility cylinder follow dated observations. Shader changes apply only to these five models: differentiated brick scale/bond, faded brick at 140 and stained stucco at 148. Earlier model materials follow their unchanged path. Seasonal foliage and movable fittings reflect the reference condition.

## Sources, review and limits

The [observation ledger](east-village-p02/observations.json) retains nine named source inspections/reinspections, full ordinary-browser Street View locators and separate identity links. April 2026 is the ground-floor target; September 2024 north-block views provide clearer upper detail. Official [Area 140 First](https://www.area140first.com/contact) and [East Village Wines](https://eastvillagewines.com/info) pages support address/identity. They do not replace facade observation. No source photographic pixels are distributed or used as textures. These dates do not establish unchanged October 2026 occupancy.

All **50 final detail images** were inspected: five elevations, ten overlapping ground views, eighteen shop views, ten massing obliques, one complete market frontage, three protected neighbors and three weather views. All **13 gameplay images** were also inspected. [Per-image hashes, per-face findings and junction review](east-village-p02/visual-review.json) identify the final package. Authoring schedules retain their initial review labels; the separate final review resolves those states without silently changing recipe hashes. Trial captures are retained separately and are not relabeled as final evidence.

Actual repairs included culled lintel faces, buried cornice brackets, camera framing, the open laundry leaf/handle, narrow stair runs and the market's two distinct escape layouts, awning lettering tangent, a duplicate bar-door pull, the parapet coping notch and bus-stop pictogram/order. Four model exports and five engine builds are recorded in the packet. The shared exporter initially required a full rebuild; all 207 earlier model bytes still matched. Later recipe passes exported only five assigned IDs.

Exact logo artwork/letterforms, tiny poster and carton copy, merchandise, measured dimensions and source-occluded features remain approximate. Hidden rear/interior/roof equipment is unknown. The storefront's partially obscured central glazing is interpreted within the recorded source limits. This is a complete bounded implementation and visual review, not calibrated 1:1 acceptance or a numerical “×50” improvement.

## Reproduce and verify

`author_p02.py` generates the independent schedule; `p02_kit.py` consumes it after the existing kits. Do not rerun revision 08/09 or P01 authors to add P02. After P02-only recipe edits:

```sh
blender -b -t 4 --python-exit-code 1 --python model-source/export_seventh_engine.py -- --only 248142657 --only 248142658 --only 248142659 --only 248142660 --only 248142713
npm run seventh:build
npm run seventh:verify
npm run verify
node scripts/review-p02.mjs model-source/east-village-p02/new-review
node scripts/review-p02.mjs model-source/east-village-p02/new-routes routes
```

Use the local server and isolated review browser on port 9222; `BOROUGH_REVIEW_URL` selects the current server. P01 and P02 ownership stays in `packetScopes`; nine packet review faces remain separate from the old 102 street / 82 Seventh lists. A full shared-recipe change still requires full export and preservation comparison.

Final shared PCK: **8,006,792 bytes**, SHA256 `476e38b45cd92fff235cb56e17c8c92506d3949959a002d88e0b26e49d07f288`. The build verifies 231 required runtime files and 127 source hashes; all runtime files total 149,564,786 bytes. External building scenes are required game assets. [Preservation](east-village-p02/preservation.json) verifies the preceding 207 GLBs/SCNs, 2,376 other tracked non-Markdown files, prior recipes and both unchanged/untracked private screenshots against the P02-start snapshot.

Four real-key routes pass with zero contacts or loading holds; four held-throttle boundaries, four orbit/zoom camera modes, reset and all five new model/collision owners pass. Seventeen original address cases pass, with the Seventh-only HUD hidden on P02. The initial side-cap fixture stopped at the new market collider, before reaching the cap; moving it north of that building fixed the test without changing the runtime. Both reports are retained. Original/package verifications and four exact localhost route hashes pass. [Validation](east-village-p02/validation.json).

Five cold starts: median **7.831 s**, p95 **8.299 s**. Five cache-enabled starts: **9.457 s / 21.687 s**; every warm run has 212 scene cache hits. The 21.7-second warm outlier remains unattributed. P01's historical medians were 6.598/8.965 s; these are not a fresh alternating control. Route frame intervals have p95 18.6 ms and maximum 48.1 ms. Five-run p95 is the maximum; browser-cold does not reset OS/GPU/WASM caches. [Raw metrics and limits](east-village-p02/metrics.json). No startup-speed improvement, total-memory or full-East-Village scalability claim.

## Timing and next session

P02 elapsed **about 74 minutes** through the final handoff, recorded in [progress](east-village-p02/progress.json). It includes research, authoring, repeated source inspection, repairs/exports, final visual/browser checks and documentation, with no parallel agent work. P01 took about 78 minutes. Keep the provisional whole-area forecast of 390–725 sessions / 300–1,100+ model/tool hours until the planned P03 timing checkpoint.

Next is **P03: 145 First Avenue / southwest Ninth corner**, faces `241822237:1` and `241822237:0`, on the next user instruction. Preserve all 212 current models. Observe both assigned street faces and assess the supporting boundary adapter; this does not automatically authorize opening the whole of Ninth or the 148 Ninth return.

Checkout and cached origin remain `a2a90a3e08540e15f40e0ede0f8af14921f54675`; published architecture remains `0de4b54dc9d0e711f11962688f0e6fca3aa01c50`. All roadmap/EV-000–003/P01/P02 work remains local and uncommitted. No fetch, commit, push, CI, deployment, paid imagery or fresh production check occurred. Preview at `http://127.0.0.1:5181/`, or restart with `npm run dev`. Use Git history for the eventual checkpoint save commit.
