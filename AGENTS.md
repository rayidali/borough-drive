# Working on Borough Drive

Read `CODEX-HANDOFF.md`, the latest entry in `SESSION-LOG.md`, `START-HERE.md`, and `model-source/NEIGHBORHOOD-NOTES.md` before substantial work.

## Session checkpoints

- On resuming, inspect the current branch, recent commits, and `git status --short --branch` before editing. Compare them with the latest checkpoint and preserve any uncommitted work.
- Honor the latest user review/pause state in the checkpoint. An unfinished fidelity backlog or an older document's suggested next work does not override an explicit pause. September 8's published pass is awaiting user review; the current request is to save documentation, not to resume modeling.
- After meaningful milestones, during long tasks, and before a planned handoff, refresh the current checkpoint in `CODEX-HANDOFF.md` and add a dated entry to `SESSION-LOG.md`. Keep earlier entries as history; use the log's template. Save progress during the session so an unexpected closure does not lose all context.
- Record the user's objective and decisions, exact gameplay/source commit, local changes, push status, deployment status, checks actually performed, unresolved issues, and the next concrete step. A local commit, a push to `main`, and a verified live deployment are separate states; record unknown or pending states explicitly.
- Use Git history to identify the checkpoint documentation's own commit. Do not repeatedly amend a checkpoint just to insert its own commit hash. Never store credentials in checkpoint files or rely on temporary files, chat history, running processes, or old tool session IDs as the only way to resume.

## Project constraints

- This is an existing ten-block East Village reconstruction. Preserve the accepted First Avenue/East 10th Street core and improve the real neighborhood's fidelity and cozy presentation.
- The user's quality target applies across the entire requested map: shop layouts, neon/projecting signs, boards, outdoor seating, paint, proportions and architectural details. Do not silently replace that scope with a selected-shop pass. Shared components must express observed features; a supported business name, photographic record, successful export or gap report is not proof that a facade is complete or 1:1.
- The active game is `dist/index.html`. Files under `dist/` are editable source and required game assets; do not delete or ignore that directory as build output. `dist/prototype.html` is an older generic prototype.
- The project uses vanilla JavaScript modules and vendored Three.js. Keep the current structure unless a requested change calls for a migration. No npm dependencies are needed to run the export.
- Use `npm run dev` to serve the game locally and `npm run verify` after changes that affect models, roads, controls, module paths, or vehicle behavior. Report what was actually verified; these checks do not establish visual accuracy or frame rate.
- Keep geometry and facade recipes reproducible in `model-source/`. Update observation records and provenance when making evidence-based changes. Use dated sources for present-day business claims and keep uncertain details explicit.
- For individual storefronts/elevations, use `model-source/storefront-details.json` and `storefront_detail_kit.py`; consult `digital-twin-coverage.json` for remaining work. Keep the core's separate reference records intact. Distinguish source-photo inspection, modeled geometry and matched-view review in progress reports.
- Preserve all third-party credits, license notices, and photographic provenance. Do not replace real architectural reference images with generated guesses or claim inference is a measured fact.
- Rebuild only affected models when possible. Existing GLBs and textures are included so the game can run without Blender.
- Keep GitHub and Vercel credentials local to the user's computer. Do not embed tokens in code, documents, remotes, or logs. The current repository and hosting configuration are recorded in the handoff; check the existing setup before creating another repository or project.
- Follow the user's current request for scope and publishing. Do not assume this handoff requests a deployment or a new citywide expansion.
- Keep current instructions and historical reports distinct when updating Markdown. Refresh README/control/version information and cross-links as needed, preserve dated history and all license notices, and point readers to the current handoff for the next authorized action.
