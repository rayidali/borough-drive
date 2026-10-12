# First Avenue / St. Marks — individual storefront revision 09

October 11, 2026. The user asked to revise the actual work after an instruction-only update. This user-endorsed revision gives the businesses in the confirmed First Avenue Seventh–St. Marks and St. Marks Second–Avenue A scope distinct storefront compositions. It preserves the accepted Seventh/core/corner, original game, interface, audio and geographic bounds. The user subsequently said “yes this is great” and explicitly requested publication to `main` and updated documentation. No paid job or additional street is included.

## What changed

There are 80 individual business/return records: 78 shop units and two architectural business packets, across 57 faces in 51 buildings. All 203 building objects remain. The other 152 exported building models are byte-identical to revision 08. Returns count separately; 80 is not a claim of 80 distinct operating establishments.

- **Lettering and signs:** five font treatments, individual line breaks, spacing and support surfaces; arched optical sign, geometric Crif Dogs star dividers, tiny Nudibranch transom labels, Fun City's painted wall lettering, and East Village Books' yellow/red sign over its right window. New fonts have recorded provenance and four bundled OFL notices; selected fonts remain substitutes for exact shop letterforms.
- **Shade and outdoor furniture:** rounded 75 Cocktail Lounge canopy with lettering following the curve; varied solid, striped and scalloped awnings; brackets and frames; Maud's orange parasols, Goodnight Sonny's striped canopy/barrels, Mogador seating, benches, planters, folded parasols and shop-specific arrangements. Chair/table clearance is independent of storefront width.
- **Entrances and displays:** different door positions, recessed thresholds, arches, folding leaves, mullions, handles, low panels and gates; shelves, books, bottles, can stacks, textiles and notices where the reference supports their presence. La Palapa's street enclosure has its own record.
- **Surfaces and painted detail:** opt-in material classes for painted frames, wood, tile/grout, plaster, woven canvas, metal, paper and chalk; world-scale procedural patterns, selected finishes, separately authored window lettering and paint layers. Source photographs are not game textures. Fine painted artwork and merchandise remain simplified.

