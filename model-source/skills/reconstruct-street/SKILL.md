---
name: reconstruct-street
description: Reconstruct or refine bounded Borough Drive streets and individually detailed storefronts using dated visual evidence, reproducible geometry/materials, and business-level rendered review. Use for street planning, implementation, AI work packets, or reconstruction-quality review. Follow the user's current quality direction and geographic scope.
---

# Reconstruct individual streets and storefronts

This is a repository-local, model-independent skill. Read it as ordinary Markdown in any assistant with access to this repository; no plugin, provider API, paid coordinator or installed skill loader is required. Keep its `references/` folder beside it. Repository links assume this location.

**October 11 storefront feedback takes precedence:** the user likes the overall local revision 08 but says businesses still look like cookie-cutter blocks. They request a “100×” step up in textures, lettering/fonts, styles, awnings/shades, outdoor seating and small details, naming Tile Bar as the reference for individuality. Read [storefront individuality](references/storefront-individuality.md) for every storefront planning, implementation or review task. Reconstruct each business's observed design; changing a name/color on a shared shop template is insufficient. Existing revisions are baselines to improve, not proof that this stronger storefront target is met. The subsequent “revise it now” request authorized the actual bounded [revision 09](../../SEVENTH-ENGINE-09.md); the user then endorsed it (“yes this is great”) and explicitly requested publication to `main`. Use revision 09 as the current working storefront example while retaining its exact-font/artwork and photographic-acceptance limits. See the current handoff for verified release state; no additional street is assigned.

**Historical September 23 saved workflow and session close:** the user endorsed the First Avenue–Avenue A browser-reference result and explicitly requested pushing it to `main`/production. The [revision 07 report](../../SEVENTH-ENGINE-07.md) and [observation ledger](../../east-seventh-browser-07.json) retain actual inspection and uncertainty; publication and checkpoint `78aa716` passed CI/Vercel, and the current handoff records exact live checks. The closing task changes documentation only; resume from the user’s next bounded instruction. Revision 04 remains the west-block visual reference, and revision 07 is the user-endorsed east-block example. Preserve the compact interface and audio. No additional street is assigned.

## Establish the task

1. Read repository [AGENTS.md](../../../AGENTS.md), the current [handoff](../../../CODEX-HANDOFF.md), latest [session log entry](../../../SESSION-LOG.md), [start instructions](../../../START-HERE.md) and [neighborhood notes](../../NEIGHBORHOOD-NOTES.md). Inspect `git status --short --branch` and recent commits; preserve uncommitted work. Read only historical reports needed for the task.
2. Record mode (`plan`, `implement`, `review`), named street/end intersections, both sides, corner returns, date policy and exclusions. A street name without endpoints is insufficient for implementation: prepare the inventory, then clarify that boundary. Specify how far each avenue return extends; mark ambiguous returns unresolved instead of including adjacent avenue blocks. Do not silently expand to the whole street or reduce it to recognizable shops.
3. For a complete street, inventory every facade, residential entrance, basement/business, vacant/site edge, street segment and intersection fixture. Give each feature one owner. Keep hidden roofs/returns explicit; they cannot inherit acceptance from a front view.
4. Read [the visual standard and review gates](references/quality-standard.md) and, for any business frontage, [storefront individuality](references/storefront-individuality.md). For code/build work, also read [the repository adapter](references/repository-adapter.md). Copy [the work packet](references/work-packet.md) for each bounded unit, preserving a separate specification for every business within it. If IDs or references are not established, use its scope-bootstrap route first. These are reading routes, not instructions to execute every referenced command.

## What the standard means

The user endorsed revision 04's overall quality on September 21. Preserve its individual architecture, credible depth/materials, precise access/shop distinctions, calm atmosphere and playable browser performance. This is a usable visual reference now; it does **not** require waiting for a new 1:1 certificate before any later authorized work.

The October 11 feedback raises the storefront requirement beyond that historical baseline. Broad facade resemblance and coverage counts do not establish business-level fidelity. Each shop needs its own observed composition, sign letterforms, shade construction, surface patterns, furnishings, visible display layers and fittings, inspected at close range and in approach views. “100×” describes the requested qualitative leap, not a measured score or an asset-budget multiplier.

It is not an exact survey or a fully calibrated photographic template. The saved west-block 39-record ledger has source/elevation review for all records and zero calibrated multi-view passes. The [stricter benchmark](../../SEVENTH-FIDELITY-BENCHMARK.md) remains a separate target. Do not copy its remaining mistakes or upgrade its acceptance labels. No instruction file guarantees identical results from every model, image set or effort setting: the review gates supply the missing feedback.

## Execute one bounded unit

