# October 25: minimap and spatial browser loading

The completed three-block expansion has 397 physical buildings in 398 model scenes. Candidate `2026-10-25T15:05:39.714Z` improves the bottom-left map and selects building residency by location and camera view. Publication is authorized before the next two blocks. The [current handoff](../CODEX-HANDOFF.md) records actual GitHub/live state; [validation](browser-scale-2026-10-25/validation.json) identifies tested files and completion states.

## Presentation and loading

The map uses actual building footprints, labeled authored roads, a warm heading marker, north indicator and distance scale in a compact rounded card. It follows the car within covered bounds. A bounded 456 × 312 pixel patch is cached and cropped as the car moves; its marker updates independently. Narrow windows retain the speed display and controls while hiding the map.

Building bounds occupy every intersected spatial cell. Nearby collision owners and visible owners load together, with speed/latency prefetch and delayed retirement. Proposed camera views and resizing wait for required scenes. The initial view is warmed without loading unrelated inspection-camera views. Existing immutable URLs, integrity checks, bounded request/staging queues and explicit recovery remain.

The camera visibility cache includes conservative translation, rotation and projection margins. Frustum broad-phase queries account for the far-plane diagonal, not merely camera depth. A 240-pose synthetic test checks cached-owner containment; a separate 100000-record test checks local index queries. These are metadata tests, not a rendered Manhattan benchmark.

Street geometry and materials are unchanged, grouped into 256 m cells to allow local visibility culling. Smaller tested cells increased draw calls too much. The pre-existing P03 street-label helper now accepts the material values its callers supply, fixing a native diagnostic error. All 398 compiled scenes, 374 ordinary authored GLBs, the original game and both private screenshots remain byte-identical to the frozen baseline.

## Evidence and performance limits

The final 21 weather/route samples measured engine averages of 95.25–120.00 fps, RAF p95 of 9.0–16.8 ms and a maximum sampled frame gap of 57.9 ms. Conditions were local M4 Max, Brave, 1440 × 1000, without network throttling. The preceding all-resident build measured 111.22–120.00 fps with a maximum sampled gap of 41.6 ms. This is a scaling change with measurable overhead on some current routes, not an across-the-board frame-rate improvement. Close-view building detail is preserved.

Earlier trials remain in the evidence directory: hidden warmup/no-op resize overfetch, costly direct map drawing, an insufficient one-second reset assertion, and malformed fault-injection response headers were diagnosed and corrected. Candidate07's driving regression motivated the larger cached map patch. Final ten routes, ten boundaries, four cameras/reset, five recovery/resize cases and ten startups pass without unexpected errors. Cold/warm startup medians are 13.405/13.431 seconds, with 331–331 of398 scenes ready. Exact completion is recorded in [validation](browser-scale-2026-10-25/validation.json); do not infer completion from the existence of a capture file. The 17-case address check belongs to candidate06, with unchanged address logic. Actual inspected images and their hashes are in [visual review](browser-scale-2026-10-25/visual-review.json).

Full Manhattan capacity remains unproven. The current catalog metadata and street/prop construction still span the authored neighborhood; future work needs paged metadata, resident street chunks, distant skyline representations and measured memory/network/device budgets. Individual scene decode/activation remains non-interruptible in this web export. See [browser scaling](../docs/BROWSER-SCALING.md) for these boundaries.

## Continuing assignment

After verified publication of this checkpoint, complete **Eleventh First–Avenue A (`01-E11-1A`)** and **Twelfth Second–First (`01-E12-21`)**, both sides. Preserve existing models and the school's reviewed First/Eleventh faces while preparing its Twelfth return. The user's instruction authorizes both blocks without routine stage permission. Source inspection, individual storefront/access geometry and served visual review remain required.
