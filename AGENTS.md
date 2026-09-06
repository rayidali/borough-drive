# Working on Borough Drive

Read `CODEX-HANDOFF.md`, `START-HERE.md`, and `model-source/NEIGHBORHOOD-NOTES.md` before substantial work.

- This is an existing ten-block East Village reconstruction. Preserve the accepted First Avenue/East 10th Street core and improve the real neighborhood's fidelity and cozy presentation.
- The active game is `dist/index.html`. Files under `dist/` are editable source and required game assets; do not delete or ignore that directory as build output. `dist/prototype.html` is an older generic prototype.
- The project uses vanilla JavaScript modules and vendored Three.js. Keep the current structure unless a requested change calls for a migration. No npm dependencies are needed to run the export.
- Use `npm run dev` to serve the game locally and `npm run verify` after changes that affect models, roads, controls, module paths, or vehicle behavior. Report what was actually verified; these checks do not establish visual accuracy or frame rate.
- Keep geometry and facade recipes reproducible in `model-source/`. Update observation records and provenance when making evidence-based changes. Use dated sources for present-day business claims and keep uncertain details explicit.
- Preserve all third-party credits, license notices, and photographic provenance. Do not replace real architectural reference images with generated guesses or claim inference is a measured fact.
- Rebuild only affected models when possible. Existing GLBs and textures are included so the game can run without Blender.
- Keep GitHub credentials local to the user's computer. Do not embed tokens in code, documents, remotes, or logs. This export has no preconfigured GitHub connection or original hosting identity.
- Follow the user's current request for scope and publishing. Do not assume this handoff requests a deployment or a new citywide expansion.
