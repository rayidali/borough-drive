# Borough Drive: continuation context

## Current checkpoint — 2026-09-08-03 (local pass verified and saved)

Recorded **2026-09-08T17:26:41-04:00**. Latest task: start at First Avenue/East 7th and improve the entire existing neighborhood toward a digital twin, including observed signs/neon, boards, outdoor seating, colors, openings, proportions and architectural details. Tiny real-world details matter. Preserve First & 10th. Assess Blender versus an engine; no migration or publication requested.

| Item | Checkpoint state |
| --- | --- |
| Current gameplay/source | `63757cbbb13749584e761e4bf7a8e655f90b1bd4` on local `main` |
| Session baseline | Gameplay `835ea6cb53f7b88ebc0edc9586080f9c371b9d20`; documentation HEAD `5753989`; initial checkout clean |
| Completed local pass | Start/reset at First & 7th, northbound. 22 individual shop designs, 26 elevation schedules, 29 source records, nine rebuilt GLBs, walking furniture collision, font/license, source/review scripts and durable browser captures. See [storefront pass 05](model-source/STOREFRONT-PASS-05.md). |
| Local changes | Gameplay, models, evidence, review records and scripts committed. Checkpoint documents saved in a separate documentation commit; use Git history below to identify it. No pending model export or known failing check. |
| Remaining fidelity | Of 200 supported non-core names, 178 still have estimated shop designs. All 641 non-core street frontages are inventoried in [digital-twin-coverage.json](model-source/digital-twin-coverage.json). Partial photo evidence does not certify a 1:1 twin. |
| Push state | New local commits not pushed; `origin/main` was not fetched this session. Cached remote remains `5753989`. |
| Deployment | No new deployment; prior production verification was `835ea6c` on September 6. Current live state not checked this session. |
| Validation | Final `npm run verify` passed on Node 24.15.0. Clean prepare/compile and three generated audits matched. Actual Chrome review: 56 viewpoints, correct start/northbound driving/both resets, zero uncaught errors or failed HTTP responses. Python parsing and staged whitespace checks passed. |
| Preservation | Core GLB/recipe, vehicle module and six licensed photographs byte-identical to `835ea6c`. All 615 footprint/height records, roads and driving bounds preserved. |
| Engine decision | Keep Blender for authored assets and Three.js for the browser. A future dense-scan desktop application could evaluate Unreal; changing renderers cannot supply missing survey evidence. |
| Next concrete step | Continue along First Avenue from East 7th toward St Marks, choosing outstanding frontages from the coverage inventory. Obtain dated full/oblique views, exact sign artwork and facade/opening dimensions; extend explicit shop/elevation schedules, rebuild affected sections and compare matching viewpoints. |

Exact dimensions, complete contemporary photography, many sign outlines/material samples and unseen details remain unavailable. This verified local pass does not complete the user's map-wide 1:1 objective. Some review views are partly occluded by trees/parked cars. The browser's existing automatic quality adjustment disabled ambient occlusion; no frame-rate benchmark was performed. Detailed results, hashes and camera poses are in [storefront-review-2026-09-08.json](model-source/storefront-review-2026-09-08.json). Existing licenses/photos remain intact.

The previously published complete revision 04 is `835ea6c`. The new local pass is `63757cb`; it is not on production. Package version `0.4.0` and the page's chapter label alone are insufficient to identify a deployment; compare its actual files/manifest with the intended gameplay commit. Documentation commits may follow that commit.

### Resume a session

1. Read this checkpoint, the latest [session log entry](SESSION-LOG.md), [START-HERE.md](START-HERE.md), and [neighborhood notes](model-source/NEIGHBORHOOD-NOTES.md). Read the [accuracy audit](model-source/ACCURACY-PASS-04.md) before changing neighborhood models or evidence.
2. Inspect the actual checkout without discarding changes:

   ```sh
   git status --short --branch
   git log -5 --oneline
   git log -1 --format="%h %cI %s" -- CODEX-HANDOFF.md SESSION-LOG.md
   ```

