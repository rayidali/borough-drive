# Seventh quality: observable requirements and review

Read when observing, modeling or reviewing a facade. This standard transfers the method and level of attention, not Seventh Street's shop names, colors or dimensions.

## Fixed reference and honest acceptance

The September 21 user endorses the current Seventh build as the desired project direction. Reference geometry/gameplay is `d4fbafe9a6af4497de81e2220d31c878f930612e`; subsequent routing fix is `bfbc8d764f838708f753a53de9b7f054101b45f0`. Use the current checkpoint for later changes. The saved revision 04 PCK SHA256 is `15b96df07f67a66862794ed1bff06f8f0a48a3d95644a82b368577134b8a81fe`.

The [revision 04 report](../../../SEVENTH-ENGINE-04.md), [coverage ledger](../../../west-seventh-coverage-04.json) and [capture manifest](../../../engine-review-2026-09-15-04/visual-captures.json) are the evidence index. Forty-one inspected source images and 39 reviewed elevations do not imply 39 exact replicas. No calibrated multi-view pass is recorded. Some captures are diagnostic poses, not matched photographs; not every captured perspective was inspected.

Two review levels must remain distinct:

| Level | What may be claimed | Required record |
| --- | --- | --- |
| Seventh visual-standard candidate | Individually reconstructed, source-guided, reviewed to the endorsed visual direction, with listed limits | Per-feature review, game views, preservation/runtime results, explicit mismatches and reviewer recommendation; user acceptance only if actually given |
| Stricter photographic acceptance | Passed the project's specified photo-comparison gates for named views/features | Calibrated independent views, zero known count/type/identity errors, recorded measurements and reviewer decision under agreed criteria; see the benchmark |

Do not describe a candidate with an unresolved required detail as “all minute details complete.” A good overall scene can be useful and user-endorsed while finer accuracy remains open. Neither level establishes surveyed world dimensions.

## Visual grammar to preserve

The saved game combines warm, restrained lighting with recognizable individual masonry facades, varied opening rhythms, physical recesses/projections, readable business/address identities, ironwork and layered street edges. Surface roughness and mortar/tile scale make walls distinct; their colors should still read under golden, dusk and rain settings. Trees and street furniture connect buildings to the pavement, with enough space to understand entrances.

Keep atmospheric softness in lighting and color, while retaining architectural edges and material identity. Avoid turning every wall orange, every opening into black glass, every building into a regular grid or every shop into a bright sign rectangle. Detail is strongest when it changes silhouette, depth, proportions and recognizable arrangement. Driving views establish the scene; close camera inspection exposes the craft. Both must hold up.

## Three source-to-result examples

These are **existing game captures**, not photographs and not independently accepted 1:1 exemplars. Review the cited source records before copying a feature. The remaining mismatches are part of the lesson.

| Case | Distinctions to learn | Saved render and limits |
| --- | --- | --- |
| 50 East 7th, building `241829575` | Asymmetric facade; three-light left/two-light right upper groups; separate oak double entrances at grade; right entry has columns, layered stone arch, fanlight and transom; individual inscription, address, notice case and service fittings | [Entrance view](../../../../docs/images/seventh-engine-04/fidelity/frontage-241829575-perspective-1.png). Exact carving, panel sizes, stone scale and lettering remain estimates. The Street View camera label “49” does not identify the building being viewed. |
| 48½ East 7th, building `241829643` | Separate residential entrance left of shop; single operable glazed leaf with fixed left sidelight; literal `48 1/2` label; white shop fascia/brackets; angled projecting display bays and recessed door; open metal benches, shaped upper hoods and fire escape | [Shop perspective](../../../../docs/images/seventh-engine-04/fidelity/frontage-241829643-perspective-2.png), [whole elevation](../../../../docs/images/seventh-engine-04/fidelity/frontage-241829643-elevation.png). Bay depth is not a flat window decal. Proprietary lettering, exact hoods/cornice and hidden threshold details are not certified. |
| 63 East 7th / Kinka | Raised residential entry, separately arranged lower openings and right/east basement shop; differing rail/gate paths; trees and street edge positioned against actual facade landmarks | [Street view](../../../../docs/images/seventh-engine-04/fidelity/63-close-0.png), [observations](../../../west-seventh-observations-04.json). Keep the shop/access side correct; do not infer invisible basement geometry from a name. Tree occlusion requires another view for review. |

Compare neighboring examples rather than averaging their layouts. The intended transfer is “identify this building's actual structure,” not “give every new building these details.”

## Feature checklist: inspect, specify, render, compare

Each row needs evidence, model location, actual review and remaining uncertainty in the packet. Use `not-applicable` only with a reason. Unknown does not mean absent. For repeated windows, record floor rows and exceptions compactly; do not hide variation behind a generic total count.