1. **Identify and inspect.** Use the preferred browser-reference workflow below within the assigned source/budget scope. Confirm the subject by neighbors and footprint, not the camera-address label. Inspect full elevation, oblique depth and entrance/sign details; seek an adjacent view for occlusions. If vision/source access is unavailable, prepare a `needs-evidence` packet instead of inventing observations. Existing source URLs/metadata are not proof of fresh inspection or permission for automatic ingestion.
2. **Transcribe before coding.** Fill the packet's feature rows: each floor's openings, doors/access, storefront divisions, lettering, masonry/ornament, materials, roof/returns and street details. For each business, add its identity summary and detailed shade, signage/letterform, material/texture, seating, display and hardware rows. Separate observed facts, dimensional estimates and unknowns. Count bays and leaves explicitly. Record an exact supporting image/view for each consequential feature.
3. **Map to source.** Identify the correct building + geometric face, effective schedule and code consumer. Draw a local horizontal/vertical/depth coordinate key. Reuse components only when their parameters express this particular building. Plan a bounded component extension for unsupported distinctive shapes. Do not turn Seventh-specific scripts into a new-street pipeline by changing only a name.
4. **Build and inspect.** Modify reproducible source, export the affected scope where supported, import/rebuild the browser package, then inspect the actual result. Work from silhouette to floor/bay rhythm, access/shop geometry, signs/materials, small fixed details and atmosphere. All remain required; ordering controls rework, not scope. A successful export cannot close a feature row.
5. **Repair from evidence.** Review complete elevations, both oblique directions, readable entry/sign crops and the driving approach. Apply the business-level individuality gates: compare the actual material scale, lettering, shade/furniture anatomy and visible layers for every shop, including differences between neighbors. Pair discrepancies with a source and exact parameter. Check source, effective record, model, import and served package before changing geometry to fix an apparently stale result. Never distort a building to compensate for a bad comparison camera.
6. **Verify and save.** Run relevant structural, preservation, browser and performance checks described in the adapter. Record source/package hashes and every check actually performed. Save a durable packet/checkpoint with remaining mismatches and the next action. `captured`, `inspected`, `modeled`, `reviewed` and `accepted` are different states.

## Preferred reference workflow: Street View in the browser

On September 23 the user explicitly credited ordinary browser Street View inspection for revision 07's improved result and asked that this method guide future work. **Prefer it for visual research on an authorized street when available.** The successful example covers every property, including residential entries, corner returns and the 108 site, rather than only named shops. This is a project preference supported by one user-endorsed pass, not a tested guarantee of equal quality or lower cost for every model.

- Start with the complete property/face inventory. Navigate the ordinary Street View interface and actually inspect each facade; use overlapping ground-level views for long buildings and neighboring panorama positions for parked-car/tree occlusions. A search result or panorama metadata alone is not visual evidence.
- Record a durable Maps/panorama locator, imagery capture month/year, inspection date, identity anchors and view direction. Separate the photograph's date from the day it was inspected. The [revision 07 ledger](../../east-seventh-browser-07.json) is the worked example; its April imagery does not establish September conditions.
- Transcribe opening counts and divisions, door leaves/sidelights, stoops/basement access, shop boundaries, signs, scaffolds and visible fixtures before modeling. For each property number, record the actual text and support surface: door leaf, meeting stile, fanlight, plaque, lintel or storefront glass. Leave unreadable/hidden placements unresolved.
- Use architectural archives, official records or another dated view to resolve gaps; keep disagreements and estimates explicit. Author reproducible geometry from the observations, then compare the final game's full elevations, closeups and obliques with the inspected references. Preserve the discrepancy/repair record.
- Keep source rights and permitted storage separate from browser access. Retain locators and observations durably; this pass distributes game captures, not Street View pixels or photographic textures. This preference does not start a paid API job, billing change, bulk acquisition or new street automatically.

## Economical worker/reviewer loop

One worker receives one elevation plus its connected access/shop and street edge, the required views, a small relevant source extract, component interfaces and an explicit file/record allowlist. An unusual landmark may need its own packet. The coordinator retains the complete street inventory so small packets do not shrink the final scope.

Do not feed every worker the entire JSON schedule or all historic session logs. The coordinator reads project context once; a worker needs the applicable constraints, exact baseline hashes and relevant records/images. Preserve unchanged accepted work. Serialize shared-file integration and exports; independent observations can run in parallel.

Use a separate review pass against the same evidence and rendered bytes. It can use the same inexpensive model in a fresh context; it must not merely repeat the worker's prose. Start future qualification with one ordinary facade, one complex/access case and one corner/street edge. Compare omissions, repair time and actual usage before assuming the workflow is cheaper. Qualification is proposed work, not an evaluation performed by this documentation task.

Continue focused, actionable repairs within the user's task and budget until the assigned review requirements are met. A fixed repair count cannot establish completion. If evidence or a component blocks progress, save `needs-evidence`, `needs-component` or `needs-review`, explain the specific issue and continue independent assigned work. Avoid repeated whole-street rebuilds without a diagnosed discrepancy. Respect the user's budget; do not invent prices, change model settings or submit paid jobs from these instructions.

## Deliver a reviewable result

- Complete scope inventory with no silently omitted property or street feature.
- Dated evidence, per-feature observations/estimates, reproducible source and narrow change list.
- Full/oblique/detail captures of the final package, discrepancy decisions and preservation/performance evidence.
- Per-business identity and feature records with actual close-view comparisons; explicit failures for generic substitutions or missing defining details.
- Honest coverage states, unresolved details, exact next step and refreshed project checkpoint.

Keep the original ten-block map, First & 10th core and accepted First & 7th corner protected unless the current request explicitly includes a change. Keep `/` on Seventh, `/index.html` on the legacy game and `dist/index.html` absent. Preserve source rights, credits and private imagery. Implementation authorization does not imply publishing, DNS changes, wider geography or unattended jobs.

## Copyable next-session instruction

> Read `model-source/skills/reconstruct-street/SKILL.md`, its storefront-individuality reference and the current project checkpoint. Plan **[street, from intersection, to intersection]**, both sides and corner/street details. Preserve the architectural baselines while applying the October 11 requirement for substantially richer, individually observed businesses; Tile Bar is the named individuality reference, not a template to clone. Prepare the complete inventory and first bounded work packet with a separate detail specification for every shop. Keep unresolved details explicit. Do not implement or publish yet.

For a later implementation request, replace the final two sentences with the actual authorized implementation scope and budget. Do not run placeholder commands or treat a sample prompt as a new user instruction.
