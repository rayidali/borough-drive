# Seventh, slowly. — DriveAround.nyc Godot browser slice

**Current published state — September 21, 2026.** This playable **Godot 4.7.2 / WebGL 2** driving study runs on the player's device. It includes an authored apricot coupe, four cameras, golden/dusk/rain transitions, a map, original synthesized music/ambience and postcards. The circuit follows First, Second, Seventh and St Marks, now extending Seventh Street through Avenue A with 182 existing building objects, all 82 mapped Seventh frontages and the five preserved First & Seventh corner objects. Revision 02 adds momentum-based drifting, automatic gears and RPM/load audio, shared masonry surfaces, branching leaf trees and street furniture. Revision 03 replaces generic Seventh openings with 76 explicit architectural schedules, retaining six corner/landmark recipes. It corrects the 50/48½ entrances, grouped windows, masonry profiles, physical storefronts without verified lettering and material depth. The full 82-frontage street remains a candidate reconstruction: exact photographic alignment and unresolved details have not been accepted. [Fidelity benchmark](../../model-source/SEVENTH-FIDELITY-BENCHMARK.md). Revision 04 adds the First–Second block corrections, DriveAround.nyc branding, camera inspection and a bounded live address display. [Engine report](../../model-source/SEVENTH-ENGINE-04.md) and [west Seventh coverage ledger](../../model-source/west-seventh-coverage-04.json) distinguish visual review from photographic acceptance. Interface source/runtime `b194dc6` and publication checkpoint `533570e` are published; exact CI, deployment and package evidence are in the [handoff](../../CODEX-HANDOFF.md).

Run `npm run dev` from the repository root and open **http://127.0.0.1:5173/** (the same build is also at `/seventh/`). All runtime assets are included in `dist/seventh/`; playing needs no Godot installation, backend, API key or GPU server. Desktop keyboard play is the tested target. The original ten-block game remains at `/index.html` in the deployed site. Vercel root promotion is configured in `vercel.json`.

**September 21 interface pass:** a compact bottom launch panel replaces the oversized left introduction. The loading screen, HUD and pause menu use bundled Inter, charcoal/sage surfaces and the supplied logo. Start/Enter begins; Escape → Controls reveals the full input guide. UI pixels follow the actual browser viewport so labels stay readable on a small laptop; the existing Retina rendering cap remains. [Interface report and actual browser evidence](../../model-source/INTERFACE-PASS-05.md). Architecture remains revision 04; no model or audio source changed. Publication status is recorded separately in the [handoff](../../CODEX-HANDOFF.md).

On the bounded East 7th Street run between First and Second Avenues, the HUD places the nearest mapped frontage address beside the speedometer. It follows the authored footprint edges in `assets/slice.json`, holds changes briefly at frontage boundaries and hides the address at intersections, on other streets or when the vehicle heading is not aligned with Seventh.

| Action | Control |
| --- | --- |
| Accelerate / brake and reverse | W / S or up / down |
| Steer | A / D or left / right |
| Handbrake / drift | Turn and briefly hold Space, release and countersteer to catch the slide |
| Chase → hood → cockpit → overhead | C |
| Camera inspection | Right-drag orbit/look · Shift + right-drag or middle-drag pan around the car and up toward roofs · wheel zoom |
| Golden hour → dusk → rain | T or weather buttons |
| Pause / resume | Escape; switching tabs also pauses |
| Full keyboard/mouse guide | Escape, then Controls; Tab navigates pause actions |
| Return to First & Seventh | R |
| Recenter camera inspection | V (keeps the selected camera mode) |
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

Run the pure handling checks with `.tools/godot/Godot.app/Contents/MacOS/Godot --headless --path engine/first-seventh --script res://tests/handling.gd`; the bounded address behavior can be checked with the same command and `res://tests/address_locator.gd`; camera input/state checks use `res://tests/cameras.gd`. Add `--facade-review` after the output-folder argument in the native command for all 82 orthographic elevation captures. These expose the modeled geometry; perspective street/shop captures separately check the playable presentation.

