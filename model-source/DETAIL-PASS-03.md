# Neighborhood detail pass 03 — September 6, 2026

**Historical report, retained as history.** Counts, export sizes and performance samples below belong to this earlier pass. The current published gameplay/model baseline is `63757cbbb13749584e761e4bf7a8e655f90b1bd4`; [accuracy revision 04](ACCURACY-PASS-04.md) and [storefront pass 05](STOREFRONT-PASS-05.md) followed this work. Shared construction details did not meet the user's request for individual fidelity throughout the map. First & 7th revision 06 is the subsequent local study; read the current [handoff](../CODEX-HANDOFF.md) before resuming.

This pass applies the shared street-level detail system to all fourteen existing visual sections: ten complete blocks and four boundary sections. It regenerates 587 non-core building objects, including annexes and boundary context; 547 of those have mapped street frontages. The accepted First & 10th GLB and its Blender recipe are byte-for-byte unchanged.

## Geometry and presentation

- Windows now occupy openings in the facade skin, with recessed glazing, masonry reveals, nested sash frames, sill drip edges, varied curtains/blinds, and supported AC units.
- Entrances have recessed paneled doors, transoms, thresholds, intercom buttons, hinges, handles, and detailed stoops where the existing schedule specifies them.
- Storefronts retain their sourced names and add transom divisions, shutter housings above the sign fascia, small display cards, and fixings. Interior geometry remains illustrative.
- Service pipes, wall anchors, cables, cornice dentils, and shallow relief add detail at pedestrian scale.
- Bare masonry retains color, roughness and normal textures. Painted masonry keeps the recorded coat color over brick roughness and normal textures. Surface images remain the credited generic Poly Haven assets.
- Road and sidewalk UVs now use physical world scale. The previous runtime ground stretched a single texture across the full neighborhood.
- Five reusable object types add 235 street details: 26 bicycles, 51 hydrants, 45 bins, 37 utility covers and 76 drain grates. Placement is deterministic and illustrative, outside the preserved core and mapped buildings; upright objects stay off the driveable roads.
- Window frames and metalwork receive multisample antialiasing in the offscreen rendering pipeline, with the existing automatic performance fallback disabling it on slower sessions.

## Observation records and inference

[`neighborhood-detail-schedule.json`](neighborhood-detail-schedule.json) separates map-wide estimated construction detail from per-address architectural treatments. It implements details already recorded in `neighborhood-references/cross-streets.json` and `first-ave-photo-addendum.json`: selected East 7th Street window crowns and arched entries, McKinley facade quoins, the bathhouse's entry treatment, and 171 First Avenue's roof rail.

The schedule also resolves three differences between the old simplified facade specifications and their retained research descriptions: 95 East 7th's red masonry, 100 East 7th's buff masonry and simpler lower trim, and the raised entrance at 63 East 7th. These remain interpretations of the dated references, including 2010/2012 photographs, rather than claims of a new current survey.

No new current tenant claims or photo-observed building counts are introduced. Reveal depths, hardware, curtains, hidden surfaces, interior furniture, weathering, utility fittings and street-object positions remain estimates. The six distributed source photographs are unchanged. Additional source images inspected during review are not distributed.

## Reproduce the pass

The commands below record this pass's workflow. At current HEAD, those scripts apply the later schedules too; use the [current rebuild instructions](NEIGHBORHOOD-NOTES.md#rebuild-order) for a new authorized change. Historical captures under ignored `renders/` may not survive a fresh checkout; current durable captures and camera poses are linked in [pass 05](STOREFRONT-PASS-05.md).

Run from the repository root with Python 3 and Blender 4.3 or newer. This pass was built with Blender 5.2.1.

```sh
python3 scripts/compile-neighborhood-details.py
blender --background -t 6 --python-exit-code 1 --python model-source/build_neighborhood.py
blender --background -t 6 --python-exit-code 1 --python model-source/build_streetscape.py
npm run verify
```

For a later isolated facade edit, use the existing `-- --tile block-3-2` option after compiling the detail schedule. The neighborhood builder combines text and geometry by material, so detailed sections contain at most 41 mesh/material batches in this export. All exported models and shared textures are included for running without Blender.

## Verification

`npm run verify` passes, including the existing 2,308 road samples, boundary driving, braking, reverse, collision, frame-rate independence and map-spawn checks. Additional checks cover the fourteen detail revisions, material batch limits, masonry surface maps, all five new compressed prop assets, and valid furniture placements.

The building footprints, street frontages, roads, map extent and drive bounds were compared with the initial GitHub import and are unchanged. The core GLB, core recipe, vehicle simulation, collision module and reference photographic files also match that import exactly.

The detailed section meshes total approximately 49.61 MiB, up from 36.04 MiB, with about 9.32 million triangles across the complete neighborhood. They continue to stream by distance. Static checks establish asset integrity and road/vehicle behavior; they do not establish architectural accuracy or performance on every device.

Six matching browser views were reviewed at Second Avenue/St. Marks, Avenue A/7th, Avenue A/10th, First Avenue/12th, East 9th and East 11th. During this route all fourteen section GLBs, the core and all five new prop files returned HTTP 200. There were no scene/asset-loading errors; the existing RGBELoader deprecation warning remains.

In an isolated Chrome session at 1440 × 1000 using ANGLE Metal on an Apple M1, a 90-frame static sample at the East 11th Street viewpoint measured a median of 16.7 ms and 95th percentile of 16.8 ms both before and after the final pass (approximately 60 fps). This is a short sample from one viewpoint, not a sustained driving benchmark or a guarantee for other devices. Before/after captures and an interactive divider comparison are saved locally in the ignored `renders/detail-pass-03/` directory.
