# First Avenue and East 10th Street — asset credits

This is a photo-guided reconstruction. It is not survey-accurate or a current-day capture. Source photographs and generated model renders are distinguished in the viewer.

## Geographic data

OpenStreetMap contributors, ODbL 1.0. https://www.openstreetmap.org/copyright
Snapshot: September 5, 2026. Geographic origin: 40.72877901545095, -73.98444322040825.
Building footprints retain their original OSM identifiers. Eave heights, roof equipment, and the theater/tower subdivision have manual photographic adjustments. Exact curb dimensions, some neighboring facades, hidden walls, cars and vegetation are inferred.

## Photographs

Individual dates, authors, source URLs, licenses, and unmodified-file provenance are in references.json.

- Eden, Janine and Jim: southwest corner (September 6, 2021), southeast corner (October 31, 2021), Tarallucci sidewalk (2021), theater (June 6, 2021), and Beron detail (May 16, 2025). CC BY 2.0: https://creativecommons.org/licenses/by/2.0/
- Kidfly182: northeast side (May 26, 2022). CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/
- JLL: full northwest and northeast listing photographs. Photo date and reuse license unknown. Observed for architectural proportions; these image files are not distributed.

The original licensed photographic pixels are unchanged. Two Beron art panels and a small unobstructed southwest masonry patch are mapped onto 3D geometry through UV coordinates. These uses adapt their placement and repetition and retain CC BY 2.0 attribution. The Kidfly182 photograph is displayed unchanged as a reference and retains its CC BY-SA 4.0 license.

Business sources and status are recorded in businesses.json (checked September 6, 2026). Beron branding and art panels remain historical references after its December 2025 closure. No current tenant is asserted at 162 First Avenue. New storefront geometry was observed in official business photographs and dated local reporting; those new photographs are not redistributed. Exact partition widths and interior furnishings remain inferred.

## Materials and renderer

Poly Haven, CC0: https://polyhaven.com/license
- red_brick_03: https://polyhaven.com/a/red_brick_03
- brown_brick_02: https://polyhaven.com/a/brown_brick_02
- concrete_wall_006: https://polyhaven.com/a/concrete_wall_006
- asphalt_02: https://polyhaven.com/a/asphalt_02
- urban_alley_01: https://polyhaven.com/a/urban_alley_01 (reflection lighting only; not a geographic background)

These generic PBR textures represent surface materials; they were not captured from the actual buildings.
Three.js r180: MIT; ../vendor/THREE-LICENSE.txt.
Draco decoder: Apache 2.0; https://github.com/google/draco/blob/main/LICENSE.

The authored mesh and Blender recipe are independent geometry. Model dimensions are in metres. The source recipe is model-source/build_intersection.py in the project repository; the viewer provides a portable compressed GLB download.

## Current storefront observations (not redistributed photographs)

- Gelatoville: https://gelatoville.com/
- HAGS, June 1, 2026: https://evgrieve.com/2026/06/for-hags-bigger-things-are-on-menu-with.html (Stacie Joy photograph).
- Nishaan: https://eatnishaan.com/ (official full front and blade sign photographs).
- Pasta de Pasta, April 1, 2025: https://evgrieve.com/2025/04/pasta-de-pasta-making-return-engagement.html (Stacie Joy photographs; visit reported as the previous day).
- Good Time, June 3, 2026: https://evgrieve.com/2026/06/retro-signage-alert-good-time-country.html (sign installed; opening not verified).
- Apollo, March 5, 2024: https://evgrieve.com/2024/03/apollo-bagels-now-with-signage-on-10th.html (photograph credited Steven).
- Theater frontage: https://www.chelseanewsny.com/news/theater-for-the-new-city-s-lower-east-side-festival-celebrates-30-years-of-creativity-NL4409197 (published April 2025; capture date unconfirmed). Current program titles: https://theaterforthenewcity.net/ . Poster layouts are authored interpretations.

Publication dates above are not automatically photograph capture dates. Geometry, type, colors and proportions are reconstructed observations rather than a photographic texture copy.


## Ten-block neighborhood expansion

Building footprints, mapped addresses and supplied heights: © OpenStreetMap contributors, ODbL, same September 5, 2026 snapshot and local coordinate frame as the core. Geometric transformations, missing-height estimates and facade observations are documented separately in the source project.

Additional architectural photographs were inspected for proportions and details only; their pixels are not redistributed or copied into textures. Full records and URLs are in `neighborhood-sources.json` and the source project's `model-source/neighborhood-references/`. Sources include Village Preservation's East Village Building Blocks archive, NYC Landmarks Preservation Commission reports and existing-condition submissions, Kevin Walsh's December 2024 Avenue A walk published by Forgotten New York, official business sites and dated local reporting such as EV Grieve. Upload/publication dates are not automatically image-capture dates.

The independent Blender recipes create the new meshes, tree leaves, benches, lamps and cars. Generic Poly Haven CC0 surface images are shared across section files through content-addressed URLs in `neighborhood/textures/`. They represent masonry and pavement; they are not scans of these NYC buildings. Unknown facade layouts, interiors, street furniture positions and other inferred details are disclosed in the model data and viewer.
