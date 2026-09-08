# East Village neighborhood expansion — September 6, 2026

**September 8 continuation:** The game starts and resets at First Avenue/East 7th. [Storefront pass 05](STOREFRONT-PASS-05.md) connects 22 individual exterior designs and 26 elevation schedules across nine sections. Its editable source is [storefront-details.json](storefront-details.json); underlying revision 04 records remain separate. The changes are not a complete 1:1 survey. See the current handoff for export, validation and publishing status.

Ten complete city blocks extend from East 7th to East 12th Street, between Second Avenue and Avenue A. Four outer sections provide boundary buildings, including the western side of Second Avenue and the edge of Tompkins Square Park. The original First & 10th model is preserved as the most individually detailed area.

Accuracy revision 04 restores five missing buildings, audits municipal footprint coverage, and brings photographic observations to 410 non-core building objects. All fourteen sections retain recessed facade construction, varied entries/storefronts, masonry surface maps and additional street objects. Read [ACCURACY-PASS-04.md](ACCURACY-PASS-04.md) for the audit, source limitations and reproducible changes. [DETAIL-PASS-03.md](DETAIL-PASS-03.md) records the earlier geometry-only pass.

## What is anchored to evidence

The September 5, 2026 OpenStreetMap snapshot supplies 610 building objects. The September 6 municipal audit adds five missing footprints, yielding 615 objects. All 620 NYC OTI footprint records in the extracted area have explicit matches; PLUTO 26v2 supplies parcel attributes. Five new footprints receive a documented translation into the accepted frame; existing footprints are preserved. Municipal direct matches supplement roof heights, while photographic exceptions remain separate. Objects include annexes and courtyard structures, so the total is not a count of independently verified street facades.

`neighborhood-observations.json` and `neighborhood-facade-audit.json` are the editable observation schedules, containing 459 combined records and 410 distinct non-core buildings with some photographic observation. The compiler joins records to exact building identities, with explicit corner-address and parcel corrections. `neighborhood-references/` and the audit retain dated URLs, image dates where known, historical signage and uncertainty. Many archive photographs have 2012 upload dates and unknown capture dates. No new observation photographs are distributed or used as texture copies.

Photographic coverage varies from a storefront detail to a complete facade. The map distinguishes photo-observed building records; this does not imply every elevation or every visual detail is verified. Unknown facade finishes, windows, cornices, fire escapes, entrances and roof equipment remain estimates, documented in each building's `facadeSpec.inference`. Street dressing and interiors are illustrative. The same inferred escape/window layout is shared across some secondary buildings. This is a developed reconstruction prototype with uneven detail, not a surveyed present-day digital twin.

## Distinct buildings

Custom massing or facade schedules cover the St Nicholas church at Avenue A/10th, Joyce dance center, former PS122, St Stanislaus, St Cyril, former St Mary, St Mark's-in-the-Bowery, Ottendorfer Library, German Dispensary, Orpheum, Village East Cinema, Elizabeth Home, and 171 First Avenue's cast-iron front. Spire heights, roof pitches, setbacks and trim depths without measurements are photographic estimates.

Revision 04 also includes East Side Community School's H-shaped footprint and grouped windows, the completed 45 East 7th replacement building with its patterned brick and setback, and Blue & Gold's small awning and low frontage. Municipal roof heights and photographic story counts are separate evidence; an exposed basement is not automatically an extra full story.

- St Nicholas: separate red-brick masses, Gothic gables, tall Avenue A window, belfry and pyramidal spire. The mapped 31.4 m is the tower top, not a box height.
- Village East: lower pale front wing, raised entrance surround and taller brick rear auditorium. The 23.9 m mapped top belongs to the rear volume.
- 307/309 East 12th: the Elizabeth Home facade spans both mapped parcels. Its western mansard/dormers and eastern stepped gable form one facade. 311 is separate.
- 107 East 7th is the main St Stanislaus church; 101 is a separate rectory. St Cyril at 62 St Marks has no tower.
- St Mary's existing 2025 condition is used; approved conversion proposals are not asserted as completed.
- 131 First Avenue is one story; 171 has three broad cast-iron window bays. 175's visible floors and written total conflict and are retained separately.

