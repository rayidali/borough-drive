# Borough Drive source, build and review adapter

Read before implementation or technical review. Source relationships were rechecked during the September 23 revision 07 pass. Commands describe the authorized build/review workflow; they do not assign another street or a background job. Use the current handoff for exact completed tests and package hashes.

**Protected baseline:** east-block [revision 07](../../../SEVENTH-ENGINE-07.md), source `098f1cc89b41c2067fe1577ddb62df5a3b3c6002`, is user-endorsed and published through guidance release `4b999cd` and checkpoint `78aa716`. The current session is closed; the commands below apply only to a later assigned task. It preserves the [interface contract](../../../INTERFACE-PASS-05.md), west block, accepted corner and audio. Use the current handoff for actual source/save/deployment state; the earlier interface-only publication is historical.

## Follow the real source chain

| Responsibility | Source / consumer | Practical rule |
| --- | --- | --- |
| Existing geography and stable IDs | [neighborhood.json](../../../../dist/reconstruction/neighborhood.json), [build_neighborhood.py](../../../build_neighborhood.py) | Preserve mapped footprints, IDs and the accepted frame. Do not run the legacy compiler to prepare an engine-only detail pass. |
| Engine-only observed detail | [storefront-details.json](../../../storefront-details.json), `seventhEngine` | Top-level legacy `elevations/frontages` serve a different export. Extract assigned records with a JSON parser instead of rewriting the entire large file. |
| Effective elevation | [seventh_street_kit.py](../../../seventh_street_kit.py), `apply_seventh_schedule()` | Merge `seventhEngine.elevations` with `observedGroundCorrections`; raw architecture alone can show obsolete doors/windows. |
| Ground/access geometry | [seventh_fidelity_kit.py](../../../seventh_fidelity_kit.py) | `architecture.observedGround` replaces low openings/doors independently, can add areaways and suppress duplicate old exteriors. Register replacement openings before wall infill. |
| Shop geometry | `seventhEngine.frontages`, `seventh_street_kit.py`, [storefront_detail_kit.py](../../../storefront_detail_kit.py) | Join `buildingId` → `businessId` → `frontageIndex`; `span` belongs to that exact face and `design.panels` fractions sum to one. |
| Street/site detail | [west-seventh-observations-04.json](../../../west-seventh-observations-04.json), [streetscape report](../../../WEST-SEVENTH-STREETSCAPE-04.md), [runtime street data](../../../../engine/first-seventh/assets/west_seventh_streetscape.json), [street_detail.gd](../../../../engine/first-seventh/scripts/street_detail.gd) | Preserve explicit observed placement and dated construction states. Building GLBs alone do not implement this scope. |
| Engine model export | [export_seventh_engine.py](../../../export_seventh_engine.py) → `engine/first-seventh/assets/neighborhood/` and [slice.json](../../../../engine/first-seventh/assets/slice.json) | GLBs are reproducible caches; `slice.json` records their hashes/positions. Partial export requires valid unaffected cached inputs. |
| Browser export | [export-seventh.mjs](../../../../scripts/export-seventh.mjs), [engine README](../../../../engine/first-seventh/README.md) | Import first, export into staging, write credits and content/source hashes. Tracked `dist/seventh/` is required playable output. |
| Runtime presentation | [world.gd](../../../../engine/first-seventh/scripts/world.gd), [weather.gd](../../../../engine/first-seventh/scripts/weather.gd), [HUD](../../../../engine/first-seventh/scripts/hud.gd), [shell](../../../../engine/first-seventh/web/shell.html) | Preserve material semantics, camera inspection, address bounds, controls and browser behavior while adding detail. |

Two concrete precedence checks: 63/Kinka (`241822202`) uses a right/east basement shop and distinct raised entry; 81/Abraço (`241822329`) uses the effective left/west residential door, not the old raw central-door record. Trace the final values before editing. A generic old business exterior may need suppression to avoid duplicate shop geometry.

## Revision 07 source and review lessons

