# Contributing to Borough Drive

Help make these ten East Village blocks more recognizable, comfortable to explore, and reliable to run. Small changes with clear evidence are the easiest to review.

## Start locally

1. Fork the repository and clone your fork.
2. Use Node.js 22 or newer and run `npm run dev`.
3. Open http://127.0.0.1:5173 and explore the area you want to change.
4. Create a branch for your change and run `npm run verify` before submitting it.

No dependency installation is required. Blender is optional unless you are regenerating models. Read [CODEX-HANDOFF.md](CODEX-HANDOFF.md), [START-HERE.md](START-HERE.md), and [the neighborhood notes](model-source/NEIGHBORHOOD-NOTES.md) before substantial work.

## Pick a focused change

Good contributions include a facade correction with dated references, a reproducible control bug, an accessibility improvement, or a performance change backed by device measurements. Open an issue first for a new geographic expansion, framework migration, or change to the established First & 10th core.

For a bug report, include the street or map destination, walk/drive mode, reproduction steps, and your browser and device. A screenshot or short recording helps with visual issues. For performance reports, include viewport size, graphics hardware if known, the route tested, and how you measured frame rate.

## Architectural and source changes

- Preserve the accepted First Avenue / East 10th Street core and improve the fidelity of the real neighborhood.
- Record facade observations in `model-source/neighborhood-observations.json` and retain research in `model-source/neighborhood-references/`. Core observations have their own facade and storefront notes.
- Include the exact building identity or address, source URL, observation, photograph date where known, and any uncertainty. A publication date is not necessarily the image capture date.
- Keep current business checks separate from architectural evidence. Unknown tenants stay unnamed; historical signs stay marked historical.
- Use real reference material. Generated architectural guesses cannot stand in for source photographs or measured facts.
- Preserve photo provenance, OSM identifiers, credits, and license notices. Only add distributed images when their reuse terms permit it, with attribution recorded.

## Model workflow

Keep geometry and facade recipes reproducible in `model-source/`. Include affected exported GLBs and textures with source changes so contributors can run the game without Blender.

Read the [rebuild order](model-source/NEIGHBORHOOD-NOTES.md#rebuild-order) before preparing data. `prepare-neighborhood.py` resets derived facade and prop fields; `compile-neighborhood-details.py` must follow it. Rebuild only affected sections where possible:

```sh
blender -b -t 6 --python-exit-code 1 --python model-source/build_neighborhood.py -- --tile block-3-2
npm run verify
```

Run the Blender commands from the repository root with Blender 4.3 or newer. Standalone review renders can go into the ignored `renders/` directory.

## Runtime changes and validation

The active game is `dist/index.html`. Files in `dist/` are editable source and required game assets. Keep the vanilla JavaScript module structure and bundled Three.js unless a migration has been discussed.

Run `npm run verify` for changes to models, roads, controls, module paths, and vehicle behavior. The checks cover asset integrity and meaningful road and vehicle invariants. They do not establish visual accuracy or browser performance.

For visible or interactive changes, also open the game and test the affected view or controls. Describe what you actually checked. Screenshots should identify whether they came from the browser or a standalone Blender render.

## Pull requests

Explain the problem and resulting behavior, link related issues or research, and include relevant before/after images. List the checks you ran and any remaining uncertainties. Keep unrelated formatting or model regeneration out of the change.

Discuss the work respectfully and keep feedback specific to the proposed change. Original contributions are submitted under the project's MIT license. Third-party material retains its own license and must include its source and required notices; see [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
