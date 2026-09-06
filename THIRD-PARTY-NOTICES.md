# Licenses and attribution

The root [MIT License](LICENSE) covers original Borough Drive code, documentation, and independently authored artistic contributions. It does not relicense third-party material or the OpenStreetMap-derived geographic databases. Existing notices and source-specific terms continue to apply.

| Component | Terms and attribution |
| --- | --- |
| Original JavaScript, HTML/CSS, Python recipes, scripts, and documentation | MIT; Rayid Ali and Borough Drive contributors |
| OpenStreetMap snapshot and derived geographic databases | © OpenStreetMap contributors; [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/), with [OSM attribution guidance](https://www.openstreetmap.org/copyright) |
| Photographs by Eden, Janine and Jim | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/); exact sources and dates in [references.json](dist/reconstruction/references.json) |
| Photograph by Kidfly182 | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/); displayed unchanged as a reference |
| Poly Haven materials and reflection environment | [CC0](https://polyhaven.com/license); individual assets listed in [ASSET-CREDITS.md](dist/reconstruction/ASSET-CREDITS.md) |
| Three.js r180 and bundled addons | MIT; [included license](dist/vendor/THREE-LICENSE.txt) |
| Draco decoder | Apache 2.0; [included license](dist/vendor/draco/LICENSE) |

## Models, renders, and geographic data

`source-data/osm-raw.json` and the OSM-derived portions of the map and geometry manifests preserve OpenStreetMap data and identifiers. Geographic transformations and estimated additions are documented in the source recipes and observation records. Keep the ODbL notices and attribution when redistributing this data.

Exported GLBs and preview renders combine authored work, OSM-derived geography, and credited surface materials. The core model also embeds licensed photographic material. Two Beron art panels and a southwest masonry patch use CC BY 2.0 photographs through UV placement and repetition; those uses retain the original photographic attribution. MIT applies only to the project's original contributions within these combined assets.

The README's two preview images are the existing `intersection-render.png` and `southwest-render.png`. They show the actual authored mesh in standalone Blender renders. Their lighting differs from the browser viewer. They retain the model's geographic and asset credits.

## Photographic provenance

The distributed reference photographs remain unchanged. [references.json](dist/reconstruction/references.json) records authors, source pages, image dates, licenses, and local filenames. Records with no local file can document research without distributing the image.

JLL listing photographs and newer storefront/landmark photographs with no verified redistribution permission were used for visual observation only. Their pixels are not included as new textures or distributed reference images. Keep those distinctions and source records intact when contributing.

Building names, business names, and signs identify the reconstructed places. Their presence does not imply affiliation or endorsement, and MIT does not grant rights in third-party trademarks or other third-party material.

The detailed [asset credits](dist/reconstruction/ASSET-CREDITS.md), vendor notices, and [architectural research records](model-source/neighborhood-references/) remain part of every source distribution.