- `architecture.observation` is an object with `sources` and `unknown`, not free text. Add dated facts without discarding earlier provenance or limits.
- `replaceWindows` removes raw windows below 3.55 m. If a corrected parlor row starts at 3.15 m, put it in `groundOpenings`; a correct-looking raw schedule can still export a blank row. Verify the effective renderer and a full-elevation image.
- Street View's displayed camera address is not the property identity. Check neighbors, facade boundaries and mapped face direction. Long corner parcels need overlapping views: the 109 Avenue A record also owns the Seventh 130 entrance/Titi’s section. Number placement belongs to a specific opening or plaque, not a universal header.
- Existing fixed count assertions can encode a source-reading error. Change them only with recorded reinspection and an actual rendered comparison; the April views corrected 116/118/120 to four bays and Yuca to five uneven stacks.
- The original `storefront_detail_kit.py` participates in legacy source signatures. Put engine-only extensions in `seventh_fidelity_kit.py` and prove protected GLB hashes unchanged instead of recompiling the original map to silence verification.
- New door options (`labelPlate`, `labelOffset`, `labelDepth`, `archedLeaves`, fixed-part materials), angled oriels and dated sheds are opt-in. Keep defaults byte-identical for accepted work. Site 108 is separate runtime geometry in `east_seventh_detail.gd`; building counts cannot stand in for its review.
- A browser observation ledger may be included in exported source hashes. Freeze observations before the release build and store subsequent rendered-review outcomes in a separate review directory so reporting does not silently stale the player.

## IDs, coordinates and material semantics

Join by stable numeric building ID and specific frontage, never display address alone. Preserve negative `-177966` (73–75), fractions such as `48½`/literal `48 1/2`, and avenue-addressed corner faces. A new street may have more than one face per building; building ID alone is insufficient ownership there.

The facade helper's tangent is `(rx, rz)` and outward normal `(-rz, rx)`. Architectural `at`, `width` and shop `span` generally express frontage fractions; heights/depths are generally meters. Check the actual consumer for each field rather than extrapolating by name. Annotate face start/end and which screen side they represent; “left” in an image is not automatically geographic west.

The current engine export shifts `z = source_z − 228`. Photo-camera conversion also rotates geographic bearings. Areaway `runtimeCenter` is shifted, while the embedded `frontage` retains source coordinates. Do not apply the shift twice or copy these constants onto a different street without checking its frame. Check the road/pavement plane and collision cut against the resulting opening.

The exporter retains material categories through vertex colors, including a semantic alpha channel for painted/illuminated surfaces. Do not strip that channel or replace all materials with a flat generic shader to reduce size. Preserve recesses, glass ordering, open grating and sign visibility in the actual engine, not just Blender.

## Before adapting to another street

This repository does **not** yet contain a generic automatic street-production pipeline. The old [block workflow](../../../BLOCK-WORKFLOW.md) is an offline inventory/packet proposal, not an engine dispatcher. Its historic price/model examples are not current costs or a tested cheaper-model result.

For the newly authorized street, prepare an adapter plan with its exact IDs/faces and inspect these coupled assumptions before building:

| Assumption to review | Current Seventh behavior |
| --- | --- |
| Export selection | Hardcoded circuit bounds plus every literal `East 7th Street` frontage |
| Schedule/render dispatch | Seventh-named namespace and literal street selection; some per-building exceptions |
| World placement | Origin shift, slice bounds, road/pavement and ground-void transforms |
| Runtime coverage | Collision/street geometry, culling/minimap and address HUD explicitly bounded to Second Avenue–Avenue A, hiding at First Avenue and endpoint intersections |
| Evidence capture | Seventh reference ledger, panorama conversions, facade lookup and camera routes |
| Verification | Fixed 182 buildings / 82 Seventh frontage expectations and named corner invariants |
| Preservation and output | Accepted core/corner and old game must stay intact; distinguish supported new scope from unchanged context |

Extend the smallest necessary source/adapter within the user's requested engine scope. Do not rewrite the engine, turn all fixed assertions off, or merely change test counts to make unsupported geometry pass. Establish new scope assertions and representative camera/road checks while retaining the old ones. Flag a necessary larger architectural change with a concrete bounded proposal; ordinary adaptation already implied by an authorized street implementation does not need repeated approval.

