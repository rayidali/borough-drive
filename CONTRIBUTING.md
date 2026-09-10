# Contributing to Borough Drive

Help make these ten East Village blocks more recognizable, comfortable to explore, and reliable to run. Small changes with clear evidence are the easiest to review.

## Start locally

1. Fork the repository and clone your fork.
2. Use Node.js 22 or newer and run `npm run dev`.
3. Open http://127.0.0.1:5173 and explore the area you want to change.
4. Create a branch for your change and run `npm run verify` before submitting it.

No dependency installation is required. Blender is optional unless you are regenerating models. Read [AGENTS.md](AGENTS.md), [CODEX-HANDOFF.md](CODEX-HANDOFF.md), the latest [session log](SESSION-LOG.md), [START-HERE.md](START-HERE.md), and [the neighborhood notes](model-source/NEIGHBORHOOD-NOTES.md) before substantial work. When returning to an existing checkout, inspect its branch, recent commits and working tree before editing; preserve uncommitted work.

The owner accepted First & 7th revision 06 as the minimum completion standard on September 9. [Performance pass 07](model-source/PERFORMANCE-PASS-07.md) preserves the models and improves runtime speed. The later [pass 08](model-source/FIRST-SEVENTH-PASS-08.md) refines this corner using dated Street View observations. Read its report and the handoff for source/publishing state. Planning an economical block/street process comes later; the fidelity backlog does not authorize expansion or unattended jobs.

## Pick a focused change

Good contributions include a facade correction with dated references, a reproducible control bug, an accessibility improvement, or a performance change backed by device measurements. Open an issue first for a new geographic expansion, framework migration, or change to the established First & 10th core.

For a bug report, include the street or map destination, walk/drive mode, reproduction steps, and your browser and device. A screenshot or short recording helps with visual issues. For performance reports, include viewport size, graphics hardware if known, the route tested, and how you measured frame rate.

## Architectural and source changes

- Preserve the accepted First Avenue / East 10th Street core and improve the fidelity of the real neighborhood.
- Record facade observations in `model-source/neighborhood-observations.json` and retain research in `model-source/neighborhood-references/`. Core observations have their own facade and storefront notes.
- Use `model-source/storefront-details.json` for explicit shop designs and per-street elevation controls. It records panels, signs, awnings, furniture, photographic sources and unmeasured dimensions; its geometry components live in `model-source/storefront_detail_kit.py`.
- Consult `model-source/digital-twin-coverage.json` before choosing outstanding work. A source record or supported tenant name does not certify its modeled appearance. A limited contribution must not be described as completing the map-wide 1:1 objective.
- Include the exact building identity or address, source URL, observation, photograph date where known, and any uncertainty. A publication date is not necessarily the image capture date.
- Keep current business checks separate from architectural evidence. Unknown tenants stay unnamed; historical signs stay marked historical.
- Use real reference material. Generated architectural guesses cannot stand in for source photographs or measured facts.
- Preserve photo provenance, OSM identifiers, credits, and license notices. Only add distributed images when their reuse terms permit it, with attribution recorded.

## Model workflow

Keep geometry and facade recipes reproducible in `model-source/`. Include affected exported GLBs and textures with source changes so contributors can run the game without Blender.

Read the [rebuild order](model-source/NEIGHBORHOOD-NOTES.md#rebuild-order) before preparing data. `prepare-neighborhood.py` resets derived facade and prop fields; `compile-neighborhood-details.py` must follow it. Rebuild only affected sections where possible:

```sh
python3 scripts/compile-neighborhood-details.py
blender -b -t 6 --python-exit-code 1 --python model-source/build_neighborhood.py -- --tile block-3-2
npm run verify
```

Run the Blender commands from the repository root with Blender 4.3 or newer. Source signatures detect stale storefront exports; a shared recipe edit may affect every section with a storefront schedule. Regenerate the coverage inventory with `python3 scripts/audit-storefront-coverage.py` after changing compiled designs. `python3 scripts/verify-neighborhood-reproduction.py` checks a clean preparation/compilation and generated audits in a disposable copy without resetting working exports. See [pass 05](model-source/STOREFRONT-PASS-05.md) for the affected-section example and export-field exclusions.

Standalone review renders can go into the ignored `renders/` directory. Keep final evidence and enough source records in tracked files to resume without temporary downloads or browser processes.

## Runtime changes and validation

The active game is `dist/index.html`. Files in `dist/` are editable source and required game assets. Keep the vanilla JavaScript module structure and bundled Three.js unless a migration has been discussed.

Run `npm run verify` for changes to models, roads, controls, module paths, and vehicle behavior. The checks cover asset integrity, exact street-material reproduction, lossless spatial batching, and meaningful road and vehicle invariants. After changing the preserved core export, run `node scripts/prepare-street-materials.mjs` to refresh its startup subset. Use `node scripts/profile-performance.mjs` in an isolated Chrome instance for full-frame rendering and startup measurements; distinguish RAF responsiveness from actual scene redraws when idle. They do not establish visual accuracy or browser performance.

For visible or interactive changes, also open the game and test the affected view or controls. Describe what you actually checked. Screenshots should identify whether they came from the browser or a standalone Blender render.

`scripts/review-first-seventh.mjs` reviews the four corner controls, eight shops, nine elevations, driving/reset and two quality modes. `scripts/review-storefronts.mjs` can review the current explicit storefront/elevation schedule in an isolated Chrome instance; setup is in [pass 05](model-source/STOREFRONT-PASS-05.md). The existing 56-viewpoint review is historical evidence for `63757cb`, not an automatic test result for later edits. New start/reset behavior should be checked in both walk and drive modes.

## Pull requests

Explain the problem and resulting behavior, link related issues or research, and include relevant before/after images. List the checks you ran and any remaining uncertainties. Keep unrelated formatting or model regeneration out of the change.

Refresh the handoff and session log after meaningful milestones. Record the exact gameplay/source commit, local changes, push state and verified live state separately. Keep earlier reports dated; documentation-only commits may follow a gameplay commit without changing its models.

Discuss the work respectfully and keep feedback specific to the proposed change. Original contributions are submitted under the project's MIT license. Third-party material retains its own license and must include its source and required notices; see [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

For the current browser-first work, read [pass 09](model-source/BROWSER-PASS-09.md) and [the block workflow](model-source/BLOCK-WORKFLOW.md). `npm run workflow:verify` tests the offline planner; Python 3 is needed for these optional workflow tools. Worker packets propose edits for one facade and cannot self-accept or publish. The Google API key is not a bulk/derivative-use permission grant.
