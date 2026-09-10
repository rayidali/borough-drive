# East Village and the First & 10th core — asset credits

This is a photo-guided reconstruction. It is not survey-accurate or a current-day capture. Source photographs and generated model renders are distinguished in the viewer.

**Accepted standard, September 9, 2026:** First & 7th revision 06 covers five individual buildings, nine elevations and eight shops. The owner accepted it as the minimum completion standard for later work. Runtime performance pass 07 preserves all those model files, architectural references and six licensed core photographs. There are 27 individual non-core shop designs and 177 supported names with estimated designs across the map. [Neighborhood sources](neighborhood-sources.json) retain dates and access limits. The [source-repository handoff](https://github.com/rayidali/borough-drive/blob/main/CODEX-HANDOFF.md) records exact source/push/deployment states.

The startup `street-materials.glb` is an exact subset of seven core material definitions and four embedded Poly Haven CC0 images, reproduced by `scripts/prepare-street-materials.mjs`. It adds no new photographs. The thin-pane glass shader uses the existing modeled-corner reflection capture and environment; it is a rendering approximation, not a new photographic source.

## Geographic data

OpenStreetMap contributors, ODbL 1.0. https://www.openstreetmap.org/copyright
Snapshot: September 5, 2026. Geographic origin: 40.72877901545095, -73.98444322040825.
Building footprints retain their original OSM identifiers. Eave heights, roof equipment, and the theater/tower subdivision have manual photographic adjustments. Exact curb dimensions, some neighboring facades, hidden walls, cars and vegetation are inferred.

## Photographs

Individual dates, authors, source URLs, licenses, and unmodified-file provenance are in [references.json](references.json).

- Eden, Janine and Jim: southwest corner (September 6, 2021), southeast corner (October 31, 2021), Tarallucci sidewalk (2021), theater (June 6, 2021), and Beron detail (May 16, 2025). CC BY 2.0: https://creativecommons.org/licenses/by/2.0/
- Kidfly182: northeast side (May 26, 2022). CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/
- JLL: full northwest and northeast listing photographs. Photo date and reuse license unknown. Observed for architectural proportions; these image files are not distributed.

The original licensed photographic pixels are unchanged. Two Beron art panels and a small unobstructed southwest masonry patch are mapped onto 3D geometry through UV coordinates. These uses adapt their placement and repetition and retain CC BY 2.0 attribution. The Kidfly182 photograph is displayed unchanged as a reference and retains its CC BY-SA 4.0 license.

Business sources and status are recorded in businesses.json (checked September 6, 2026). Beron branding and art panels remain historical references after its December 2025 closure. No current tenant is asserted at 162 First Avenue. New storefront geometry was observed in official business photographs and dated local reporting; those new photographs are not redistributed. Exact partition widths and interior furnishings remain inferred.

## Materials and renderer

Poly Haven, CC0: https://polyhaven.com/license
- red_brick_03: https://polyhaven.com/a/red_brick_03
- brown_brick_02: https://polyhaven.com/a/brown_brick_02
- white_bricks, Rob Tuytel: https://polyhaven.com/a/white_bricks (included surface maps used by neighborhood detail revision 03)
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

## Neighborhood detail revision 03 — September 6, 2026

`model-source/neighborhood_detail_kit.py` builds recessed windows and entrances, sashes, curtains, sill drip edges, door hardware, shutter housings, service pipes and cornice microdetail. Their exact dimensions and placement are authored estimates. The specific arched crowns, entrances, quoins and roof railing in `model-source/neighborhood-detail-schedule.json` translate the existing dated architectural research into geometry. They do not assert new photograph dates or current occupants.

`model-source/build_streetscape.py` creates original bicycle, hydrant, bin, utility-cover and drain-grate meshes. Their deterministic placements are illustrative street dressing. The accepted core model and all source photographic bytes remain unchanged. Bare masonry uses the credited color/roughness/normal maps; painted masonry retains its recorded paint color over surface roughness and normal maps. No reference photographs were generated, recolored, or redistributed by this pass.

## Neighborhood accuracy revision 04 — September 6, 2026

Municipal data supplements the same existing map extent:

- **NYC Office of Technology and Innovation:** 620 building footprint records, BIN/DOITT identifiers, roof heights and edit dates. [Dataset](https://data.cityofnewyork.us/Housing-Development/Building-Footprints/5zhs-2jue); [field metadata](https://github.com/CityOfNewYork/nyc-geo-metadata/blob/main/Metadata/Metadata_BuildingFootprints.md). Five missing footprints are added with a documented translation into the accepted coordinate frame; 570 direct matches supply roof heights. The city data is not asserted to be a current field survey.
- **NYC Department of City Planning:** PLUTO 26v2, 526 related parcel records, retrieved September 6, 2026. [Public data](https://data.cityofnewyork.us/resource/64uk-42ks.json). Only geographic, building and address attributes are retained.
- **NYC Department of Health and Mental Hygiene:** 274 latest establishment inspection records in the modeled extent. [Public data](https://data.cityofnewyork.us/resource/43nn-pn8j.json). Inspection dates are retained and do not guarantee continued occupancy.
- **NYC Department of Consumer and Worker Protection:** five matched retail premises from [Legally Operating Businesses](https://data.cityofnewyork.us/Business/Legally-Operating-Businesses/w7w3-xahh). License status is supporting dated evidence, not an opening guarantee.
- **NYC Department of Transportation:** [March 5, 2025 completion report](https://www.nyc.gov/html/dot/html/pr2025/safer-across-manhattan-aves.shtml), supporting the widened Second Avenue bicycle lane and upgraded bus lane. Other facility types and directions use the included OSM snapshot. Road and lane dimensions remain estimates.

City data retains its source-specific terms and [NYC Open Data policies](https://cityofnewyork.github.io/opendatatsm/publicpolicies.html). The project documents its extracts, joins, coordinate alignment and height conversions in `model-source/ACCURACY-PASS-04.md` and `geography-corrections.json`. MIT covers the project's original contributions and does not relicense the city datasets or remove ODbL obligations from the OSM-derived geography.

**Architectural photographs used for observation only:**

- Village Preservation, [East Village Building Blocks](https://buildingblocks.villagepreservation.org/). Individual building/profile URLs and image URLs appear in `neighborhood-sources.json` under `facadeAudit`. Most newly inspected archive photographs have 2012 upload paths; capture dates are generally unknown. The archive's old tenants are not automatically treated as current businesses.
- Morris Adjmi Architects, [45 East 7th](https://ma.com/45-east-7th.html), completed 2021. The publisher credits Jimi Billingsley, VUW, Field Condition and Nexus Development. Inspection informs brick pattern, proportions, window arrangement, cornice and setback; it does not supply image textures or establish measured dimensions.
- Scoundrel's Field Guide / David Shaw, [Blue & Gold Tavern](https://scoundrelsfieldguide.com/new-york/new-york-city/blue-gold-tavern/). The inspected close facade photograph has a May 2022 upload path and no confirmed capture date. It informs the small sign, low brick frontage, green awning and metalwork.

The 376 new written facade observations are included; those research photographs are not redistributed. Existing licensed photographic files and the core model are unchanged. New facade forms are independently modeled geometry over the previously credited generic material maps. Exact shop units, most sign lettering, service details, interiors and street dressing remain authored estimates. Business evidence and contrary/closure evidence retain their separate dates in the downloadable source inventory.

## Storefront detail pass 05 — September 8, 2026

New source photographs were inspected from Tile Bar's website, EV Grieve, Kevin Walsh / Forgotten NY, and Village Preservation. Their exact URLs, original dates, uncertainty and observation notes are in `neighborhood-sources.json` under `storefrontDetails`. These new photographs are not redistributed or copied into textures. Irving Green and Casey Rubber Stamps reuse the separately identified prior observations.

Script sign meshes use **Damion Regular**, Copyright 2014 The Damion Project Authors (https://github.com/googlefonts/damionFont), SIL Open Font License 1.1. The font and complete license are preserved in the source repository's `model-source/fonts/`; a runtime copy of the notice is at [DAMION-OFL.txt](DAMION-OFL.txt). Source: https://github.com/google/fonts/tree/main/ofl/damion (retrieved September 8, 2026). Typeface substitution, object dimensions, paint values and unseen details remain estimates; business sign/logotype designs are not claimed as original project artwork.

Revision 05's three images in the repository's `docs/images/` are unedited captures of the actual browser game, with its existing adaptive graphics settings. They carry the same model/geographic credits and are not real photographs or new photographic textures. Their review conditions and limitations are recorded in `model-source/storefront-review-2026-09-08.json`. Older reports and images retain their original dates; this documentation refresh does not assert a new street survey or change existing licenses.

## First & Seventh study 06 — September 8, 2026

- Tile Bar's official exterior image (July 26, 2023 filename; unconfirmed capture date): [tilebarnyc.com](https://www.tilebarnyc.com/).
- Individual corner architecture: [Village Preservation / Building Blocks](https://buildingblocks.villagepreservation.org/). Archive upload paths are from 2012; capture dates are generally unknown.
- Saifee exterior and lights: [EV Grieve, September 5, 2025](https://evgrieve.com/2025/09/sept-5.html); additional 2024 plant-display photographs, including Rainer Turim, are linked in the source manifest.
- Tenant change and surviving Unique exterior: [EV Grieve / Stacie Joy, Monkey Sushi, July 3, 2025](https://evgrieve.com/2025/07/openings-monkey-sushi-on-1st-avenue.html).
- E7 Deli: [eastvillage.com](https://eastvillage.com/shopping/e7-deli-cafe/e7-deli/), image upload March 2024; capture date unknown.
- Hen House, Yubu and 7th Street Burger: dated EV Grieve articles listed in `cornerDetails.sources`; E Smoke: official business site and business-credited listing photos with unknown dates.

These photographs were inspected for authored geometry and are not redistributed. Google Street View was unavailable during this review. Small labels, precise murals, some return elevations, material colors and all unmeasured dimensions remain interpretations; generic surface assets are not scans of these buildings. Saifee's buff running-bond mortar is authored geometry. Storefront glass reflects the reconstructed intersection. All existing licensed core photo files remain unchanged.

## First & Seventh visual observations — September 10, 2026

Google Street View (© Google) was inspected through the Street View Static API: predominantly April 2026 imagery, with September 2024 closer west-side/Yubu views. The dated panorama IDs, source links, observations and limitations are recorded in [the neighborhood sources](neighborhood-sources.json). Google image pixels are not distributed, embedded or applied as game textures. Access credentials remain local. API access does not itself grant a general right to redistribute imagery or create derived datasets; see [Google’s terms](https://cloud.google.com/maps-platform/terms).

The refinement’s wall markings, lettering, color values and small display items are authored approximations, not exact reproductions or scans. Existing Poly Haven surfaces and the six licensed core photographs keep their original credits and terms. New review PNGs capture the actual game, with the same underlying asset credits.

## Browser presentation pass 09

The depth-based ambient pass extends the vendored Three.js SSAO kernel and blur; the original Three.js MIT notice and shader provenance remain included. Static procedural clouds and bounded road-color variation are authored presentation effects applied to the existing credited surface materials. No new photograph or generated architectural reference is included. The new offline workflow does not ingest Google imagery: standard Google Maps terms restrict bulk extraction and derived content, and an API key or deletion of previews does not itself resolve those restrictions. Existing source and photographic credits remain unchanged.