This session used Blender 5.2.1. The exporter reads existing recipes without running the geographic compiler or changing the original game. `assets/slice.json` records input/source hashes, identities, coordinates and generated GLB hashes. `.godot/`, `exports/` and `assets/neighborhood/` are regenerable caches. `dist/seventh/` is the required tracked player package; do not remove or ignore it. `dist/seventh/build.json` identifies the actual shipped bytes and source hashes. **September 21 correction:** its `sourceCommit` currently inherits the hardcoded geographic baseline `c76dccebc143960498d21eeab8c55c2d0dbcc5ce` from `slice.json`; it is not the checkout HEAD or current gameplay save. Record the actual gameplay Git commit separately in the handoff and use content hashes for tested package identity. `seventh:verify` detects stale exports.

For a future street, read the [portable reconstruction skill](../../model-source/skills/reconstruct-street/SKILL.md), especially its repository adapter: the exporter, runtime details, review cameras and fixed scope assertions are Seventh-specific. Changing a street name alone does not extend this pipeline correctly. Remaining small-icon/legacy branding and calmer, louder music have a separate [experience brief](../../docs/DRIVEAROUND-EXPERIENCE-BRIEF.md); those items remain separate from the published interface pass, and no next street is assigned.

For all bounded source-camera starts, whole elevations and overlapping street closeups, run `node scripts/review-seventh-fidelity.mjs renders/seventh-engine-04/fidelity "" model-source/west-seventh-reference-04.json`. The revision 03 invocation without a ledger retains the separately labeled church pose fit. See the benchmark for why these captures do not automatically establish a match. The structural architecture checks also run in `npm run seventh:verify`.

For the same nine performance samples without repeating behavioral/recovery checks, run `node scripts/review-seventh-performance.mjs renders/seventh-engine-04/performance`. Keep other game/native renderers and build jobs stopped during measurement.

For browser testing, start the dev server and an isolated Chromium browser with remote-debugging port 9222, then run `npm run seventh:review`. It drives with real keys, measures actual rendered frames, captures weather/cameras and checks controls, preferences, Retina sizing, tab-switch pause, postcard download, missing-pack Retry and graphics-loss recovery. `npm run seventh:camera-review` tests all four inspection modes, camera-only recentering and car-transform preservation. `npm run seventh:address-review` is a shorter address/branding pass covering both avenue edges, both sides of the inner block, the 48 1/2 frontage and St Marks clearance. `?review=1` enables telemetry plus test-only pose/frontage camera commands; ordinary visits omit both. Driving assertions use real keyboard input, not injected velocity. For the native frontage-collision, full-circuit and end-to-end Seventh traversal check:

```sh
.tools/godot/Godot.app/Contents/MacOS/Godot --path engine/first-seventh -- --review-out=/absolute/path/to/review-folder
```

[Revision 04 review](../../model-source/SEVENTH-ENGINE-04.md) and [current checkpoint](../../CODEX-HANDOFF.md) distinguish tests, exact commits and publication. The initial download remains large, about 120.6 MiB before HTTP compression; local startup is not a public-network measurement. Shared-world multiplayer, traffic and 500-user load testing are not implemented. Vercel can serve this static package; hosting bandwidth and a broader device matrix still need testing before launch at that scale.

All original [source credits](../../THIRD-PARTY-NOTICES.md), [architectural observations](../../model-source/NEIGHBORHOOD-NOTES.md) and uncertainty remain applicable. Lofi vertex colors use a shared semantic shader for brick/paint/stone, with six existing Poly Haven CC0 diffuse/normal maps. The engine-only schedule lives under `storefront-details.json.seventhEngine` and is applied by `seventh_street_kit.py` plus `seventh_fidelity_kit.py`; the original storefront schedules/export stay intact. Reference photos are inspection-only, with no new photo pixels bundled. Authored atmosphere is not photographic evidence or fidelity acceptance. The package includes original-code MIT, engine/third-party notices, Damion OFL and geographic attribution. [Unreal streaming](../../model-source/UNREAL-BROWSER-PILOT.md) remains a future GPU option.