3. If remote state matters, fetch `origin` and compare it with the checkout before changing branches or pulling. Local `origin/main` can be stale. Record any uncommitted files or unpublished commits before continuing.
4. Use `npm run dev` to open the game locally when needed. A previous session's server, browser, authentication, or `/tmp` files may no longer exist. All required game assets and reproducible source are in the repository; no Blender rebuild is needed to resume.
5. Follow the user's current task and publishing scope. For an authorized game publication, include all required models, textures, manifests, runtime modules and source records. Confirm deployment success and compare live content with the intended commit before describing it as live.
6. Update this checkpoint and add a dated log entry at the next meaningful milestone or handoff. Record partial work and failures when the task is incomplete. Do not present an old test or browser review as a new check.

## Export baseline

- Exported September 6, 2026 from the latest published ten-block version, version 4.
- Original source commit: `67c99489185417c9de9e6a7292de5329df00c82a`.
- At export, runtime and model files matched that baseline. Export-only additions were the local server, package scripts, setup instructions, and this handoff. The original hosting identity and Git metadata were omitted.
- The game can run entirely from the included static assets. No backend, Google API key, or live map service is required.

## Open-source repository preparation — September 6, 2026

- The owner authorized a public repository at `https://github.com/rayidali/borough-drive` after local GitHub authentication confirmed `rayidali`.
- Original code, documentation, and independently authored artistic contributions use MIT. Third-party and geographic data terms remain in `THIRD-PARTY-NOTICES.md` and the original asset credits.
- The repository adds a visual README using the existing Blender renders, contributor documentation, issue/PR templates, and GitHub Actions verification on Node.js 22 and 24.
- Personal setup instructions were replaced with public contributor instructions. Runtime code, geometry, textures, and reference photographs were preserved.
- The initial publishing request covered the source repository. Later requests authorized the Vercel deployment and complete revision 04 publication recorded in the current checkpoint. The geographic scope remains the existing map.

## User's objective and feedback

The public game is connected to this repository's `main` branch. The repository-root `vercel.json` serves `dist/` directly and skips installation and building. Revision 04's models, runtime changes, source recipes, evidence and README screenshots were published together in `835ea6c`.

Rayid wants to build a driving game in a recognizable digital twin of New York City, eventually Manhattan and then NYC. The immediate approved scope is ten connected East Village blocks around First Avenue and East 10th Street: East 7th to East 12th, Second Avenue to Avenue A.

The user knows this neighborhood and rejected generic buildings with real business names. Google photorealistic tiles were closer but still did not meet the desired street-level quality. The accepted approach is authored 3D geometry based on actual map footprints and photographic observations. First & 10th is the most individually detailed core and should remain the quality anchor.

Desired atmosphere: cozy, aesthetic, warm, calm exploration, with the relaxed feeling of slowroads.io but substantially stronger geographic and architectural fidelity. Prioritize recognizable facades, building proportions, rooflines, fire escapes, storefront openings, cornices, windows, signage, sidewalk details, materials, and good driving feel. Preserve real geometry while improving lighting and presentation.

Do not mistake a verified business name for a verified facade. Storefront availability and architectural reference dates must remain separately documented. Unknown occupants should stay unnamed; historical signs must remain marked as historical.

## What currently exists

- Ten complete blocks plus four boundary sections, covering three avenues and six cross streets.
- 615 building objects including five restored municipal footprints, annexes and boundary context; this is not 615 independently verified facades.
- 410 additional building records with photographic observations, from 459 combined source records. Coverage varies from storefront observations to fuller facades.
- 620 municipal footprint matches, PLUTO 26v2 parcel attributes and 210 independently supported named place records, including 200 outside the core; September 8 removed two duplicate identities. The audit retains excluded and unresolved entries.
- Blender-generated Draco GLBs with shared textures, streamed by distance.
- A highly detailed preserved First & 10th core, map travel, walk/drive modes, collision, fixed-step vehicle simulation, street props, warm lighting, and source/accuracy information.
- Business baseline checks dated September 6, 2026, two identity corrections/exterior review dated September 8, and OSM snapshot dated September 5. Image dates vary. Twenty-two shops have explicit exterior designs; remaining named shop designs are estimated.

