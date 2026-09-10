# First Avenue / East 7th Street — Street View refinement 08

Authored September 10, 2026 after the user authorized using the working Street View API to improve this corner toward the detail and presentation of Assassin’s Creed Unity. The five-building, nine-elevation, eight-shop scope remains the accepted [revision 06](FIRST-SEVENTH-PASS-06.md) benchmark. [The handoff](../CODEX-HANDOFF.md) distinguishes this local work from the previously published speed pass. This pass is not a claim of AAA production quality or a surveyed, pixel-exact digital twin.

## What changed

| Corner | Revised features |
| --- | --- |
| NW / Tile Bar | Longer paired-stripe canopy along East 7th; side window, residential entrance, painted wall, wheeled bins and cellar cover; adjusted irregular window spacing and AC locations. Old pavement tables are absent from the April views and removed. |
| NE / E7 Deli and adjoining shops | Current red Monkey Sushi sign and window strip; white Hen House sign with ochre script; revised E7 side sign and window spacing, illuminated window lettering, cooler/display detail, layered painted wall approximations. Burger has the visible red projecting sign and a red outdoor dining structure. |
| SW / E Smoke and Yubu | Exposed brick treatment, revised side-window/escape spacing, open metal grating, product-covered glazing, corner plaque, short sign return and poster/mural panels. Yubu gains shutter tracks/housing; the earlier open-door arrangement remains because the newer view is substantially blocked. |
| SE / Saifee, 114 and 116 First | Small service windows separate from full-size windows; two red-brown side escapes; full green side storefront with hardware carts, pots, soil bags, plants, reed blind, separate canopies and cream sign. Main canopy lettering and service labels updated. |
| Crossing | Four corner poles, longer traffic mast arms, pedestrian/street signs, utility lids and red tactile paving. Positions fit the existing road geometry and remain estimates. |

Window sash stops, sill caps, weather seals, paint wear, fixings and grating are authored geometry. The corner recipe is extended in [first_seventh_refinement.py](first_seventh_refinement.py), with individual facade schedules in [first-and-seventh.json](first-and-seventh.json) and shop records in [storefront-details.json](storefront-details.json).

The first browser review caught a material-batch overflow, repetitive painted strokes and a paint layer covering Burger’s glazing. Compatible matte colors now share a vertex-color material, the markings were revised, and the opaque painted wall ends before the separate shop opening. Glass, emissive signs, metallic iron and masonry surface maps retain distinct materials.

## Sources and accuracy limits

[The dated observation record](first-seventh-street-view-08.json) contains eight inspected panorama sources, their IDs, positions, headings, dates and observations. Most intersection images are **April 2026**. Closer west-side and Yubu views returned **September 2024**; an unrelated nearest **November 2017** selection was rejected for current shop claims. The API returning a panorama does not establish the newest capture available everywhere.

Google Street View images were inspected as temporary references and deleted after review. No Google photograph is bundled, projected onto a facade or included in these game screenshots. Google’s attribution is retained in the source records. Existing photographic and material licenses remain in [the credits](../dist/reconstruction/ASSET-CREDITS.md) and [third-party notices](../THIRD-PARTY-NOTICES.md).

The following remain incomplete, rather than silently treated as exact:

- Wall art, logos, font outlines and unreadable print are authored approximations. Painted groups establish the observed placement and color families; they do not reproduce every original stroke.
- Mapped footprints, original mapped heights and inherited rendered heights remain unchanged. No new dimensional survey was performed. The reference-position comparisons still show framing/proportion differences.
- Burger’s glazing is partly blocked by a truck/diners, and Yubu is largely obscured by a dining structure in the newer close view. Their complete current arrangements cannot be established from these images. The red dining structure is fitted within the existing sidewalk width, not positioned from a survey.
- Room depth, shelf stock, movable objects, lighting and weather combine observed features with estimates. Vehicles and trees remain illustrative; this is not a captured moment containing every pedestrian or temporary object.

Those limits matter to the requested 1:1 target. This pass makes concrete corrections across the corner; documenting the remaining differences does not fix them or certify completion to the user’s desired standard.

## Preservation and performance

Only **block-5-1, block-5-2 and edge-south** are rebuilt. [Preservation checks](first-seventh-08-preservation.json) compare 24 files against the published baseline: First & 10th model/recipe and six licensed photographs, vehicle/viewer/glass/spatial/shared-texture code and eleven unaffected neighborhood GLBs remain byte-identical. All 615 footprints, frontage geometry, mapped heights, road data and bounds are unchanged.

