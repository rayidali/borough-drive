# West Seventh streetscape anchors — September 15, 2026

The bounded First–Second East 7th pass uses the dated view metadata in [`west-seventh-reference-04.json`](west-seventh-reference-04.json) and the runtime ledger in [`west_seventh_streetscape.json`](../engine/first-seventh/assets/west_seventh_streetscape.json). It does not claim a survey, current municipal inventory, or 1:1 acceptance.

Each tree record stores its image `pixelU`, image heading/pitch/FOV, the exact `engineCameraStart` copied from the reference record, the curb depth assumption (7.25 m) and the inferred ground-frame X. The projection uses the actual `cameraStart.z`; source image pitch is only image metadata. Runtime north curb is `z=-7.25` and south curb is `z=+7.25`.

| Dated view | Tree-side anchors, inferred X (m) |
| --- | --- |
| 2026-04 west | north −188.86 |
| 2026-04 church | north −166.92; south −174.51 |
| 2024-09 54 | north −151.66; south −151.68 |
| 2024-09 58 | north −143.78; south −144.49 |
| 2024-09 62 | north −121.99; south −118.57 |
| 2024-09 68 | south −103.37 |
| 2024-09 73-close | north −78.44; south −83.53 |
| 2024-09 77-close | distinct north-79 and south-80 trees, both X −59.19 on opposite curbs |
| 2024-09 78 | south −53.94 |

The 76 view is retained as a possible repeat of the 73-close north tree and creates no second placement. Pixel ambiguity, curb depth and source-to-engine alignment set the stated 2–3 m placement uncertainty; the figures are useful visual anchors, not measured trunk coordinates.

The street kit removes generic hydrants, lamps and mailboxes in this west E7 interval while retaining the existing warm night-light pools. It keeps only location-supported fixtures: the Tile-corner mailbox from the 2024-09 corner view, a drain from 85-close, and the small parking-post group from 77-close. Dimensions and precise map positions remain estimates.

Two dated roadway structures are modeled with collision volumes: the 77 north enclosure has a black corrugated sloped roof and translucent panel enclosure, and the 86 south Yubu enclosure has red/yellow trim. Both are curb-anchored with an estimated 2.4 m road depth, leaving the fixed center route clear. Their along-street spans, interiors and panel artwork are estimates; neither lets the vehicle pass through.

The fire-site work separates the former 48 E7 strip (`x≈−218..−185`, `z≈9..20`) from the rear L-shaped church lot and its east return. The E7 edge uses a connected green chain-link diamond mesh and temporary poster panels. July 2026 LPC current-condition material supports the modeled plywood bracing, pale salvaged carved-stone stack, stored black gothic ironwork, orange barriers, yellow rails, dirt/rubble/excavation and tan remaining party wall with pointed niches. The proposed metal-and-glass portico is unbuilt and excluded. All site envelopes and item dimensions are metric estimates.
