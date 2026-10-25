# East Ninth, First Avenue–Avenue A — complete block record

<!-- current-project-status -->
> **Current status:** The [project handoff](../CODEX-HANDOFF.md) governs current scope, publication and next work. This file retains its dated observations, evidence or specialist instructions. See [browser scaling](../docs/BROWSER-SCALING.md) for the current loading/rendering work; older model counts and paused states describe their original checkpoints.
<!-- /current-project-status -->

October 14–15, 2026. Complete local geographic pass with dated-source and performance limits; no publication.

**October 23 continuation note:** this exact 295-model result was transferred intact to the new laptop. Tool/build/browser/Street View setup and preservation checks are saved separately in [machine verification](machine-setup-2026-10-23/verification.json). The user is restarting VS Code/Terminal; use the [restart guide](../START-HERE.md#after-restarting-vs-code-or-terminal) and [current handoff](../CODEX-HANDOFF.md). Expansion remains local/uncommitted; GitHub/live retain the earlier 203-model revision 09. The dated source observations, visual acceptance limits and October 15 measurements in this report have not been replaced by setup checks. Next proposed block remains Tenth Second–First with protected-core ownership preparation on assignment; no new block/publication was performed.

The user’s “looks good keep going onto the next” assigned `01-E09-1A`; “session got cut off suddenly” continued that assignment. The delivery covers both sides and assigned corner returns: **50 facade planes across 41 buildings**, including eight articulated P.S.122 planes. Forty buildings are new; the existing 148 First Avenue model receives its deferred Ninth return. Current total: **295 models**. The schedule contains **745 architectural openings, 41 residential/institutional access entries and 42 shopfront/return records**; these are authored records, not counts of distinct currently operating businesses.

[Exact inventory](east-village-e09-east/inventory.json) · [Dated observations](east-village-e09-east/observations.json) · [Schedule](east-village-e09-east/schedule.json) · [Individual review](east-village-e09-east/face-review.json) · [Inspected images and repairs](east-village-e09-east/visual-review.json).

## Architecture and storefront work

The block retains separate narrow rowhouses, tenements, basement businesses and the articulated former school. Corrections include actual floor/bay rhythm, window divisions and hoods, independent doors/numbers, high stoops, iron-railed basement wells, building-height steps, ornamental stone and metalwork, painted versus exposed masonry and visible equipment. The low 410 frontage, 404 recessed roof volume and Celeste’s one-storey infill/open terrace are represented separately from their taller neighbors. The school’s assigned First return has a narrow supporting sidewalk through z=−181.65; the First Avenue vehicle cap remains −166.

Every shop has its own dated composition: Flower Power’s sunflower/wood/jar frontage; Whitmans’ black shade and chairs; FA’s carved rounded display windows; Thursday’s amber sign, red door and timber enclosure; Psychic’s script canopy; La Fleur’s leaf and pink lettering; Mr. Throwback’s sports lettering/garments; the barber’s pole and portraits; Social Tees’ dog graphic/bench; Hello Yam’s icon/white stools; the striped Creperie canopy/woven chairs; Murphy’s straight blue shade/plants; Confectionery’s rounded red canopy; Monkey’s green shade; Ralph’s picture-menu hatch; Doc’s wrap canopy and painted figures; Lime Tree’s Ninth enclosure and oval cloth mark. Those features come from each frontage’s evidence, not a shared business-name preset.

Recipes are [author_e09_east.py](author_e09_east.py) and [e09_east_kit.py](e09_east_kit.py). `e09_east_detail.gd` supplies the assigned street detail; owner-specific colliders cover the two curb dining structures. The exporter retains one visual/collision owner per building, including multi-plane corners and school. Shared recipe changes require exporting all 41 compatible owners even for a single geometry correction; unrelated old models remain protected.

## Review and repairs

Round01 capture was interrupted by disk exhaustion; its 339 PNGs are partial evidence and are not claimed as a fully inspected set. All **381 round02 images** were inspected: 50 elevations, 50 ground views, 32 wells, 46 business front crops, 92 business obliques, 100 mass/junction views, seven protected comparisons and four complete corner-store views. This revealed additional painted-masonry, ornamental railing, lettering and ground-depth defects.

All **80 round03 images** were inspected after repairing white-painted brick, diamond upper rails at 441–445, Lime Tree’s projected cloth lettering, La Fleur’s graphic clearance, Social Tees’ outlined face and double-sided well floors/inner linings. All **21 round04 images** were inspected after the school support strip and adjusted well/shelter/cloth cameras. A close view exposed Thursday’s molding crossing its sign; round05 moves only its lit face, lettering and wood character forward. All **six round05 images** were inspected, including three readable front/oblique sign views and neighboring/whole-facade views.

Review is by the implementer in a separate served-image pass, not an independent second reviewer. Images retain their actual build identity. All 295 compiled scenes match between rounds03/04; 294 remain identical in round05, with only `248142676` changing. Capture counts are not acceptance. [Final repair continuity](east-village-e09-east/repair-05.json).

## Preservation and bounds

All **254 unrelated preceding GLB/SCN pairs** remain byte-identical. The protected First-facing portion of shared 148 matches **34,523 transformed/color triangles**, with zero missing/added triangles at 0.1 mm coordinate precision; the comparison excludes the joining corner seam and is supplemented by mass/height assertions and rendered comparisons. [Audit and limitations](east-village-e09-east/first-face-preservation.json). Both private screenshots, original ten-block game, UI, audio and vehicle handling are preserved.

Ninth now connects Second–First–Avenue A, with east terminal **x=207** / outer **211**, west terminal **−213** / outer **−217**, center **z=−154.7**. First stays **−166** / outer **−171**; other avenue ends remain **−119**. The address HUD remains Seventh-only. The north school sidewalk is supporting geometry, not an opened road. Extreme free-camera orbit/zoom can intersect nearby awnings/escape rails as before; camera collision was not added. Unmodeled terrain beyond terminal caps remains outside this assigned street.

## Sources and limits

The ledger has **62 dated visual/reference records**, primarily July 2022 and September 2024, with older architectural and close-view supplements. Source pixels remain temporary reference, not distributed textures. This is not an October 2026 occupancy survey. Seven tenant identities remain `needs-evidence`: both 411 shops, 412/414 basement shops, east 428, west 434 and the star frontage at 436. Their observed physical storefronts are modeled and reviewed without invented names. Good Beer represents July 2022 appearance and is explicitly recorded as subsequently closed in September 2022; no current-tenant claim is made.

Fonts, illustration outlines, menu/poster contents, decorative measurements and merchandise remain approximations. Hidden roofs/rears/deep interiors are unobserved. Ground dimensions and relative heights use mapped geometry plus visual estimates, not survey calibration. Minor paving seams and stylized display objects are not exact photographic replicas. No calibrated multi-view 1:1 acceptance or measured “50×/100×” gain is claimed.

## Final validation and performance

Final build **`2026-10-15T04:33:43.860Z`**: PCK **8,178,208 bytes**, SHA256 **`b0100bd00b509f41afce60e8648e42c6892664b73c4757fc8ba49300f2d2b9ab`**. There are **314 required runtime files / 157 source hashes / 235,738,090 runtime bytes / 8,276,065 authored triangles**. The external scene catalog must accompany the shared pack. All 295 scenes initially load (12 west releasable / 283 pinned).

[Validation](east-village-e09-east/validation.json) records passing original/export verification, eight real-key driving routes without contacts/loading holds, eight held-throttle boundaries, four camera modes with orbit/zoom and fixed car, reset, 41 single model/collision owners, 17 address cases, ten startups, four local HTTP route hashes and all 314 runtime hashes. Twenty-one gameplay, eight weather and six follow-up driving images were inspected. The 17 address screenshots are retained; assertions passed, but those images are not claimed as an additional manual suite.

[Metrics and raw-run links](east-village-e09-east/metrics.json) retain these desktop results:

| Measurement | Median | p95 / maximum |
| --- | ---: | ---: |
| Five cold-cache startups | 16.883 s | 21.509 s |
| Five warm-cache startups | 22.543 s | 23.691 s |
| Seven main driving legs | — | p95 17.6–17.7 ms |
| Main westbound Ninth leg | — | p95 33.4 ms / max 5,049.1 ms |
| Three comparable chase repeats | — | p95 33.9 / 33.3 / 33.4 ms; max 300.1 / 34.4 / 34.4 ms |

All 295 scene responses were cache hits on every warm startup; warm was nevertheless slower. Historical 255-model startup medians were 9.928 s cold / 12.593 s warm. No fresh paired baseline was run, so this does not isolate the cause of the difference. Cold disables browser network cache, not OS/GPU/WASM caches. Browser counters do not establish total RAM or mobile capacity.

The **5.049-second frame gap** occurred with all models resident, no loading hold and no contact; cause is unknown. It did not recur in three chase repeats, but westbound rendering remains slower and adaptive scale fell from 1 to 0.75. Three initial repeats accidentally retained overhead mode; their faster figures are preserved separately and excluded from chase comparison. The checker now explicitly selects chase. This is **not a smooth-60-fps or whole-area capacity pass**; preserve detail while addressing this cost before substantial further growth.

Disk availability fell to 399 MiB after the startup suite and returned to about 3.0 GiB after the isolated review browser was closed. No inference is made that disk space caused the earlier stall or the laptop shutdown. The preview server remains running. [Hosting/preservation audit](east-village-e09-east/hosting-preservation.json) records 2,407 unchanged tracked files against this block’s baseline, the explicit changed-file list and both unchanged private screenshots.

Wall elapsed through validation was **647.2 minutes**, including the interruption/recovery and unmeasured inactive time. This is not active model/tool time and is excluded from a stable project-throughput forecast. Both larger block samples have interruptions; the 190 geographic units remain coverage inventory, not a promised number of sessions or hours.

## Save and continuation

All work remains **local and uncommitted** on `main` / cached `origin/main` `a2a90a3e08540e15f40e0ede0f8af14921f54675`. No commit, push, CI run, deployment, production recheck or paid source job was requested. Previously verified published architecture is revision09 (`0de4b54`, release `3457a29`). Unexpected session/laptop interruption and disk exhaustion are distinct events; the shutdown cause is unknown. Saved recipes, observations and checkpoints support recovery without temporary browser/process state.

Preview **http://127.0.0.1:5181/** (restart `npm run dev -- 5181`): north on First, then **right onto Ninth**. The legacy game stays at `/index.html`.

The next proposed geographic delivery is **`01-E10-21`, East Tenth between Second and First, both sides**, only on the next user instruction. Prepare exact ownership around the protected First/Tenth core then; do not treat a planning row as an edit allowlist. Preserve the 295-model result and both private images. Continue one complete assigned block with internal groups and individual detail review; no next street or publication runs automatically.