The existing startup/material cache, spatial batching, thin glass and idle-render gating remain in place. Only the bounded crossing treatment changes the road-rendering module. The final measurements and conditions are recorded in [the performance review](first-seventh-08-performance.json); compare with [pass 07](PERFORMANCE-PASS-07.md). These are short local samples on one device, not universal frame-rate guarantees.

Measurements: Chrome 152 / Apple M1, 1440×1000, DPR 1, unthrottled local HTTP with browser cache disabled. GPU/driver caches and thermal state were not reset. Driving samples use a fixed frame count, so elapsed time and route distance vary.

| Measurement | Published pass 07 | Local pass 08 |
| --- | --- | --- |
| Saifee Detailed, active rendering | 50.2 FPS | 48.9 FPS |
| Saifee Faster, active rendering | 60.0 FPS | 60.0 FPS |
| Northbound driving stress | 28.1 FPS | 26.8 FPS |
| Preserved First & 10th SE | 28.6 FPS | 27.8 FPS |
| Settled scene redraws | 0 | 0 |
| Initial reconstruction transfer | 38.24 MiB | 38.86 MiB |
| All neighborhood GLBs | 51.78 MiB | 52.40 MiB |
| Actual GLB triangles | 9,389,484 | 9,435,099 |
| Largest material batch count | 62 | 63 |

The new corner adds about **0.49%** to total neighborhood triangles. Matte paint colors share a vertex-color batch. Saifee mortar keeps its running-bond spacing and opening exclusions using surface bands instead of thousands of raised boxes; that removes 123,300 unnecessary triangles from the first refinement export. The measured result stays close to the optimized baseline, with a small frame-rate cost in these samples; it does not establish 60 FPS in dense Detailed views.

## Inspect and reproduce

Run `npm run dev` and open **http://127.0.0.1:5173**. The game starts at First & 7th. Use the four corner buttons and walk closer to the shops. The current local chapter label is **08**.

```sh
python3 scripts/compile-neighborhood-details.py
blender -b -t 6 --python-exit-code 1 --python model-source/build_neighborhood.py -- --tile block-5-1 --tile block-5-2 --tile edge-south
python3 scripts/audit-storefront-coverage.py
npm run verify
python3 scripts/verify-neighborhood-reproduction.py
```

Do not run the compiler during an export. It resets three older non-corner render-height metadata values (`241822303`, `241829661`, `248142640`) when rebuilding source data; preserve their existing exported values when leaving those sections unchanged. The clean reproduction check explicitly excludes export-only heights/metadata.

With an isolated Chrome on port 9222, `node scripts/review-first-seventh.mjs` exercises controls, streaming and recovery and captures 26 views. `node scripts/review-first-seventh-matched.mjs` captures the game at reference GPS positions/headings/pitches/FOVs with an explicitly estimated 2.50 m camera height and the game’s own lighting. It hides UI only inside its review tab; it does not alter the shipped game. `node scripts/profile-performance.mjs` measures actual active rendering separately from idle RAF responsiveness.

Final evidence: [browser review](first-seventh-08-final-review.json), [reference-position views](first-seventh-08-matched-review.json), [performance](first-seventh-08-performance.json), [baseline browser review](first-seventh-08-before-review.json), and [game captures](../docs/images/first-seventh-08/). These PNGs are unedited captures of the 3D game.

Open the four final game views: [Tile Bar / NW](../docs/images/first-seventh-08/seventh-nw.png), [E7 Deli / NE](../docs/images/first-seventh-08/seventh-ne.png), [E Smoke / SW](../docs/images/first-seventh-08/seventh-sw.png), [Saifee / SE](../docs/images/first-seventh-08/seventh-se.png). The [Saifee return comparison](../docs/images/first-seventh-08/matched/saifee-return.png) and [Monkey / Hen comparison](../docs/images/first-seventh-08/matched/monkey-and-hen.png) use the recorded reference position and angles.

Final local validation passed after the review-status update: `npm run verify`, clean source reproduction (615 buildings and all three audits), 26 browser views with controls/loading/retry checks, and 11 reference-position views. The injected core-load failure produces its expected warning and recovers; there were no unexpected errors or failed requests. These checks establish working exports and reproducibility, not visual acceptance or exact real-world dimensions. User acceptance of pass 08 remains pending.