## Future build sequence

Run from repository root. Use installed tool paths from the engine README; do not invent a new installation or download assets just to read this skill.

```sh
# Inspect and record state/protected hashes before editing.
git status --short --branch
git log -5 --oneline

# Example only: re-export this particular Seventh building after its data edit.
# Replace the ID with an assigned supported ID; repeat --only for more IDs.
blender -b -t 4 --python-exit-code 1 --python model-source/export_seventh_engine.py -- --only 241829643

# Import and rebuild the served package after model/runtime edits.
npm run seventh:build
npm run seventh:verify
npm run verify
```

`--only` requires all unaffected GLBs to exist with current input hashes. A changed shared recipe invalidates those hashes; the exporter deliberately rejects the partial rebuild. Then assess the shared change and perform the required full slice export **without `--only`**, followed by protected-output comparisons. Do not bypass the stale-cache check. Rebuilding the supported slice is different from regenerating the original ten-block game or authorizing new geography.

Do not regenerate music for a facade edit. Do not edit cached GLBs as the only source of a change. Native captures before import can show old geometry; use the build/import step first. Check source → effective record → GLB → Godot import → package → served bytes when the scene disagrees with a patch.

## Future review commands and their limits

Start `npm run dev`. Browser review uses a separate Chromium review profile with CDP on port 9222; follow the engine README and installed browser setup, leaving the user's normal browser alone. Use a new task-owned output folder, then save relevant game captures and reports durably before handoff.

The focused camera/address runners explicitly foreground their review tab; camera gestures wait for the loading overlay to hide. Preserve these readiness checks: September 21 review encountered a hidden-tab startup timeout and an input transport timeout. Distinguish a test/browser startup failure from a failed game assertion before editing gameplay to repair it.

```sh
# Existing First–Second scope: reference-camera starts, elevations, closeups.
node scripts/review-seventh-fidelity.mjs renders/street-review/fidelity "" model-source/west-seventh-reference-04.json

# Existing browser behavior/recovery, independent camera, bounded address checks.
npm run seventh:review
npm run seventh:camera-review
npm run seventh:address-review

# Existing isolated nine-sample performance route.
node scripts/review-seventh-performance.mjs renders/street-review/performance
```

The fidelity script saves images and hashes; it does not acquire sources or inspect/accept results. A building filter does not filter ledger panorama captures. Its old no-ledger path uses raw architecture doors for some closeups: prefer the effective bounded ledger and inspect framing. A new street requires an adapted ledger/camera route; the sample command above only reviews Seventh.

For native circuit/collision or elevation checks, use the engine README's `--review-out=/absolute/path/...` command and optional `--facade-review`. Use actual output paths, never the placeholder. Handling, camera and address test scripts also live under `engine/first-seventh/tests/`. Run relevant checks for changed behavior; an unrelated documentation edit requires no game rebuild or runtime suite.

Pause other rendering/export work during performance tests. Record device, browser, viewport, DPR, render scale, weather, route, cache conditions, sample duration, frame behavior, contacts/errors and package bytes. Revision 04's historical short M1 / 8 GB / 1440×1000 / DPR 1 samples averaged 60 FPS at full scale, with 5.341 s local ready time and an 82.49 MiB PCK. Earlier captures had a different FPS ceiling; run a same-environment baseline before claiming a speedup/regression.

The later interface review measured 8.23 s startup and 39.1–53.8 FPS with adaptive scale reaching 0.75 on its intermediate package. Final interface PCK is 87,390,432 bytes. Those figures are not an A/B against revision 04; the [interface report](../../../INTERFACE-PASS-05.md) separates intermediate full-suite evidence from final layout/camera/address checks. Use the actual current package for a new baseline rather than inheriting historical frame-rate claims.

The existing benchmark targets ≥60 FPS, no more than 10% mean regression and PCK below 100 MiB for the current slice. These are project targets, not a promise that the whole map fits the same package budget. A larger authorized scope needs explicit streaming/package planning, not silent detail deletion or an unsupported capacity claim. Global material sharing helped the last pass; a 48 m spatial-bucket change increased draw calls and was reverted. Measure an optimization rather than assuming it helps.

