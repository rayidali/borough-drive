# Neighborhood accuracy revision 04 — September 6, 2026

**Historical reference/report; current state updated September 9, 2026.** The material below remains a dated record, including its original counts, source dates and checks. The owner accepted [First & 7th revision 06](FIRST-SEVENTH-PASS-06.md) as the minimum completion standard. [Performance pass 07](PERFORMANCE-PASS-07.md) preserves the model exports and improves runtime speed. Read [CODEX-HANDOFF.md](../CODEX-HANDOFF.md) for exact current source/push/deployment states. Wider block/street processing awaits the later plan; this historical report does not authorize new work.

The previous detail pass added geometry without resolving enough of the underlying geography and storefront inventory. This pass audits the whole existing map against municipal footprints, architectural photographs and independently dated business evidence. The First Avenue/East 10th Street core and its licensed photographs remain preserved.

## Scope and coverage

| Inventory | Result |
| --- | --- |
| Existing geographic scope | Ten blocks, East 7th–East 12th, Second Avenue–Avenue A, plus four boundary sections |
| Municipal footprint records checked | 620; every record has an explicit building match |
| Missing substantial buildings restored | 5 |
| Building objects, including annexes and boundary context | 615; 592 outside the preserved core |
| Additional building objects with photographic observations | 410, up from 77 |
| New facade audit records | 376; some refine previously observed buildings |
| Original mapped retail/food/bar/bank candidates reviewed | 369 |
| Independently supported named place records | 212, including 202 outside the core |
| Business audit entries excluded or unresolved | 167, including closed, superseded, duplicate and upper-floor entries |

These counts describe records, not a survey of every elevation. Of the non-core building objects with street frontages, 142 still lack individual photographic observations. Some are small secondary structures or boundary context. Roof equipment, unseen walls, exact opening depths, shop partitions, interiors, furniture, trees and parked vehicles remain estimates. No claim is made that every tenant is open today or that every facade matches September 2026.

## Missing buildings and geometry

The [NYC OTI footprint extract](../source-data/nyc-buildings-2026-09-06.geojson) and [PLUTO 26v2 parcel subset](../source-data/nyc-pluto-2026-09-06.json) supplement the existing OSM snapshot. The source records retain municipal identifiers, edit dates and height provenance. Owner names and financial parcel attributes are not included.

| Restored building | NYC BIN | Modeled consequence |
| --- | --- | --- |
| 73–75 East 7th Street | 1006347 | Restores the six-story building beside Blue & Gold's block; accommodates Big Bar |
| 256–258 East 10th Street | 1005900 | Restores the missing apartment frontage |
| 323–325 East 12th Street | 1006505 | Restores a six-story northern boundary building |
| 195–197 Avenue A / 441–445 East 12th | 1005999 | Restores the corner building and separate businesses on its two streets |
| East Side Community School, 420 East 12th | 1005974 | Restores its H-shaped building, recessed elevations and open internal courtyard |

