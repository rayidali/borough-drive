# Licenses and attribution

The root [MIT License](LICENSE) covers original Borough Drive code, documentation, and independently authored artistic contributions. It does not relicense third-party material or the OpenStreetMap-derived geographic databases. Existing notices and source-specific terms continue to apply.

| Component | Terms and attribution |
| --- | --- |
| Original JavaScript, HTML/CSS, Python recipes, scripts, and documentation | MIT; Rayid Ali and Borough Drive contributors |
| OpenStreetMap snapshot and derived geographic databases | © OpenStreetMap contributors; [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/), with [OSM attribution guidance](https://www.openstreetmap.org/copyright) |
| NYC OTI footprints/roof heights, DCP PLUTO 26v2, DOHMH and DCWP public records | City of New York and the contributing agencies; [NYC Open Data policies and terms](https://cityofnewyork.github.io/opendatatsm/publicpolicies.html). Source-specific attribution, dates and modifications are retained; MIT does not relicense the city datasets. |
| Photographs by Eden, Janine and Jim | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/); exact sources and dates in [references.json](dist/reconstruction/references.json) |
| Photograph by Kidfly182 | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/); displayed unchanged as a reference |
| Poly Haven materials and reflection environment | [CC0](https://polyhaven.com/license); individual assets listed in [ASSET-CREDITS.md](dist/reconstruction/ASSET-CREDITS.md) |
| Three.js r180 and bundled addons | MIT; [included license](dist/vendor/THREE-LICENSE.txt) |
| Draco decoder | Apache 2.0; [included license](dist/vendor/draco/LICENSE) |
| Damion Regular, used for some script sign meshes | Copyright 2014 The Damion Project Authors; SIL Open Font License 1.1; [included license](model-source/fonts/OFL.txt), [source](https://github.com/google/fonts/tree/main/ofl/damion). A typeface approximation, not original business artwork. |

Performance pass 07 (September 9, 2026) preserves the accepted revision 06 models and all existing photographic provenance. `dist/reconstruction/street-materials.glb` contains seven original core material definitions and four byte-identical embedded Poly Haven images, extracted by `scripts/prepare-street-materials.mjs`; it adds no new imagery or license. Performance-review PNGs are unedited game captures and retain the same model/material credits. See [the report](model-source/PERFORMANCE-PASS-07.md) and [current publication state](CODEX-HANDOFF.md).

## Models, renders, and geographic data

`source-data/osm-raw.json` and the OSM-derived portions of the map and geometry manifests preserve OpenStreetMap data and identifiers. Geographic transformations and estimated additions are documented in the source recipes and observation records. Keep the ODbL notices and attribution when redistributing this data.

The dated NYC extracts in `source-data/` add 620 footprint records, 526 related PLUTO parcel records, 274 latest restaurant inspection records and five matched retail license records. They are geographic/business subsets of public datasets, not live feeds. The City's terms disclaim completeness and accuracy warranties; the application is independently authored and is not a City product. [ACCURACY-PASS-04.md](model-source/ACCURACY-PASS-04.md) documents selections, coordinate alignment, field conversions and joins. The joined geographic database retains its OSM attribution and ODbL obligations.

Exported GLBs and preview renders combine authored work, OSM-derived geography, and credited surface materials. The core model also embeds licensed photographic material. Two Beron art panels and a southwest masonry patch use CC BY 2.0 photographs through UV placement and repetition; those uses retain the original photographic attribution. MIT applies only to the project's original contributions within these combined assets.

The README's core preview images are the existing `intersection-render.png` and `southwest-render.png`. They show the actual authored mesh in standalone Blender renders; their lighting differs from the browser viewer. Revision 04's images and revision 05's `first-and-seventh-revision-05.png`, `tile-bar-revision-05.png` and `hen-house-revision-05.png` in `docs/images/` are captures of the actual local game. The revision 05 captures are unedited. Both kinds of preview retain the model's geographic and asset credits. They are not real-world reference photographs.

## Photographic provenance

The distributed reference photographs remain unchanged. [references.json](dist/reconstruction/references.json) records authors, source pages, image dates, licenses, and local filenames. Records with no local file can document research without distributing the image.

JLL listing photographs and newer storefront/landmark photographs with no verified redistribution permission were used for visual observation only. Their pixels are not included as new textures or distributed reference images. Keep those distinctions and source records intact when contributing.

Revision 04 adds written observations from Village Preservation's East Village Building Blocks archive, Morris Adjmi Architects' 45 East 7th project photographs, and Scoundrel's Field Guide's Blue & Gold coverage. Those research images are not distributed. The architect credits Jimi Billingsley, VUW, Field Condition and Nexus Development; Scoundrel's Field Guide is published by David Shaw. Exact source/image links and date limitations are retained in [neighborhood-facade-audit.json](model-source/neighborhood-facade-audit.json). Authored geometry and generic credited surface maps remain distinct from those photographic references.

Published storefront pass 05 adds observation records from Tile Bar's website, EV Grieve, Kevin Walsh / Forgotten New York and Village Preservation, with two separately identified reused cross-street observations. [storefront-details.json](model-source/storefront-details.json) and the downloadable [neighborhood sources](dist/reconstruction/neighborhood-sources.json) retain exact links, dates and limitations. These photographs are not redistributed or copied into new textures. The included Damion font and its full license remain separate from business artwork. [Pass 05](model-source/STOREFRONT-PASS-05.md) documents the partial scope; [the handoff](CODEX-HANDOFF.md) records publishing and continuation status without changing these license terms.

Building names, business names, and signs identify the reconstructed places. Their presence does not imply affiliation or endorsement, and MIT does not grant rights in third-party trademarks or other third-party material.

The detailed [asset credits](dist/reconstruction/ASSET-CREDITS.md), vendor notices, and [architectural research records](model-source/neighborhood-references/) remain part of every source distribution.

## First & Seventh observation pass 06

The local September 8, 2026 study adds photographic observations from Tile Bar, Village Preservation, EV Grieve (including credited Stacie Joy and Rainer Turim photographs), eastvillage.com and the E Smoke business/listing sources. [first-and-seventh.json](model-source/first-and-seventh.json) preserves exact source/image URLs, available dates, observations, access limitations and reuse status. New reference photographs are not included in game assets or repository screenshots. Modeled lettering and mural color fields are interpretations; they are not licensed reproductions of exact shop artwork. Existing photograph, font, material and geographic licenses remain in force. The new comparison screenshots are unedited captures of the running game.

## First & Seventh visual observations — September 10, 2026

Google Street View (© Google) was inspected through the Street View Static API: predominantly April 2026 imagery, with September 2024 closer west-side/Yubu views. The dated panorama IDs, source links, observations and limitations are recorded in [pass 08](model-source/FIRST-SEVENTH-PASS-08.md) and [its observation record](model-source/first-seventh-street-view-08.json). Google image pixels are not distributed, embedded or applied as game textures. Access credentials remain local. API access does not itself grant a general right to redistribute imagery or create derived datasets; see [Google’s terms](https://cloud.google.com/maps-platform/terms).

The refinement’s wall markings, lettering, color values and small display items are authored approximations, not exact reproductions or scans. Existing Poly Haven surfaces and the six licensed core photographs keep their original credits and terms. New review PNGs capture the actual game, with the same underlying asset credits.

## Browser presentation pass 09

The depth-based ambient pass extends the vendored Three.js SSAO kernel and blur; the original Three.js MIT notice and shader provenance remain included. Static procedural clouds and bounded road-color variation are authored presentation effects applied to the existing credited surface materials. No new photograph or generated architectural reference is included. The new offline workflow does not ingest Google imagery: standard Google Maps terms restrict bulk extraction and derived content, and an API key or deletion of previews does not itself resolve those restrictions. Existing source and photographic credits remain unchanged.
