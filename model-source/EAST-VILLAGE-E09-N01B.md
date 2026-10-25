# 01-E09-21-N01B — 339–333 East Ninth

<!-- current-project-status -->
> **Current status:** The [project handoff](../CODEX-HANDOFF.md) governs current scope, publication and next work. This file retains its dated observations, evidence or specialist instructions. See [browser scaling](../docs/BROWSER-SCALING.md) for the current loading/rendering work; older model counts and paused states describe their original checkpoints.
<!-- /current-project-status -->

October 14, 2026. **Complete locally, within the dated-source and review limits below.** The user's later shutdown/recovery request resumed this same packet. Nothing was published.

The user’s “keep on going ahead” assigns four north-side Ninth faces: `247852687:0`, `247852686:0`, `247852685:0`, `247852684:0`. This is the second child of `01-E09-21-N01`, under corridor `01-E09-21`. All 217 preceding models, original game, UI/audio/handling, frozen geography and both private screenshots remain protected. Publication is not requested.

[Progress](east-village-e09-n01b/progress.json), [baseline](east-village-e09-n01b/baseline.json), [protected models](east-village-e09-n01b/protected-models.json), [observations](east-village-e09-n01b/observations.json), [schedule](east-village-e09-n01b/schedule.json).

## Source and geometry

Thirteen ordinary-browser Street View views were opened and inspected. Primary appearance is September 2024; November 2017 only supplements obscured access. Dates and locators are preserved, source pixels remain temporary references and are not game assets. This is not an October 2026 occupancy survey. The west shop at 333 has an unreadable circular script seal; its physical frontage is included without inventing a tenant name or transplanting the mapped Downtown Funk & Junk name from a later lease.

Each mapped frontage starts at geographic west and runs east; positive depth projects south toward the street. Engine z is source z minus 228, making these faces approximately z=−162.6. Heights/depths are meters; horizontal at/span values are fractions. The irregular mapped footprints remain unchanged. Touching party walls are recorded at every join, including protected 341 and deferred 331. The absence of deferred 331 is a coverage limit, not an observed alley.

337’s mapped height is 18.93 m, but its visible cornice is below both neighbors. This new engine model uses an explicitly estimated 15.9 m facade height from relative roofline observations. The municipal/source record stays unchanged. No higher hidden rear roof is invented. Other heights remain 16.70, 16.62 and 16.67 m. Fine dimensions, exact commercial fonts, relief and display artwork remain estimates; hidden roofs/rears and deep interiors remain unobserved.

## Individual feature schedule

| Face | Architectural/access distinctions | Shops and detail |
| --- | --- | --- |
| 339 | Four upper rows of four sash openings plus four parlor windows; broad cream head bands, thin sill bands, outer vents, plain brick parapet, rust four-level escape. Two basement openings, right ochre single leaf with square glass and 339 below it, caged round lamps, real low well and separate descent, four-lid refuse storage. | Residential; no invented storefront. |
| 337 | Four rows of four sash openings; taupe brick, cream flat heads, dark cornice with ladder notch, four-level black escape/scrolls. Recessed common entrance and separate three-step approach; 337 at rear door. | New Sew Good Cleaners has curved faded red canopy, condensed white name, separate side service copy, nine unequal display compartments, bags, folded goods, sewing-machine profile, papers and low AC. Wicked Heathens’ east display projects forward, with diamond grille and jewelry/clothing forms; no guessed exterior brand sign. |
| 335 | Four rows of four sash openings; red brick, lowest triangular sandstone heads, varied molded upper heads, ornate pale cornice, black escape. Center black single door, observed 335 transom, fluted/relief portal, hooded lamp and standpipes. | Fabulous Fanny’s gray cloth canopy, script name/paired 335, rectangular grille, large eyeglasses, red frame, small spectacles and busts, upper AC. Layers has no copied canopy: small brown script sign, narrow metal/glass frontage, grille, mirror/chair layers and dated lower tags. |
| 333 | Four rows of four sash openings, related but separately placed red-brick/stone/cornice architecture, black escape/drop ladder. Separate center door with patterned transom. | West shop: black inclined canopy/333 E9th, broad pane/narrow right door, circular unreadable seal, blinds, chairs and water jug. Spark Pretty: black cloth, stacked white logo/pink 333, rectangular grille, colorful clothing/torso forms and small display objects, upper AC. |

This totals 68 above-grade windows, two basement openings, six shopfronts, five identified businesses plus one unresolved tenant, and four separate residential doors. Outdoor seating is not observed in this packet. Mature/small curb trees and paired cellar plates are separately owned street fixtures.

## Supporting runtime adapter

Only west Ninth extends: center z=−154.7, visible terminal x=−99, outer limit −103; north/south outer limits remain −164/−144.3. First remains −166/−171, east Ninth closes at the existing x=10.75 curb with backup x=13, and Second/Avenue A stay −119. The new 339 well cuts overlapping ground planes; its refuse-storage collider belongs to its existing building owner. The lane remains clear. The address HUD remains Seventh-only.

