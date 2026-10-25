# EV-000 public geography snapshot

<!-- current-project-status -->
> **Current status:** The [project handoff](../../CODEX-HANDOFF.md) governs current scope, publication and next work. This file retains its dated observations, evidence or specialist instructions. See [browser scaling](../../docs/BROWSER-SCALING.md) for the current loading/rendering work; older model counts and paused states describe their original checkpoints.
<!-- /current-project-status -->

Retrieved October 12, 2026 for the authorized East Village boundary/topology inventory. These selected public municipal records are planning inputs; no photographs, property-owner records, financial records, credentials or paid endpoints are included. The initial bounding box includes surrounding context so the exact project polygon can clip whole source features. It is not the authoring boundary.

| Source | Publisher and original service | Saved features before project clipping |
| --- | --- | ---: |
| Street centerlines | [NYC OTI Centerline](https://services6.arcgis.com/yG5s3afENB5iO9fj/arcgis/rest/services/Centerline_view/FeatureServer/0) | 1,327 |
| Building footprints | [NYC OTI BUILDING](https://services6.arcgis.com/yG5s3afENB5iO9fj/arcgis/rest/services/BUILDING_view/FeatureServer/0) | 5,857 |
| MapPLUTO 26v2 | [NYC Department of City Planning, Information Technology Division](https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/ArcGIS/rest/services/MAPPLUTO/FeatureServer/0) | 5,389 |
| Shoreline 2022 | [NYC OTI shoreline service](https://services6.arcgis.com/yG5s3afENB5iO9fj/ArcGIS/rest/services/Shoreline_2022/FeatureServer/21) | 2 source features |

The shoreline service credits NYC OTI for funding/coordination, the Sanborn Map Company for production, and CARSI at Hunter College for management/quality assurance. Manhattan source imagery is March 18, 2022; later service edit timestamps do not make that shoreline a current-condition survey. Whole shoreline features are retained as returned; only the defined Houston–Fourteenth section enters the project inventory.

[Manifest](manifest.json) records the retrieval time, exact queries/selected fields, counts, SHA256 values and service edit metadata. Per-layer metadata files preserve source schemas and attribution. Each query first collected matching object IDs, then fetched bounded pages and verified exact ID equality with no duplicates or missing features. A failed oversized query was retried with smaller pages; no partial result is treated as complete.

Official interpretation: [NYC street-centerline metadata](https://github.com/CityOfNewYork/nyc-geo-metadata/blob/main/Metadata/Metadata_StreetCenterline.md). `STATUS=2` means constructed; `RW_TYPE=6` denotes a path/trail; `TRAFDIR=NV` denotes non-vehicular. These are map attributes, not current access certification. Width fields and Web Mercator lengths must not be mistaken for measured facade dimensions or local metres.

Use the original publishers' data terms and attribution; the repository's MIT license does not replace third-party terms. Existing OpenStreetMap/municipal provenance for legacy faces remains in [asset credits](../../dist/reconstruction/ASSET-CREDITS.md). The snapshot includes no business occupancy or visual observation claim.

See [EV-000 report](../../model-source/EAST-VILLAGE-EV000.md), [offline inventory script](../../scripts/inventory-east-village.py) and [explicit download script](../../scripts/fetch-east-village-inventory.py). Reproduction uses the saved snapshot. A future dated refresh must preserve this evidence and use a new destination.
