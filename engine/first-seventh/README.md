# Paused Godot experiment

September 14, 2026. This directory contains an **incomplete, untested** Godot look-development experiment begun before the user clarified that they want Unreal in the browser, with an eventual target of approximately 500 concurrent independent players. Implementation here is paused. There is no playable new game, working car controller, weather system or completed camera system in this directory.

Follow [the Unreal browser pilot plan](../../model-source/UNREAL-BROWSER-PILOT.md) and [the current handoff](../../CODEX-HANDOFF.md). Do not treat these shaders or export files as evidence of Unreal performance or accepted visual quality.

The temporary export cache in `assets/neighborhood/` is ignored by Git. Reproduce it with `blender -b -t 4 --python-exit-code 1 --python model-source/export_seventh_engine.py` from the repository root. `assets/slice.json` records identities, coordinates, source hash and generated file hashes. Original browser GLBs remain included under `dist/` and are unchanged. Export success is not an engine-import or visual test.

All original [source credits](../../THIRD-PARTY-NOTICES.md), [architectural observations](../../model-source/NEIGHBORHOOD-NOTES.md) and source-specific limitations remain applicable. These material experiments are authored color treatments, not new photographic evidence.