## Occupancy

Business sources were checked September 6, 2026; online checks do not establish the photograph capture date or guarantee current occupancy. Unconfirmed tenants are not assigned a new name. Historical architectural photos do not prove a shop remains open.

The Swiss Institute's old St Marks/Second Avenue venue is closed. Orpheum's STOMP text is historical, so its modeled marquee has only the venue name. Blank Street at 149 Avenue A is closed; Barnes & Noble's announced Steiner opening is not modeled as open. The old Beron signage in the preserved core remains explicitly historical. Lucy's, Maya, Baba Doner, The Rabbit and other recent names retain separate dated sources. Shop partitions and sign dimensions are estimates, including the partial units at Lucy's and Danny & Coop's.

The generated `neighborhood-business-audit.json` covers 369 mapped candidates plus reviewed additions: 210 supported names and 167 excluded/unresolved records. September 8 identity corrections remove duplicate Ralph's and Danny & Coop's entries from revision 04's 212-name total. Matching uses exact addresses, mapped positions, municipal identities and individual corrections; each name selects a specific street frontage. Multiple tenants receive estimated separate units. Website address evidence, recent inspections, retail licenses and contrary evidence retain their own dates. A currently reachable website can still be stale: Ferns is excluded because a newer broker listing identifies a former tenant. A name in this inventory does not certify its sign design, partition dimensions or continued operation.

## Roads and presentation

Coordinates use the original First & 10th origin, rotated to the mapped avenue bearing. Roads are straightened approximations within the footprint frame; widths and curb details are estimated. East 9th and St Marks stop at Avenue A. The park beyond is partial boundary context, not a complete park model.

`street-facilities.json` records OSM bicycle facilities and dated DOT evidence for Second Avenue. Cross-street and Avenue A markings are now represented. Lane widths and offsets fit the accepted road approximation; illustrative parking is omitted where it would block the protected East 12th track or the usable driving lane. Vehicle dynamics and driving bounds are unchanged.

The geometry manifest is always available for collision and navigation. Fourteen visual sections use simple distant silhouettes and load detailed meshes within 116 m of a section's bounds; distant sections unload beyond 205 m after a delay. Shared content-addressed textures avoid embedding the same texture in every section. Repeated trees, benches, parked cars and lamps use spatially grouped GPU instances. The original intersection meshes are batched by material at runtime.

The map supports travel by place/address search or map selection, and the physics use the full neighborhood bounds. Vehicle checks cover braking, reverse, frame independence, collision and valid outer lanes. Current browser review uses the actual streamed GLBs with the app's lighting; standalone Blender renders remain a separate presentation. Device frame rate and subjective driving feel require separate measurement and user review.

## Rebuild order

1. `python3 scripts/prepare-neighborhood.py` creates geometry from the included OSM and municipal snapshots and checked-in matches. This resets derived facade/prop data.
2. `python3 scripts/compile-neighborhood-details.py` applies facade observations, address/business evidence, street facilities and deterministic dressing.
3. `blender -b -t 6 --python-exit-code 1 --python model-source/build_neighborhood.py` exports all sections and shared textures. `-- --tile block-3-2` rebuilds one section; repeat `--tile` to select several.
4. Rebuild reusable props only if changed: `blender -b --python model-source/build_street_props.py` and `blender -b --python model-source/build_extra_props.py`.
   Revision 03's bicycle, hydrant, bin, utility-cover and drain-grate kit uses `blender -b --python model-source/build_streetscape.py`.
5. `node scripts/verify-intersection.mjs` and `node scripts/verify-neighborhood.mjs` validate the static project, source modules, GLB resources and meaningful road/vehicle invariants.
6. Optional actual-mesh review: `blender -b -t 6 --python model-source/render_neighborhood.py`. Review output is separate from the site's rendering and is not an AI concept image.

The entire game runs from static files without Google imagery keys or a live map service. The original ten-block export is preserved in the public `rayidali/borough-drive` repository history. Accuracy revision 04 includes the completed detail pass, source evidence and exported assets together. Vercel serves `dist/` from `main` at https://borough-drive.vercel.app.