| Feature family | Details to record and inspect | Typical failure to catch |
| --- | --- | --- |
| Identity and extent | Building ID, geometric face/segment, street side, neighbors, fraction/range/address spelling, corner return, lot boundary and adjoining wall | Copying camera label, sorting addresses into the wrong parcels, dropping negative IDs or joining by rounded house number |
| Mass/silhouette | Facade width, street-facing height, exposed floor count, ground datum, setback, party-wall return, roof/parapet, chimney/tower/dormer, cornice silhouette | Using a parcel's highest roof point as the whole front; merging neighboring buildings; changing accepted footprints to fit one photo |
| Floor/bay rhythm | Every floor's opening order, unequal spacing/widths, grouped bays, blank wall areas, lintel/sill levels, mezzanine or basement distinction | Uniform seeded window grid, correct total count on wrong floors, treating a basement as a full upper floor |
| Window anatomy | Actual opening shape, sash count, vertical mullions, horizontal/transom rails, frame width/color, reveal depth, sill projection, hood/keystone/arch shoulders, grille/guard, observed AC and blind placement | Arch ornament over a rectangular opening, masonry covering glass, floating trim, decorative/random AC masquerading as observation |
| Doors and small hardware | Residential/service/shop role; side/order; leaf count and operable versus fixed panel; width, height, recess; panel/glazing arrangement; fanlight, transom, arch, columns; handle, intercom, bell, number plate | Two leaves where one leaf and sidelight exist, wrong side entry, lost fraction, adding a generic door below every shop sign |
| Access and basement | At grade/raised/sunken; visible tread count, direction, landing and threshold; separate stair down; areaway opening, retaining wall, gate, handrail/rail returns and safe pavement edge | Obsolete stoop, invented ramp, stairs into solid wall, basement storefront accidentally sealed by pavement, render hole without protective collision |
| Shop divisions | Unit boundaries and residential separation; stall riser/panels, framing sequence, glazing, recess, bay angles, transom, shutters, awning profile/valance/supports, entry path | One huge glass strip for several shops, backing plane in front of deep glazing, hidden entrance, business evidence mistaken for physical dimensions |
| Lettering and signs | Exact legible words, case, accents, fractions and line breaks; sign mounting, projection, orientation, scale, supports, border, illumination and neighboring layers | Correct name in wrong place/font; reversed face; awning hiding sign; z-fighting; generated guesses at illegible letters |
| Wall/ornament | Material zones and transitions; brick bond and mortar scale; tile size/grout; stone base, rustication, courses, lintels, pilasters, capitals, brackets, cornice layers, relief silhouette and depth | Texture stretched across stories, arbitrary weather noise, missing cornice depth, generic arches substituted for unique profiles |
| Fire escapes and services | Side/bay alignment, platform levels and width, grating/open spaces, railing topology, stair direction, drop ladder, wall brackets; standpipes, vents, lights and visible cables | Solid slabs replacing open grating, floating stairs, escape blocking the modeled door, unexplained extra ladders |
| Pavement/street edge | Curb and grade continuity, pavers/slabs/seams, tree pit position, rail/fence, fixed bench/bike rack, hydrant, poles/signs, drain/utility covers, bollards and curb ramps | Evenly spaced decorative clutter, duplicated corner fixture ownership, impossible access or collision path |
| Temporary/dated features | Construction fences/scaffolds/sheds, bracing, vacant edge, salvaged material, dining enclosure, movable boards/tables/chairs/bicycles and seasonal planting | Proposed work drawn as completed; mixing years into an asserted current snapshot; adding a station because one exists nearby |
| Roof/side/hidden parts | Visible return details and exposed roof equipment; enumerate occluded/unseen areas separately | Claiming rear/roof completion from one frontal image; inventing an interior to imply source coverage |
| Atmosphere/experience | Material identity in neutral/readable view and three weather states, camera readability, smooth movement, continuous accessible street presentation | Darkness/bloom/trees concealing mismatches; visual polish used as evidence of accurate geometry |

## Evidence discipline that changes the model

Record capture date separately from webpage publication date and retrieval date. A dated business source supports identity/occupancy, not every facade feature. Label existing-condition versus proposed architectural drawings. Keep mixed-date exceptions explicit when no single complete current source exists. A new present-day claim needs fresh evidence; do not automatically reuse September 2026 claims forever.

Find full and adjacent/oblique views before assuming a truck/tree hides nothing important. Retain durable source identifiers, view coordinates/crops and observed facts using the permitted storage method. Do not export observation photos as facade textures unless their permitted use specifically supports that output. The private user screenshot stays local. Generated images cannot replace architectural evidence.

A reusable component may encode geometry mechanics, but its floor count, opening order, dimensions, material zones, access and signs come from the individual record. Dimensional estimates need a basis (such as a footprint or relative photo ratios) and uncertainty. Avoid false precision: an authored `0.035` geometry parameter is not proof of a measured 35 mm feature.

## Review gates

1. **Coverage:** account for every assigned feature and every full-scope inventory item. A source count, schema pass or list of business names cannot pass this gate.
2. **Identity/count/type:** compare per-floor openings, leaves, access type, storefront partitions and legible labels. Known mismatches require repair or an explicit unresolved state; they cannot disappear into an average score.
3. **Proportions/depth:** use full elevation plus independent obliques to check silhouette, spacing, recesses, bay projections, stairs, cornices and corner joins. Include readable entry/sign closeups. Check wall infill, sign occlusion and glazing order in the actual renderer.
4. **Photographic comparison when claimed:** calibrate a comparable camera with at least four stable facade landmarks and verify a second view; save pose/FOV/resolution and annotations. An orthographic elevation or copied panorama heading is not calibrated acceptance. The benchmark's 1.5% mean / 3% maximum / 1% entrance image-width errors are **proposed project thresholds, not user-approved limits or external standards**. Report measurements and their basis; do not award a stricter pass against silently invented tolerances.
5. **Appearance/play:** inspect golden/dusk/rain and driving approaches without hiding architecture; use detailed/neutral views as needed for diagnosis. Street objects/access must join pavement coherently and preserve driving/collision behavior.
6. **Independent review and final bytes:** compare the final package against sources and this checklist, not just the worker's description. Record who/what reviewed which views, failures, unresolveds and exact hashes. If a later cosmetic change follows performance testing, retain the tested hash and qualify applicability; do not relabel old tests.

Use the [repository adapter](repository-adapter.md) for actual checks. Separate visual acceptance, runtime correctness and performance. The [strict benchmark](../../../SEVENTH-FIDELITY-BENCHMARK.md) retains the complete photographic target; this guide does not certify the existing build or authorize new work.
