# Storefront individuality and close detail

## User direction — October 11, 2026

The user likes the overall First Avenue / St. Marks result but finds its businesses too generic and insufficiently like the originals. They request a **“100×” increase in textures, details, fonts, styles and elements**, naming **Tile Bar** as a reference for how individual a storefront should feel. This is the current quality requirement for businesses across the requested map, including existing work when assigned for refinement. Earlier visual endorsements remain historical. The subsequent [revision 09](../../../SEVENTH-ENGINE-09.md) implements this direction and is user-endorsed for publication as the current working storefront reference. Preserve its individuality and continue evidence-led refinement; endorsement is not a calibrated match or a waiver for generic replacements.

Treat “100×” as a substantial increase in observed, visible fidelity, not a numerical multiplier for polygons, texture resolution, prop counts or spending. A richer generic shop still misses the request. Tile Bar is the user's reference for individuality; neither its present game model nor any uninspected photograph is an accepted detail benchmark. Inspect its actual dated reference views when a storefront implementation/review task calls for it. Do not infer its features from its name or copy its design onto other businesses.

This reference records the requested standard. It does not launch a map-wide rebuild or acquisition job. Follow the active task's bounds and preserve protected work unless a subsequent request includes it.

## Observe and specify each business separately

For every business, record its exact building/face, unit boundaries, target date and dated views. A building with three shops needs three business-level specifications, including below-grade shops and each corner return. Residential access stays separately owned. Use ordinary browser Street View plus permitted supplementary close views where useful; broad elevation images rarely resolve all lettering, fabrics or hardware.

Write a short **identity summary**: the observed combination of shapes, materials, signs and street-edge arrangements that distinguishes this business from its neighbors. Then fill these feature families with source locators, observations, estimates and unresolveds. Mark absent only when the relevant area is visible; a parked vehicle or unreadable image is not evidence of absence. These are inspection categories, not a list of props to add everywhere.

| Family | Record and reproduce when visible |
| --- | --- |
| Storefront composition | Unequal unit widths, door position/recess, projecting bays, transoms, mullion sequence and thickness, stall risers, tile/panel surrounds, shutter tracks and junctions with residential entrances. |
| Shade and canopy | Actual type: fabric awning, rigid canopy, umbrella, retractable frame or none; pitch/curve, projection, thickness, scalloped/straight valance, seams, stripe spacing/direction, side panels, brackets, arms, poles, mounting and observed open/closed state. |
| Sign and lettering | Each fascia, projecting blade, window vinyl, painted panel, neon/tube or illuminated box; exact readable words/case/line breaks, letter shape, stroke weight, width, spacing, baseline, outline/shadow, logo silhouette, colors, backing, mounting, depth and placement. A universal font with a changed business name fails a visibly distinctive sign. |
| Materials and textures | Actual material zones: ceramic/glazed tile, grout, brick, painted or stained timber, metal, stone, fabric and glass; pattern size/orientation, trim edges, finish/roughness and observed wear. Match where materials meet. Uniform flat color, stretched noise and arbitrary grunge cannot stand in for the source surface. |
| Outdoor seating and enclosures | Table shape/top/base, chair profile/material, stools/benches, arrangement and spacing, umbrella/canopy, platform, rails/screens, planters, dining structure, menu board and entry clearance. Match the observed furniture family and layout instead of reusing one patio set along the block. Retain the imagery date for movable/seasonal features. |
| Windows and visible depth | Glass divisions, vinyl placement, blinds/curtains, displays, shelving, visible merchandise/menu layers, lights and depth behind the glass. Include only source-supported visible interior cues; mark deeper interiors unknown. Repeated black or emissive panes are insufficient where the reference shows distinctive layers. |
| Small distinguishing elements | Handles, hinges, kickplates, vents, cables, lamps, security grille, door notices, menu holders, stickers/posters, address support, threshold, planters and other observed fittings. Keep readable source text distinct from unreadable graphics; never invent legibility. |

Record the ordinary connective parts as well as the signature feature. A convincing awning above a generic door/glass strip does not finish the shop. Scope includes every business in the assigned extent; Tile Bar or a few recognizable venues cannot substitute for that coverage.

## Author the differences into the rendered result

Reuse mesh/material mechanics where appropriate, with parameters tied to this storefront's observations. When a component cannot express an observed canopy profile, lettering, furniture shape or layered window, extend it or author a bounded custom piece. Do not flatten the source feature to fit the existing recipe, randomize “variety,” or select a generic style preset and call it individual.

- Use geometry for silhouette, recess/projection, supports, furniture and other depth that changes with viewpoint. Use appropriately scaled authored textures, decals or material detail for lettering, tile/grout, fabric, paint and surface wear. Choose the representation by the visible result and browser cost; a particular technique is not mandatory.
- Match letterforms, not just a font category. Use an appropriate licensed font, custom lettering or authored sign graphic where supported; retain provenance. If the exact typeface or wording cannot be established, record the approximation and visible discrepancy. The interface's Inter font does not define business signage.
- Author texture scale and orientation per material zone; check sharpness at the permitted stopped/orbit/zoom distance. Inspect roughness, transparency, sign illumination and color under readable lighting, then in the game's weather states. Atmosphere must not conceal missing work.
- Retain reproducible sources for bespoke details. The existing exporter/runtime must actually carry the required UVs, materials, texture references, transparency and sign treatment before relying on them. Inspect the imported and served game, not only an authoring render.
- Keep source photographs separate from distributed assets unless their permitted use supports that output. Browser access is not a texture license. Do not replace evidence with generated imagery. No image-generation or paid-media job is implied by this standard.
- Preserve close-view detail while measuring browser cost. Consider shared material resources, atlases, batching and distance-based simplification where effective; these may share implementation without making every storefront look alike. Do not silently remove observed signature features to meet a package or frame-rate target. “100×” grants no automatic budget increase.