The school identity and address are recorded by [NYC Public Schools](https://www.schools.nyc.gov/schools/M450). It is separate from PS 19 on First Avenue.

The five new footprints are translated **0.553 m east and 0.744 m south in the local game frame** to align them with the accepted map. This offset is the median of 523 comparable shared-BIN footprints; the residual centroid difference at the 95th percentile is 0.161 m. This measures agreement between those two datasets, **not absolute model or facade accuracy**. Existing OSM and core footprints are not shifted, rotated or scaled. Partial overlaps and annex matches remain explicit in [geography-corrections.json](geography-corrections.json).

Direct single-BIN matches provide roof-height provenance for 570 non-core objects. Municipal roof heights describe the roof above local ground and exclude roof equipment; individual landmark recipes retain their documented subdivisions. The city [footprint metadata](https://github.com/CityOfNewYork/nyc-geo-metadata/blob/main/Metadata/Metadata_BuildingFootprints.md) explains the source field definitions. The model does not inherit the accuracy of a survey merely by using these records.

## Facades and conflicting references

[neighborhood-facade-audit.json](neighborhood-facade-audit.json) records the inspected photograph, building identity, observed story/bay arrangement, material family, ground-floor use, fire escapes, cornice treatments and limitations. These observations control the geometry directly. The combined 459 source records include the earlier observation schedule and 376 audit records.

The audit uses [Village Preservation's East Village Building Blocks](https://buildingblocks.villagepreservation.org/) and separately credited references. Many archive images were uploaded in 2012; their capture dates are not supplied. The audit does not turn an upload date into a capture date or use an old shop sign as current occupancy evidence. Research photographs are not redistributed or copied into textures.

Specific corrections include:

- **79 East 7th / Blue & Gold:** five-story, three-bay brick elevation, green cornice and escape, low brick shopfront, two dark windows, central entrance, green awning and small blue/gold sign. Its dedicated profile also uses the closer [Scoundrel's Field Guide photograph](https://scoundrelsfieldguide.com/new-york/new-york-city/blue-gold-tavern/), uploaded May 2022 with an unconfirmed capture date. The shallow entrance treatment is simplified; no below-street interior is modeled.
- **81 East 7th / Abraço:** raised residential entrance and low shop opening, separated from the upper window rows. Exposed basement levels are no longer universally counted as extra full stories.
- **45 East 7th / 119 Second Avenue:** the archive shows the post-explosion vacant site; the architect records a completed 2021 replacement. The new recipe follows the completed building's brick pattern, banding, tall openings, dark cornice and setback. [Morris Adjmi Architects](https://ma.com/45-east-7th.html) documents the seven-story building and credits its photographs. Proposed LPC elevations inform proportions but are not described as as-built measurements.
- **East Side Community School:** grouped classroom glazing, pale stone surrounds, brick wings and the red entrance beside the western end of the recessed East 12th Street elevation. Sculpture, court details and the small identification plaque are simplified or estimated.
- **Across the map:** individual bay counts and positions, rectangular/segmental/round openings, recorded escape absence and placement, paired windows, basement levels, stoops, pedimented entries, roof balustrades and ground-floor uses replace more of the shared defaults.

The facade builder also fixes a rendering defect: aggregated street frontages previously failed to match subdivided footprint edges, leaving solid wall skins across some modeled openings. Window and storefront openings now cut the correct wall surface. Courtyard holes remain open in the full model, distant geometry and building collision. Material sharing now distinguishes same-name materials with different colors, preventing the core's palette from overriding neighborhood finishes.

## Businesses and storefront placement

[neighborhood-business-audit.json](neighborhood-business-audit.json) is generated from the mapped inventory, [business website evidence](../source-data/business-web-evidence-2026-09-06.json), [NYC restaurant records](../source-data/nyc-business-records-2026-09-06.json), selected [retail license records](../source-data/nyc-retail-records-2026-09-06.json), prior research and [explicit corrections](business-corrections.json). All checks are dated September 6, 2026; each inspection retains its own date.

A matched business website address, a matching city inspection from September 2025 onward, or an individually reviewed source can support a new name. An inspection is dated occupancy evidence and a license is dated licensing evidence; neither guarantees continued operation. Placeholder inspection dates are not accepted as recent inspections. Old or contradictory names remain in the audit without a new current sign.

Examples beyond Blue & Gold include Big Bar, Abraço, Porto Rico Importing Co., Pillow-Cat Books, Boris & Horton, Smør, Barber's Blueprint and Smithereens. More recent records replace the old Crispy Burger and 192 First Avenue Pasta de Pasta identities with Spirals and Pastasole. Ferns' older website conflicts with a [June 2025 broker listing identifying a former tenant](https://www.meridiancapital.com/wp-content/uploads/2025/06/166-First-Avenue-Meridian-Setup.pdf); the old name is excluded. Historical Beron signage in the preserved core keeps its existing disclosure.

Businesses are joined to a specific building and street elevation. Multiple tenants share estimated subunits ordered by their mapped positions; a corner address no longer automatically labels every ground-floor wall. An unpartitioned span over 14 m receives a conservative envelope of at most 6 m on either side of its mapped point, leaving unsupported stretches unnamed. This prevents a small shop from claiming a whole long elevation; the envelope is not a measurement. Storefront dimensions, most typography and unobserved interiors remain estimates. The named-place count is an evidence inventory, not a claim that 212 storefront designs have been photographed; small units and dedicated landmark recipes may have different visible signage.

The travel map can search the supported place inventory or building addresses and takes the player to the selected street frontage.

## Streets

[street-facilities.json](street-facilities.json) records mapped bicycle facilities on East 9th, East 10th, St. Marks Place, East 12th and Avenue A, and the protected avenue lanes. The Second Avenue treatment also uses [NYC DOT's March 5, 2025 completion report](https://www.nyc.gov/html/dot/html/pr2025/safer-across-manhattan-aves.shtml) for its widened cycle lane and upgraded bus lane in this area.

The accepted road centerlines, widths, navigation bounds and vehicle dynamics remain intact. Markings and lane offsets fit the existing straightened map and are not surveyed dimensions. Illustrative parked cars are omitted from the protected side of East 12th where the current road width cannot accommodate parking, the track and a clear driving lane together. This is a known road-width approximation. Trees and the 235 additional small street objects retain estimated placements.

## Reproduction and review

These commands describe the revision 04 workflow; current scripts include revision 05 schedules. For a present-day authorized edit, follow [the current rebuild order](NEIGHBORHOOD-NOTES.md#rebuild-order). The [clean reproduction verifier](../scripts/verify-neighborhood-reproduction.py) checks current source data in a disposable copy, without replacing the working game exports. Its export-field exclusions and the current browser review are explained in [pass 05](STOREFRONT-PASS-05.md).

No network access or new Python/npm packages are needed to compile the included evidence:

```sh
python3 scripts/prepare-neighborhood.py
python3 scripts/compile-neighborhood-details.py
blender --background -t 6 --python-exit-code 1 --python model-source/build_neighborhood.py
npm run verify
```

Preparation resets derived data; compilation and export must follow it. After an observation-only edit, compile and rebuild affected sections. Repeat `--tile` to choose several sections in one export. The accepted core does not need rebuilding.

Validation includes road and vehicle invariants, model/texture references, source-to-building joins, restored building identities, open courtyard collision and bounded shop partitions. A clean preparation/compilation in an isolated temporary directory was compared with the working manifest. Browser review uses the actual exported GLBs and the app's lighting, with street views across all fourteen sections. These checks do not establish exhaustive visual accuracy or a device-independent frame rate.

Final `npm run verify` passes on Node.js 24.19.0: 2,308 road samples, map spawns, boundary driving, vehicle behavior, local modules, GLBs/textures, municipal joins, courtyard collision and business partition checks. Clean source preparation/compilation reproduces the working geometry, facade schedules, business records and props. All 610 original footprints, road centers/widths/directions and driving bounds are preserved. The core model, core recipe and six licensed reference files are byte-identical to the repository baseline.

The fourteen section GLBs total **48.67 MiB and 8,761,042 triangles**, with at most 46 material batches in a section. They continue to stream by distance; these totals are not a per-frame draw count. Browser review covered all fourteen sections, followed by specific checks of corrected storefronts and the school entrance. Model and texture requests succeeded, with no uncaught exceptions. The vendored loader's pre-existing deprecation warnings remain.

The real map controls successfully searched for Blue & Gold, Smithereens, the school, Boris & Horton and Pastasole; invalid input remained in the dialog with a validation message. Two sequential 180-frame stationary samples at 1440 × 1000 on an Apple M1 / ANGLE Metal measured **30.9 fps near Blue & Gold** (median 33.3 ms, p95 50.1 ms) and **60.0 fps near the school** (median/p95 16.7 ms). Default adaptive quality was enabled, so these are observations of that session, not comparisons at locked quality or a sustained driving benchmark.

The [machine-readable review record](accuracy-review-2026-09-06.json) contains checks, viewpoints and sample conditions. [First Avenue](../docs/images/first-avenue-revision-04.png) and [Blue & Gold](../docs/images/blue-gold-revision-04.png) are actual browser captures. Existing third-party terms and the six licensed photographic files are preserved; see [asset credits](../dist/reconstruction/ASSET-CREDITS.md) and [third-party notices](../THIRD-PARTY-NOTICES.md).
