# East Village neighborhood expansion — September 6, 2026

Ten complete city blocks extend from East 7th to East 12th Street, between Second Avenue and Avenue A. Four outer sections provide boundary buildings, including the western side of Second Avenue and the edge of Tompkins Square Park. The original First & 10th model is preserved as the most individually detailed area.

## What is anchored to evidence

The September 5, 2026 OpenStreetMap snapshot supplies 610 building objects, footprints, supplied heights, mapped addresses and building types within the area and boundary context. Missing height/story values are flagged as estimates. Mapped building objects include annexes and courtyard structures; 610 is not a count of independently verified street facades.

`neighborhood-observations.json` is the editable observation schedule. The compiler joins these records to exact mapped building identities, including explicit corner-address and split-parcel corrections. The full research records in `neighborhood-references/` retain observations, dated source URLs, image dates where known, historical signage and uncertainty. No new observation photographs are distributed or used as texture copies.

Photographic coverage varies from a storefront detail to a complete facade. The map distinguishes photo-observed building records; this does not imply every elevation or every visual detail is verified. Unknown facade finishes, windows, cornices, fire escapes, entrances and roof equipment remain estimates, documented in each building's `facadeSpec.inference`. Street dressing and interiors are illustrative. The same inferred escape/window layout is shared across some secondary buildings. This is a developed reconstruction prototype with uneven detail, not a surveyed present-day digital twin.

## Distinct buildings

Custom massing or facade schedules cover the St Nicholas church at Avenue A/10th, Joyce dance center, former PS122, St Stanislaus, St Cyril, former St Mary, St Mark's-in-the-Bowery, Ottendorfer Library, German Dispensary, Orpheum, Village East Cinema, Elizabeth Home, and 171 First Avenue's cast-iron front. Spire heights, roof pitches, setbacks and trim depths without measurements are photographic estimates.

- St Nicholas: separate red-brick masses, Gothic gables, tall Avenue A window, belfry and pyramidal spire. The mapped 31.4 m is the tower top, not a box height.
- Village East: lower pale front wing, raised entrance surround and taller brick rear auditorium. The 23.9 m mapped top belongs to the rear volume.
- 307/309 East 12th: the Elizabeth Home facade spans both mapped parcels. Its western mansard/dormers and eastern stepped gable form one facade. 311 is separate.
- 107 East 7th is the main St Stanislaus church; 101 is a separate rectory. St Cyril at 62 St Marks has no tower.
- St Mary's existing 2025 condition is used; approved conversion proposals are not asserted as completed.
- 131 First Avenue is one story; 171 has three broad cast-iron window bays. 175's visible floors and written total conflict and are retained separately.

## Occupancy

Business sources were checked September 6, 2026; online checks do not establish the photograph capture date or guarantee current occupancy. Unconfirmed tenants are not assigned a new name. Historical architectural photos do not prove a shop remains open.

The Swiss Institute's old St Marks/Second Avenue venue is closed. Orpheum's STOMP text is historical, so its modeled marquee has only the venue name. Blank Street at 149 Avenue A is closed; Barnes & Noble's announced Steiner opening is not modeled as open. The old Beron signage in the preserved core remains explicitly historical. Lucy's, Maya, Baba Doner, The Rabbit and other recent names retain separate dated sources. Shop partitions and sign dimensions are estimates, including the partial units at Lucy's and Danny & Coop's.

## Roads and presentation

Coordinates use the original First & 10th origin, rotated to the mapped avenue bearing. Roads are straightened approximations within the footprint frame; widths and curb details are estimated. East 9th and St Marks stop at Avenue A. The park beyond is partial boundary context, not a complete park model.

The geometry manifest is always available for collision and navigation. Fourteen visual sections use simple distant silhouettes and load detailed meshes within 116 m of a section's bounds; distant sections unload beyond 205 m after a delay. Shared content-addressed textures avoid embedding the same texture in every section. Repeated trees, benches, parked cars and lamps use spatially grouped GPU instances. The original intersection meshes are batched by material at runtime.

The map supports travel to a nearby driveable road, and the physics use the full neighborhood bounds. Vehicle checks cover braking, reverse, frame independence, collision and valid outer lanes. No browser gameplay/performance measurement was requested or performed; actual frame rate depends on the device. Asset review uses imported exported GLBs in standalone Blender renders with separate lighting.

## Rebuild order

1. `python scripts/prepare-neighborhood.py` creates geometry from the included mapped snapshot. This resets derived facade/prop data.
2. `python scripts/compile-neighborhood-details.py` applies observations and deterministic street dressing.
3. `blender -b -t 6 --python-exit-code 1 --python model-source/build_neighborhood.py` exports all sections and shared textures. `-- --tile block-3-2` rebuilds one section.
4. Rebuild reusable props only if changed: `blender -b --python model-source/build_street_props.py` and `blender -b --python model-source/build_extra_props.py`.
5. `node scripts/verify-intersection.mjs` and `node scripts/verify-neighborhood.mjs` validate the static project, source modules, GLB resources and meaningful road/vehicle invariants.
6. Optional actual-mesh review: `blender -b -t 6 --python model-source/render_neighborhood.py`. Review output is separate from the site's rendering and is not an AI concept image.

The entire game runs from static files without Google imagery keys or a live map service. The complete source and render assets stay with the Site project, ready for a later user-authorized transfer to Rayid's own GitHub repository. No GitHub account was used for this expansion.