`author_e09_n01b.py` and `e09_n01b_kit.py` write/consume the independent schedule. Packet-only edits rebuild only the four assigned IDs. Initial shared-dispatch integration required a full export. Final verification preserves all 217 preceding authored GLB and compiled scene hashes. The area split is 12 west / 209 pinned; all 221 models still load initially. This does not prove whole-area scalability.

## Review trail

Five model exports and five engine builds completed the repair loop. Initial review caught an overlapping 339 vent/number, a railing across its entry, the wrong door-glass composition, uniform blinds, grille topology, bright wall/canopy colors and simple displays. Later passes corrected dark entrance lining, tree proportions and curved canopy wear; the fourth pass exposed reversed side lettering. The fifth build fixes that lettering and was reviewed in full.

All **58 final detail images** were opened and inspected: four elevations and ground crops, six storefronts from front/left/right, building joins and rooflines, entrances and the well, seven protected context views and three weather views. [Inspected-image ledger](east-village-e09-n01b/inspected-views.json) and [business/face assessments](east-village-e09-n01b/visual-review.json) distinguish captures from actual review. Four earlier capture sets remain separate. Review is by the implementing agent, without independent second review or calibrated photographic 1:1 acceptance.

All **18 final gameplay images** were inspected. Six real-key driving legs have zero contacts and loading holds; seven held-throttle boundaries, four camera modes with orbit/zoom, reset and four single visual/collision owners pass. The 17 address cases pass. The first address-check trial reused command ID 1 and read the initial pose; the checker now uses one sequence counter for setup and cases. That failed trial is retained, and no game code changed for this repair.

## Exact build and measurements

Final build: **2026-10-14T05:01:04.528Z**. PCK **8,031,316 bytes**, SHA256 `143be91b9c79a859ff6de5ef3f4bb6bea718ab2573b1f8eef26a02c2d300588d`; Brotli size 7,409,689 bytes. The required package has **240 runtime files, 145 source hashes and 164,342,193 total runtime bytes**. The PCK grows 8,148 bytes and the full runtime catalog grows 5,062,272 bytes over N01A. External scenes must accompany the PCK.

| Local startup sample | Cold median / p95 | Cache-enabled median / p95 |
| --- | --- | --- |
| Before, 217 models | 8.067 / 8.488 s | 8.783 / 14.083 s |
| Final, 221 models, after restart | 6.971 / 7.226 s | 9.061 / 11.170 s |

Each cell uses five runs; nearest-rank p95 is therefore the maximum, not a stable population estimate. All 221 scenes cache-hit on every final warm run. Six driving-leg p95 values are **18.5–18.6 ms**, maximum **18.8 ms**. These are unthrottled local desktop observations at 1440×1000, not mobile, whole-area scalability or total RAM tests. The historical 12-model release/reload proof was not repeated in this packet.

The laptop shutdown interrupted the first final-startup trial after five recorded starts; its CDP timeout is retained in [the interrupted result](east-village-e09-n01b/performance-interrupted/startups.json). The complete final ten runs used a fresh isolated browser profile after recovery. The before/final conditions therefore differ and cannot establish a causal performance improvement. The earlier 14.083-second warm outlier and historical P02 21.687-second outlier remain unexplained. No diagnosis of the laptop shutdown is claimed.

Original-game and export verifiers pass. Four local HTTP response hashes and all 240 runtime response lengths match. [Preservation](east-village-e09-n01b/preservation.json) confirms the 217 previous GLB/SCN pairs, 132 prior build sources, 2,374 other tracked non-Markdown files and both unchanged/untracked private screenshots. [Metrics](east-village-e09-n01b/metrics.json) and [validation](east-village-e09-n01b/validation.json) hold raw references, conditions and documentation checks.

## Timing and continuation

The wall-time record in [progress](east-village-e09-n01b/progress.json) includes the shutdown gap. Active working time was not measured, so this fifth completed detail packet is excluded from timing calibration. Four earlier elapsed samples remain; the provisional 630–1,340 sessions / 630–2,250+ hours forecast is unchanged pending the planned recalibration.

Next, only on the next user instruction: **01-E09-21-N02A, 331–325 East Ninth**, four exact faces in [the next handoff](east-village-e09-n01b/next-handoff.json). The former eight-face N02 group is split into A and B; B retains 323–317. All 53 initial leaf-face assignments are retained without duplicates. No fresh N02 research or implementation has started.

No commit, push, CI, deployment, paid imagery or production recheck has occurred. Prior plan/loading/facade work remains local and uncommitted. Main and cached origin are `a2a90a3e08540e15f40e0ede0f8af14921f54675`; previously verified production remains revision 09. Preview: http://127.0.0.1:5181/.