## Preserve and identify the final result

Compare assigned changed IDs and out-of-scope assets/records against the frozen baseline. Use [revision 04 preservation evidence](../../../engine-review-2026-09-15-04/preservation.json) as a pattern. `seventh:verify` confirms protected IDs exist; it does not itself prove their old GLB hashes remain unchanged. Check protected First & Seventh models, original core/geography/namespaces and unrelated controls/audio independently.

`dist/seventh/build.json` records shipped file sizes/hashes and source hashes. **Its current `sourceCommit` is inherited from `slice.json` and hardcoded geographic baseline `c76dccebc143960498d21eeab8c55c2d0dbcc5ce`, not the checkout HEAD or revision 04 gameplay commit.** Record the gameplay/source save separately using Git. Use content hashes to identify what was exported and tested. This corrects older README/checkpoint prose; no manifest/code change was made for this documentation task.

The deployed routing contract is `/` → `dist/seventh/index.html`, `/index.html` → `dist/legacy.html`, direct `/seventh/` preserved. Keep `dist/index.html` absent because filesystem precedence bypasses the root rewrite. Preserve the shell's `/seventh/` base path. A shell-only edit still changes shipped `index.html` and its source hash: keep `build.json` synchronized and run verification. Do not change the manifest merely to disguise a stale binary; rebuild when its actual sources changed.

Report local save, push and verified live deployment separately. Only publish when the current user instruction authorizes it. Credits and provenance remain required. Saving this skill creates no background work, source-acquisition permission or new route.


## First Avenue–Avenue A revision 06 example

The [east-block report](../../../SEVENTH-ENGINE-06.md) and [inventory](../../../east-seventh-coverage-06.json) are the implemented example for 35 editable + two protected frontages. They are not an accepted photographic template. Use `east-seventh-reference-06.json` with the existing fidelity capture script; its 37 whole-elevation and 52 overlapping ground views are diagnostic, with no calibrated source poses.

The effective ground layout can come from `seventhEngine.observedGroundCorrections`, replacing `architecture.windows`/`doors`. Inspect both before editing access or counting openings. Engine-only `addressOverride` corrects mapped identity without mutating the preserved geographic source. `businessOverrides` can activate only an already mapped Seventh POI with explicit supporting source IDs. `architecture.returnShops` assigns a corner business's Seventh face separately from its avenue face; it must not overlap an independent residential door.

Opt-in pointed/ogee openings, church profiles, corbelled cornices, balcony geometry, solid awning valances and worn tread edges express observed differences. Their defaults preserve the accepted west/corner models. Compare all model hashes after a shared recipe change, not just assigned IDs. Revision 06 left the 108 site unresolved. Revision 07 subsequently inspected and modeled its visible gated/planted street edge; the hidden rear building and complete curb-fixture placement remain gaps. A new source ledger must not automatically mark them accepted.

Partial rebuilds must take review-camera heights from the verified exported building records. A revision 06 check caught eight cached facades reverting to old source heights in `reviewFrontages` during `--only`; the exporter now uses the retained model heights and verification asserts equality. This affects review framing, not building geometry. Verify full and partial exports produce equivalent review records.

For runtime street details, `world.batch_details()` currently consumes only direct `MeshInstance3D` children of `geometry`. A named identity-transform site group can accidentally bypass that path and add hundreds of draw calls. Move only its static meshes into the existing batch input (preserving transforms/materials), keep collision nodes intact, and measure the actual final package. Do not replace global batching with spatial buckets without evidence.

A browser can be visible but OS-unfocused during automated reload. Revision 07 recorded a loading watchdog timeout followed by eventual engine readiness. The browser harness holds focus during ordinary work and disables that emulation for the explicit focus-loss check. Preserve failures, and use `node scripts/review-seventh.mjs OUT --recovery-only` to repeat independent settings/recovery checks after completed driving checks; report both result files and their exact package hashes.