## Review at business scale before repeating the approach

For an authorized fidelity pass, finish one representative storefront through source comparison, final-game closeups and obliques before applying a shared approach widely. Use Tile Bar as the named detail reference where relevant to the assigned work; if it is protected/out of scope, use it for comparison and choose an in-scope implementation specimen. A specimen checks the method; it does not reduce the full assignment or require a new approval round for already authorized work.

Review **each business**, even where multiple shops share one facade. Required review evidence includes a readable complete storefront crop, oblique depth and the driving approach, with extra crops for text, furniture or materials that the overview cannot resolve. Save source locators and inspected final-game filenames/package hashes. A captured image is not an inspected comparison.

| Review question | Completion rule |
| --- | --- |
| Does the business match its source composition and identity summary? | Identify source-specific features and their actual rendered counterparts. Correct name/color alone cannot pass. |
| Are canopy, furniture, lettering, materials and window layers individually represented? | Resolve visible mismatches in applicable categories. `Not applicable` needs observed support; missing evidence remains unresolved. |
| Has a shared component erased a real difference? | Compare neighboring storefronts. As a diagnostic, mentally ignore their names: unexplained identical awnings, frames, furniture or material layouts require repair. Real observed repetition is allowed. |
| Do closeups and obliques hold up? | Check texture scale, sign letterforms/mounts, depth, edge joins and small fittings in the served game. Distant driving resemblance alone is insufficient. |
| Is the result complete for the assigned scope? | Every business and its required feature rows has a recorded outcome. Known defining omissions prevent a storefront-detail pass, even when building counts, exports and driving checks pass. |

Return an explicit discrepancy list: source expectation → actual game result → feature/record to repair → remaining uncertainty. Continue actionable repairs within the authorized task and budget. Isolate evidence/component blockers so other assigned work can proceed; do not declare success after a fixed repair count. No invented accuracy percentage or automatic “100× achieved” claim. User endorsement, photographic calibration, runtime correctness and storefront-detail review remain separate outcomes.


### P01 review lesson

Compare the complete sign and entry composition, not just whether each component exists. The first P01 render needed a larger Spirals wordmark, warmer burger-shop paint, an actually open glass leaf with attached hardware, distinct paper/blue menu boards and corrected two-sided pub signage. Source-obscured pavement does not justify adding a generic A-frame; remove invented props. Inspect window end walls and both obliques so shallow displays do not expose the world behind the building. Keep dated sources separate when an older elevation has a superseded business. These are review examples, not templates for the next shops.


## Corner and close-view lessons from P03

Review every business return as its own composition even when it shares a name: separate fascia lengths, shade construction, window divisions, seating and artwork can differ around one corner. A single wraparound business does not authorize identical copies of its primary face. Use one compatible shallow interior shell where storefront glazing turns the corner, and inspect open doors from both sides. Keep observed residential entries independent, including the actual jamb/transom number position and clear step path.

At readable close range, check that letters sit ahead of shade fabric and trim, display objects rest in plausible planes, and vents/rails do not erase murals or entrances. Record fine artwork/letterform approximation instead of claiming exact reproduction. Unique image names and overlapping whole-ground crops are mandatory when multiple business records share a face; a successful capture count must not hide overwritten views. After the first three pilots, ordinary 3–5-face packets leave more room for this review; split larger planning groups before authoring and retain every remaining face.

## Ninth Street access and material review

Shared entrance helpers can introduce unobserved brick reveals, a railing across a real approach, or the wrong grille weave. Compare the complete threshold, step direction, landing, side walls and clear passage with the dated source. Correct these per facade; don't change protected neighbors' defaults. Surface overlays on curved cloth must follow the cloth's subdivisions; a single flat patch can sink behind the canopy despite correct material and winding. Inspect the actual visible fade, seams and lettering from both road and sidewalk.

When a mapped height contradicts clearly observed neighboring rooflines, retain the original source value and record any bounded model-height correction as an estimate with supporting views. Do not turn it into a surveyed measurement or invent an unseen rear roof. Record unresolved tenant lettering explicitly while still reconstructing its visible frontage; a later lease does not identify an earlier photographed shop.

## October 15 observed repair lessons

An illuminated sign can be correctly named yet partly hidden inside its fascia molding. Compare front and both close obliques at readable scale and separate the physical layers. Curved and sloping awnings need both illustration boundaries and glyphs projected onto the cloth. White-painted brick needs paint-level contrast, not exaggerated random masonry color. Preserve the observed difference between upper ornamental balcony spindles and a plain lowest rail. For shops behind sidewalk dining frames, capture inside the enclosure as well as from the road. Keep the frame in the game; correct an obscured comparison camera instead. The [Ninth east report](../../../EAST-VILLAGE-E09-EAST.md) records the actual repairs and dated-source limits.
