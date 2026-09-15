# Seventh, slowly. — Godot browser slice

September 14, 2026. The user deferred a GPU machine and authorized proceeding with available hardware. This playable **Godot 4.7.2 / WebGL 2** driving study runs on the player's device. It includes an authored apricot coupe, four cameras, golden/dusk/rain transitions, a map, original synthesized music/ambience and postcards. The circuit follows First, Second, Seventh and St Marks, now extending Seventh Street through Avenue A with 182 existing building objects, all 82 mapped Seventh frontages and the five preserved First & Seventh corner objects. Revision 02 adds momentum-based drifting, automatic gears and RPM/load audio, shared masonry surfaces, branching leaf trees and street furniture. Revision 03 replaces generic Seventh openings with 76 explicit architectural schedules, retaining six corner/landmark recipes. It corrects the 50/48½ entrances, grouped windows, masonry profiles, physical storefronts without verified lettering and material depth. The full 82-frontage street remains a candidate reconstruction: exact photographic alignment and unresolved details have not been accepted. [Fidelity benchmark](../../model-source/SEVENTH-FIDELITY-BENCHMARK.md).

Run `npm run dev` from the repository root and open **http://127.0.0.1:5173/seventh/**. All runtime assets are included in `dist/seventh/`; playing needs no Godot installation, backend, API key or GPU server. Desktop keyboard play is the tested target. The original ten-block game remains at `/`. This slice has not been pushed or deployed.

| Action | Control |
| --- | --- |
| Accelerate / brake and reverse | W / S or up / down |
| Steer | A / D or left / right |
| Handbrake / drift | Turn and briefly hold Space, release and countersteer to catch the slide |
| Chase → hood → cockpit → overhead | C |
| Look around | Hold right mouse and drag |
| Golden hour → dusk → rain | T or weather buttons |
| Pause / resume | Escape; switching tabs also pauses |
| Return to First & Seventh | R |
| Engine, music and ambience | M or Sound button |
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

Run the pure handling checks with `.tools/godot/Godot.app/Contents/MacOS/Godot --headless --path engine/first-seventh --script res://tests/handling.gd`. Add `--facade-review` after the output-folder argument in the native command for all 82 orthographic elevation captures. These expose the modeled geometry; perspective street/shop captures separately check the playable presentation.

This session used Blender 5.2.1. The exporter reads existing recipes without running the geographic compiler or changing the original game. `assets/slice.json` records input/source hashes, identities, coordinates and generated GLB hashes. `.godot/`, `exports/` and `assets/neighborhood/` are regenerable caches. `dist/seventh/` is the required tracked player package; do not remove or ignore it. `dist/seventh/build.json` identifies the actual shipped bytes and source hashes; `seventh:verify` detects stale exports.

For photographic-camera starting poses, the separately labeled church pose fit and every entrance closeup, run `node scripts/review-seventh-fidelity.mjs renders/seventh-engine-03/fidelity`. See the benchmark for why these captures do not automatically establish a match. The structural architecture checks also run in `npm run seventh:verify`.

For browser testing, start the dev server and an isolated Chromium browser with remote-debugging port 9222, then run `npm run seventh:review`. It drives with real keys, measures actual rendered frames, captures weather/cameras and checks controls, preferences, Retina sizing, tab-switch pause, postcard download, missing-pack Retry and graphics-loss recovery. `?review=1` enables telemetry plus test-only pose/frontage camera commands; ordinary visits omit both. Driving assertions use real keyboard input, not injected velocity. For the native frontage-collision, full-circuit and end-to-end Seventh traversal check:

```sh
.tools/godot/Godot.app/Contents/MacOS/Godot --path engine/first-seventh -- --review-out=/absolute/path/to/review-folder
```

[Revision 03 review](../../model-source/SEVENTH-ENGINE-03.md) and [current checkpoint](../../CODEX-HANDOFF.md) distinguish tests, exact commits and publication. The initial download remains large, about 120.2 MiB before HTTP compression; local startup is not a public-network measurement. Shared-world multiplayer, traffic and 500-user load testing are not implemented. Vercel can serve this static package; hosting bandwidth and a broader device matrix still need testing before launch at that scale.

All original [source credits](../../THIRD-PARTY-NOTICES.md), [architectural observations](../../model-source/NEIGHBORHOOD-NOTES.md) and uncertainty remain applicable. Lofi vertex colors use a shared semantic shader for brick/paint/stone, with six existing Poly Haven CC0 diffuse/normal maps. The engine-only schedule lives under `storefront-details.json.seventhEngine` and is applied by `seventh_street_kit.py` plus `seventh_fidelity_kit.py`; the original storefront schedules/export stay intact. Reference photos are inspection-only, with no new photo pixels bundled. Authored atmosphere is not photographic evidence or fidelity acceptance. The package includes original-code MIT, engine/third-party notices, Damion OFL and geographic attribution. [Unreal streaming](../../model-source/UNREAL-BROWSER-PILOT.md) remains a future GPU option.