Examples in the served game: [Compton's](first-stmarks-review-09/final-businesses/241822288-0-0-0-front.png), [Maud](first-stmarks-review-09/final-businesses/241822164-1-0-0-front.png), [East Village Books](first-stmarks-review-09/detail-fixes/248142698-0-0-0-front.png), [75 Cocktail Lounge](first-stmarks-review-09/detail-fixes/241822217-0-0-0-left.png), [Fun City](first-stmarks-review-09/final-businesses/248142689-0-architecture-0-front.png). These images retain the package identities recorded in their manifests.

## Evidence and actual review

[The business ledger](storefront-observations-09.json) retains 108 locators: 55 revision 08 views and 53 additional browser detail captures, with observations, camera identity and uncertainty. Some camera labels do not identify the visible subject; neighbors and facade identity determine the evidence used. April 2026 and September 2024 imagery is not October occupancy verification. Tile Bar was inspected as the user's individuality example, without changing its protected model.

[The actual review record](first-stmarks-review-09/visual-review.json) covers all 80 records. All 279 full-candidate business crops were inspected: 93 front, 93 left and 93 right. Wide shops use overlapping crops. This exposed source/render discrepancies that were repaired, including canopy winding/culling, chair spacing, duplicate sign layers, missing glyphs, canopy/optical silhouettes, folding-window divisions and individual lettering/display placement.

Seven faces received a last repair pass. All 30 replacement front/left/right crops were inspected on the final package: Organic, 75 Cocktail Lounge, East Village Books, SOCKS, Crif Dogs and both Bar Al Pastor faces. The complete-candidate PCK is `588646c3a39e288b7153980b292eeeebbcd90ae812b6a2955d17814b0542ff83`; the seven-face captures use the final PCK below. Earlier captures are not relabeled as final-package evidence. The draft's 93 inspected front crops and repair notes remain separate. Unreviewed draft oblique pixels were discarded; the manifest records that retention decision.

The user endorsed this revision for publication on October 11. That establishes a working visual reference, not a calibrated 1:1 pass. Exact logo/letter shapes, fine graffiti and illustrations, tiny notices, product inventory and interiors remain incomplete or approximate. Source occlusions and estimated dimensions are explicit per business. The user's “100×” request is a qualitative direction, not a measured improvement or mesh-count target.

## Reproducible implementation

The current author is [author_storefront_09.py](author_storefront_09.py). It regenerates revision 08, then applies all 80 packets to `storefront-details.json.firstStmarksEngine`. Running `author_stmarks_08.py` alone resets the revision 09 additions. [storefront_individual_kit.py](storefront_individual_kit.py) is opt-in through `storefront09` / `detail09`; the existing protected storefront path is unchanged.

[The exporter](export_seventh_engine.py) preserves semantic material groups and records recipe/font/source hashes. The runtime selects [storefront.gdshader](../engine/first-seventh/shaders/storefront.gdshader) only for the new groups. [Font provenance](fonts/storefront-09/sources.json) and [static derivative recipe](fonts/storefront-09/instantiate.py) preserve the original licenses and rename derivatives.

```sh
python3 model-source/author_storefront_09.py
blender -b -t 4 --python-exit-code 1 --python model-source/export_seventh_engine.py
npm run seventh:build
npm run seventh:verify
npm run verify
```

Shared recipe changes require a full cache export, even though unchanged protected models remain byte-identical. The first detailed candidate exceeded the existing 100 MiB PCK limit. Lower tessellation and extrusion on newly added glyphs brought it under the cap; features were retained and readability inspected. Do not bypass stale-source or size checks.

With the local server and an isolated Chromium CDP browser on port 9222, use [review-storefronts-09.mjs](../scripts/review-storefronts-09.mjs) for every business's front/left/right crops; optional comma-separated face IDs restrict a repair capture. [The route harness](../scripts/review-first-stmarks-routes.mjs) uses normal keyboard physics and captures endpoint telemetry inside the browser frame loop. It stops at the measured endpoint only after recording/asserting the traversal, for readable screenshots.

## Package, checks and state

- Baseline branch `feature/first-stmarks-08`, instruction commit `23c63d8ed4afb2283f34c7058e80208d6e8f8b52`; gameplay/export baseline `02833ce18410c771881dac55d4034022db9729b2`. Implementation/export/evidence are saved locally in **`0de4b54dc9d0e711f11962688f0e6fca3aa01c50`**; a following checkpoint preserves exact OFL notice bytes in Git. Use the [current handoff](../CODEX-HANDOFF.md) and Git history for checkpoint state.
- Final geometry: 203 models, **4,035,769 triangles**. PCK **102,660,112 bytes**, SHA256 **`8da68329347228060231d47f46e80c9d6233b6afb0469fd43611bdc83204b1d0`**. All 18 runtime files total 143,048,305 bytes before HTTP compression. The unchanged `build.json.sourceCommit` is the geographic baseline `c76dcce…`, not this gameplay save; actual source hashes identify the tested build.
- Final `npm run seventh:verify` passes: 18 package files, 108 source hashes, 203 buildings, 82 Seventh frontages and 102 First/St. Marks faces. `npm run verify` passes original geography, models, driving/bounds, materials, batching and browser-presentation checks. Python/JS syntax and the reconstruction skill validator pass.
- [Preservation audit](first-stmarks-review-09/preservation.json): 51 intended models changed, 152 unchanged; all older schedule namespaces match; original game/core, UI/audio/controls, routing and both private screenshot hashes are preserved. The generated browser shell changes only the PCK size metadata. Private screenshots remain untracked.
- [All 18 final keyboard routes](first-stmarks-review-09/final-routes-complete/routes.json) pass across three weather modes, with zero measured route contacts, browser errors or failed responses. All 32 route/approach images were inspected: 18 stopped endpoints, three mid-street player views and eleven perspectives. A prior trial's post-endpoint coast hit the unchanged x=239 terminal; the browser-frame crossing measurement fixes that test timing error without changing the game. Both reports remain.
- [Performance results](first-stmarks-review-09/performance-summary.json): revision 08 baseline nine-sample mean **59.93 FPS**. Initial revised mean **57.83 FPS**, including a **1,433.4 ms** first-drive pause. The same final package's isolated repeat averaged **60.00 FPS**, range **59.98–60.01**, maximum frame gap **17.8 ms**. The pause did not recur; its cause is not proven. Local ready times were 6.289 s baseline, 7.172 s initial revised and 6.058 s repeat. These are the standard short First Avenue / Seventh samples on one Apple M1, not a complete St. Marks performance or public-network/device benchmark.
- **Published:** release `3457a29739ecd99f4c13bdde2efdb07cea30816f` is on `main` and live at [DriveAround.nyc](https://www.drivearound.nyc/). Both Node.js 22/24 jobs and Vercel passed. All 31 live checks match: root/Seventh/legacy/manifest on canonical, apex and Vercel hosts; all 18 runtime files including the complete PCK; refreshed credits. Production browser smoke passes launch, driving, four cameras, three weather modes and pause, with zero errors/warnings/failed responses. [Release evidence](publication-review-2026-10-11.json) · [current handoff](../CODEX-HANDOFF.md). The following publication checkpoint changes only documentation/evidence.

The skill, repository adapter and current entry points retain both the stronger business-level standard and the execution lessons from this pass. Source acquisition, modeled detail, inspected game views, test success and acceptance remain separate states.