This remains a reconstruction prototype with uneven detail. There are 142 non-core objects with mapped frontages but no individual photographic observation. Secondary elevations, some road widths, furniture positions, trees, interiors and unseen geometry remain estimated. Many archive photographs have 2012 upload dates and unknown capture dates. Do not describe it as a surveyed, fully current digital twin. Browser checks from the current local work are recorded below separately from the original export validation.

## Where to work

| Path | Purpose |
| --- | --- |
| `dist/index.html` | Active ten-block game page |
| `dist/reconstruction/viewer.js` and `viewer.css` | Main rendering, interaction, and interface |
| `dist/reconstruction/vehicle.js` | Fixed-step vehicle dynamics |
| `dist/reconstruction/neighborhood-world.js` | Collision, street geometry, navigation |
| `dist/reconstruction/neighborhood-render.js` | Section streaming and instanced props |
| `dist/reconstruction/neighborhood-map.js` | Minimap and travel map |
| `dist/reconstruction/neighborhood.json` | Geometry, facade data, visual sections, prop placements |
| `model-source/neighborhood-observations.json` | Editable photographic observation schedule |
| `model-source/neighborhood-facade-audit.json` | Revision 04's 376 individually inspected facade observations |
| `model-source/geography-corrections.json` | Municipal matches, five restored footprints and address corrections |
| `model-source/business-corrections.json` | Reviewed tenant overrides and contrary evidence |
| `model-source/neighborhood-business-audit.json` | Generated supported/unresolved business inventory |
| `model-source/street-facilities.json` | Dated street facility evidence and explicit dimension estimates |
| `model-source/neighborhood-references/` | Detailed architectural and occupancy research records |
| `model-source/build_intersection.py` | Blender recipe for the detailed core |
| `model-source/build_neighborhood.py` | Blender recipe for neighborhood sections |
| `model-source/storefront-details.json` | Explicit shop designs, per-street elevations and dated photographic provenance |
| `model-source/storefront_detail_kit.py` | Blender components for signs, openings, awnings and observed furniture |
| `model-source/digital-twin-coverage.json` | Map-wide inventory of remaining frontage evidence/design gaps |
| `model-source/storefront-review-2026-09-08.json` | Local browser poses, graphics settings, asset hashes and validation |
| `model-source/neighborhood_landmarks.py` | Landmark massing and facade forms |
| `scripts/prepare-neighborhood.py` | Derive mapped geometry from included OSM snapshot |
| `scripts/compile-neighborhood-details.py` | Apply observations and deterministic details |
| `dist/vendor/` | Included Three.js r180 and Draco runtime, with notices |
| `dist/prototype.html` | Earlier generic prototype, preserved for history; not the active game |

## Running and validation

Use Node.js 22 or newer. `npm run dev` serves only `dist/` at http://127.0.0.1:5173. It uses built-in Node modules and needs no dependency installation. `npm run verify` runs the original meaningful vehicle, road, map-spawn, GLB, texture, and module checks.

The exported copy was checked with Node.js 24.19.0: both verification scripts passed, including 2,308 road samples, valid map spawns, boundary driving, braking/reverse/collision, and frame-rate independence. A local HTTP smoke check passed for the page, JavaScript, Draco WebAssembly, core and section GLBs, and map JSON. This was a source/asset/server check, not a browser gameplay or visual performance test.

Use Blender 4.3 or newer only when mesh regeneration is needed. Read `model-source/NEIGHBORHOOD-NOTES.md` for the rebuild order. The preparation script resets derived facade and prop data, so the detail compiler must follow it. Rebuild only the affected neighborhood section where possible, for example:

```sh
blender -b -t 6 --python-exit-code 1 --python model-source/build_neighborhood.py -- --tile block-3-2
```

For optional standalone renders, specify a portable output location:

```sh
blender -b -t 6 --python model-source/render_neighborhood.py -- --output renders/neighborhood
```

Existing model exports are included; do not make Blender installation a prerequisite to opening or editing the viewer. Do not regenerate every model just to inspect the project.

## Suggested next work

Use the revision 05 coverage inventory to continue along First Avenue from East 7th toward St Marks, then throughout the existing map. Audit unobserved frontages, unseen elevations and unresolved shop units against dated sources. The user's request is map-wide fidelity; Blue & Gold was an example of a systemic problem, not the sole target. Assess actual driving feel and browser frame rate on the user's device. Preserve the accepted core and keep visual inference distinct from observation. Follow the user's current publishing instructions; the geographic scope remains the existing map.

