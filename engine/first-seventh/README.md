# Seventh, slowly. — Godot browser slice

September 14, 2026. The user deferred a GPU machine and authorized proceeding with available hardware. This playable **Godot 4.7.2 / WebGL 2** driving study runs on the player's device. It includes an authored apricot coupe, four cameras, golden/dusk/rain transitions, a map, original synthesized music/ambience and postcards. The circuit follows First, Second, Seventh and St Marks, reusing 154 existing building objects, including all five First & Seventh corner objects.

Run `npm run dev` from the repository root and open **http://127.0.0.1:5173/seventh/**. All runtime assets are included in `dist/seventh/`; playing needs no Godot installation, backend, API key or GPU server. Desktop keyboard play is the tested target. The original ten-block game remains at `/`. This slice has not been pushed or deployed.

| Action | Control |
| --- | --- |
| Accelerate / brake and reverse | W / S or up / down |
| Steer / brake | A / D or left / right; Space |
| Chase → hood → cockpit → overhead | C |
| Look around | Hold right mouse and drag |
| Golden hour → dusk → rain | T or weather buttons |
| Pause / resume | Escape; switching tabs also pauses |
| Return to First & Seventh | R |
| Music and ambience | M or Sound button |
| Save a game-view postcard | P |
| Hide interface / fullscreen | H / F |

## Rebuild and verify

Editing/exporting needs Godot 4.7.2. The local Mac setup uses `.tools/godot/Godot.app/Contents/MacOS/Godot` and official `web_nothreads_debug.zip` / `web_nothreads_release.zip` templates in `.tools/godot/templates/`. Obtain the matching [official build/templates](https://github.com/godotengine/godot-builds/releases/tag/4.7.2-stable). Set `BOROUGH_GODOT` to another executable if needed, and adjust the two custom-template paths in `export_presets.cfg` for that installation. Do not commit machine-specific absolute paths.

```sh
# Only if the ignored geometry cache is absent or source geometry changed:
blender -b -t 4 --python-exit-code 1 --python model-source/export_seventh_engine.py

# Only when changing the authored audio recipe:
python3 model-source/make_seventh_audio.py

# Import, export into staging, include licenses and record package/source hashes:
npm run seventh:build
npm run seventh:verify
npm run verify
```

This session used Blender 5.2.1. The exporter reads existing recipes without running the geographic compiler or changing the original game. `assets/slice.json` records input/source hashes, identities, coordinates and generated GLB hashes. `.godot/`, `exports/` and `assets/neighborhood/` are regenerable caches. `dist/seventh/` is the required tracked player package; do not remove or ignore it. `dist/seventh/build.json` identifies the actual shipped bytes and source hashes; `seventh:verify` detects stale exports.

For browser testing, start the dev server and an isolated Chromium browser with remote-debugging port 9222, then run `npm run seventh:review`. It drives with real keys, measures actual rendered frames, captures weather/cameras and checks controls, preferences, Retina sizing, tab-switch pause, postcard download, missing-pack Retry and graphics-loss recovery. `?review=1` enables read-only telemetry; ordinary visits omit its sampler. For the native frontage-collision and full-circuit check:

```sh
.tools/godot/Godot.app/Contents/MacOS/Godot --path engine/first-seventh -- --review-out=/absolute/path/to/review-folder
```

[Measured review](../../model-source/SEVENTH-ENGINE-01.md) and [current checkpoint](../../CODEX-HANDOFF.md) distinguish tests, exact commits and publication. The initial download remains large, about 102 MiB before HTTP compression; local startup is not a public-network measurement. Shared-world multiplayer, traffic and 500-user load testing are not implemented. Vercel can serve this static package; hosting bandwidth and a broader device matrix still need testing before launch at that scale.

All original [source credits](../../THIRD-PARTY-NOTICES.md), [architectural observations](../../model-source/NEIGHBORHOOD-NOTES.md) and uncertainty remain applicable. Lofi vertex colors replace the original surface-texture treatment in this experiment; authored atmosphere is not new photographic evidence or fidelity acceptance. The package includes original-code MIT, engine/third-party notices, Damion OFL and geographic attribution. [Unreal streaming](../../model-source/UNREAL-BROWSER-PILOT.md) remains a future GPU option.