## Previous local work — neighborhood detail revision 03

Rayid requested that the entire existing map reach and exceed the core's detail level. All fourteen existing sections were rebuilt using the shared recessed-facade system in `model-source/neighborhood_detail_kit.py`, with source-specific controls in `neighborhood-detail-schedule.json`. The pass covers 587 non-core building objects, 547 with mapped street frontages, and adds 235 instanced street objects. It also fixes stretched road/pavement UVs and enables multisample antialiasing for the postprocessing targets.

That pass preserved the core GLB/recipe, six photographic source files, mapped footprints, roads, navigation bounds, vehicle dynamics and collision module. Its photographic coverage remained 77 additional observed building records. The user rejected the insufficient geographic and storefront fidelity; this led to revision 04. See `model-source/DETAIL-PASS-03.md` for the historical pass report.

## Current neighborhood — accuracy revision 04

Read `model-source/ACCURACY-PASS-04.md` before continuing. Every municipal footprint in the existing extent has an explicit match. Five missing substantial buildings are restored: 73–75 East 7th, 256–258 East 10th, 323–325 East 12th, 195–197 Avenue A and East Side Community School at 420 East 12th. Only the new footprints are aligned to the accepted OSM frame. Existing core geometry remains unchanged.

The facade audit brings photographic coverage to 410 non-core building objects. Individual controls now include bay positions, story/basement separation, actual curved openings, recorded cornices and fire escapes, ground use and special entries. Blue & Gold has a dedicated low frontage profile; 45 East 7th uses the completed replacement building rather than the archive's vacant-site condition. The school's H-shaped outline, grouped glazing, recessed entry and internal courtyard are modeled separately from PS 19.

The compiler now processes all 369 mapped retail/food/bar/bank candidates, website address evidence, city inspection records and reviewed corrections. Of 379 total audit entries, 212 support a name and 167 are excluded or unresolved. Businesses attach to individual street frontages and estimated shop units. The data inventory is not a count of independently photographed storefront designs. Ferns, superseded Pasta de Pasta at 192 First, Blank Street and historical Beron each retain contrary/status evidence. Search in the travel map takes a name or address to its corresponding street.

Cross-street bicycle facilities, Avenue A lanes and Second Avenue's cycle/bus treatment are recorded separately from illustrative street dressing. Existing road widths and vehicle simulation are preserved; protected-side illustrative parking on East 12th is omitted to retain a clear driveable lane within those approximate widths. Building collision and distant silhouettes now preserve courtyard holes. Material variants prevent differing same-name core/neighborhood colors from being incorrectly shared.

All fourteen neighborhood GLBs were rebuilt, followed by affected-section corrections from browser review. The ordinary compiler and source preparation need no external packages or network calls. A final clean preparation/compilation in an isolated directory reproduced the working facade, geometry, business and prop data. The local server uses `npm run dev` at http://127.0.0.1:5173. Production deploys from `main` using the included static assets.

Final validation: `npm run verify` passes on Node.js 24.19.0, including 2,308 road samples, vehicle/navigation invariants, model/texture references, municipal joins, courtyard collision and bounded business partitions. Section exports total 48.67 MiB and 8,761,042 triangles, with at most 46 material batches per section. All 610 original footprints, road centers/widths/directions and driving bounds are unchanged. Core model/recipe and six licensed reference files are byte-identical to HEAD.

Actual browser views were inspected across all fourteen sections, then rechecked after correcting the school entrance and over-wide corner shops on 21 buildings. Model/texture requests succeeded and no uncaught exceptions occurred; existing RGBELoader deprecation warnings remain. Name/address searches and invalid-input handling passed in the real interface. Two sequential 180-frame stationary samples on Apple M1 / ANGLE Metal at 1440 × 1000 recorded 30.9 fps near Blue & Gold and 60.0 fps near the school. Default adaptive quality was enabled; this is not a sustained or fixed-quality driving benchmark. See `model-source/accuracy-review-2026-09-06.json` for conditions and `docs/images/` for actual browser captures.
