# Borough Drive: continuation context

## Current checkpoint — 2026-09-08-08 (First & 7th comparison pass saved locally)

Recorded **2026-09-08T22:20:14-04:00**. The user resumed implementation specifically at **First Avenue / East 7th Street**, using the **most recent accessible view**, to establish a detailed standard before extending block by block. This first intersection study is implemented and reviewable locally. **User acceptance is pending; do not extend to the rest of the map automatically.** Google Street View was inaccessible, so the sources and viewer explicitly identify the alternative dated photographs and remaining uncertainty.

| Item | Checkpoint state |
| --- | --- |
| Exact local gameplay/source commit | `0f40856c9c576d1648ddae9c6e76bb550a98b42a` — Model the First and Seventh four-corner detail study |
| Checkpoint documentation | Follows the source commit separately. Identify its own commit using `git log -- CODEX-HANDOFF.md SESSION-LOG.md`; do not amend just to embed its own hash. |
| Checkout at resume | Initially clean `main...origin/main`, HEAD `a44257a0a45c627176ed618f179cba53e5820940`. All new source, models, observations and 22 game captures saved in the local source commit. No unfinished export. |
| Implemented scope | NW 115 First / Tile Bar; NE 118–120 First / 91 East 7th with E7 Deli, Hen House, Monkey Sushi and 7th Street Burger; SW 113 First / 86 East 7th with E Smoke and Yubu; SE 116 and adjoining 114 First / Saifee. Five profiles, nine elevations, eight shop treatments. |
| Geometry/details | Individually scheduled bays, lintels, cornices, grilles and escapes; revised Saifee/113 proportions; Tile Bar tilework, door and joined striped canopy; shop lettering, boards, lights, entries, bay windows, stock, plant racks, table and street hardware. Dimensions and obscured details remain estimates. |
| Presentation | Four First & 7th view buttons. Detailed / Automatic / Faster graphics, physical storefront glass and corner reflection capture, display lighting. Faster uses simpler glass. Start/reset remains `(0,228)`, northbound, both modes. |
| Preservation | First & 10th GLB/recipe, vehicle code and six licensed photos byte-identical to published baseline. All 615 mapped footprints/heights and all roads/bounds unchanged. Render-height estimates separately set 116 First to 13.15 m and 113 First to 16.7 m. |
| Push / deployment | **Not pushed or deployed.** Remote not fetched in this task; cached `origin/main` remains `a44257a`. Existing production https://borough-drive.vercel.app remains previously published gameplay `63757cbbb13749584e761e4bf7a8e655f90b1bd4`, through documentation `a44257a`; no new live check. |
| Checks completed | Final `npm run verify` on Node.js 24.15.0; 2,308 road samples, source/model signatures, corner schedules, model/assets, navigation and collisions. Disposable clean prepare/compile reproduced all source fields and three generated audits. Staged whitespace checks and 191 relative Markdown links passed. |
| Browser review | 22 final game viewpoints saved; start/northbound driving/both resets/four corner buttons/graphics persistence passed. Zero uncaught exceptions, console errors or failed HTTP responses. Existing RGBELoader deprecation warning remains. |
| Size / performance | Fourteen neighborhood GLBs: 51.78 MiB, 9,389,484 triangles, maximum 62 material batches. Two sequential 120-frame stationary M1/ANGLE Metal samples at 1440×1000: 25.0 fps Detailed and 56.3 fps Faster. Short single-device samples, not a sustained driving benchmark. |
| Remaining uncertainty | Exact fonts/logos, tiny labels, complete murals, unobserved room layouts and return surfaces, calibrated paint/material samples and surveyed dimensions. Latest accessible photographs vary from dated 2021–2025 business views to undated/archive architecture. No certified 1:1 / latest Google panorama match or user-approved standard. |
| Next concrete step | Open the local game and compare all four First & 7th buttons with the user's Street View views. Address the user's specific discrepancies within this intersection before extending block by block. Read a new publishing instruction before pushing. |

Start with [FIRST-SEVENTH-PASS-06.md](model-source/FIRST-SEVENTH-PASS-06.md), [source observations](model-source/first-and-seventh.json), [the full browser review](model-source/first-seventh-review-2026-09-08.json) and the tracked images in `docs/images/`. The executable recipe is `model-source/first_seventh_kit.py`; compilation is `scripts/neighborhood_corner.py` plus the storefront compiler. The broader inventory now has 411 photo-observed non-core building records, 214 supported names (204 non-core), 27 individual non-core shop designs and 177 supported non-core names with estimated designs. These coverage counts do not certify complete facades.

Rebuild only `block-5-1`, `block-5-2` and `edge-south` after corner-kit changes. This initial integration also regenerated six preexisting detailed sections solely for the shared-recipe signature; their binary geometry/textures and all other metadata are unchanged. Do not compile while Blender is exporting, because it writes the manifest at completion. Blender authors assets and Three.js runs the browser game; no engine migration was requested or performed.

### Photographic sources and durable records

| Purpose | Actual sources and where to resume |
| --- | --- |
| First & 10th architecture/photos | Wikimedia Commons/Flickr: Eden, Janine and Jim; Kidfly182. JLL full-building photographs are observation only. Exact dates, URLs, licenses and bundled files: [references.json](dist/reconstruction/references.json) and [core facade notes](model-source/FACADE-NOTES.md). |
| Individually modeled core shops | Official business sites including Nishaan and Gelatoville; dated EV Grieve and theater reporting. [Core storefront notes](model-source/CURRENT-STOREFRONTS.md) record those observations. |
| Wider neighborhood/storefronts | Village Preservation's Building Blocks archive, NYC landmark records, official business photographs (including Tile Bar), EV Grieve, Forgotten New York/Kevin Walsh, and separately credited architecture sources. [Storefront schedule](model-source/storefront-details.json), [facade audit](model-source/neighborhood-facade-audit.json), and [research records](model-source/neighborhood-references/) retain evidence and uncertainty. |
| Geography and materials | Included OSM snapshot and NYC OTI/PLUTO records anchor mapped geometry. Poly Haven surface maps are generic, not scans of these actual buildings. [Credits](dist/reconstruction/ASSET-CREDITS.md) and [third-party notices](THIRD-PARTY-NOTICES.md) preserve terms. |

Most new reference photographs were inspected to guide authored geometry; they are not copied onto every facade. Six licensed core photographs are bundled; selected core photo patches retain their original attribution. Other research images and historical temporary filenames may not exist locally: resume from the tracked source URLs, not old download folders. No image-generation guesses stand in for real reference photographs.

### Resume a session

1. Read this checkpoint, the latest [session log entry](SESSION-LOG.md), [START-HERE.md](START-HERE.md), and [neighborhood notes](model-source/NEIGHBORHOOD-NOTES.md). For historical context, read [pass 05](model-source/STOREFRONT-PASS-05.md), the [coverage inventory](model-source/digital-twin-coverage.json) and the historical [accuracy audit](model-source/ACCURACY-PASS-04.md).
2. Inspect the actual checkout without discarding changes:

   ```sh
   git status --short --branch
   git log -5 --oneline
   git log -1 --format="%h %cI %s" -- CODEX-HANDOFF.md SESSION-LOG.md
   ```

3. If remote state matters, fetch `origin` and compare it with the checkout before changing branches or pulling. Local `origin/main` can be stale. Record any uncommitted files or unpublished commits before continuing.
4. Use `npm run dev` to open the game locally when needed. A previous session's server, browser, authentication, or `/tmp` files may no longer exist. All required game assets and reproducible source are in the repository; no Blender rebuild is needed to resume.
5. Follow the active First & 7th benchmark scope and the user's publishing instructions. Extend beyond this intersection only after review. For an authorized game publication, include all required models, textures, manifests, runtime modules and source records. Confirm deployment success and compare live content with the intended commit before describing it as live.
6. Update this checkpoint and add a dated log entry at the next meaningful milestone or handoff. Record partial work and failures when the task is incomplete. Do not present an old test or browser review as a new check.

## Historical export baseline

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

The public game is connected to this repository's `main` branch. The repository-root `vercel.json` serves `dist/` directly and skips installation and building. Revision 04 was published in `835ea6c`; the online runtime/model pass is `63757cb`, with later documentation commits. The local First & 7th source commit and its unpushed state are recorded above.

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

This remains a reconstruction prototype with uneven detail. There are 142 non-core objects with mapped frontages but no individual photographic observation. Secondary elevations, some road widths, furniture positions, trees, interiors and unseen geometry remain estimated. Many archive photographs have 2012 upload dates and unknown capture dates. Do not describe it as a surveyed, fully current digital twin. Pass 05 browser checks are linked above; older validation below remains historical.

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

The original September 6 exported copy was checked with Node.js 24.19.0: both verification scripts passed, including 2,308 road samples, valid map spawns, boundary driving, braking/reverse/collision, and frame-rate independence. A local HTTP smoke check passed for the page, JavaScript, Draco WebAssembly, core and section GLBs, and map JSON. This was a source/asset/server check, not a browser gameplay or visual performance test.

Use Blender 4.3 or newer only when mesh regeneration is needed. Read `model-source/NEIGHBORHOOD-NOTES.md` for the rebuild order. The preparation script resets derived facade and prop data, so the detail compiler must follow it. Rebuild only the affected neighborhood section where possible, for example:

```sh
blender -b -t 6 --python-exit-code 1 --python model-source/build_neighborhood.py -- --tile block-3-2
```

For optional standalone renders, specify a portable output location:

```sh
blender -b -t 6 --python model-source/render_neighborhood.py -- --output renders/neighborhood
```

Existing model exports are included; do not make Blender installation a prerequisite to opening or editing the viewer. Do not regenerate every model just to inspect the project.

## Later map-wide work — after the First & 7th benchmark review

The user has resumed work on First & 7th only. After that benchmark is accepted, use the revision 05 coverage inventory to work through First Avenue from East 7th toward St Marks and throughout the existing requested bounds. Audit unobserved frontages, unseen elevations and unresolved shop units against dated sources. The user's request is map-wide fidelity; Blue & Gold was an example of a systemic problem, not the sole target. Assess actual driving feel and browser frame rate on the user's device. Preserve the accepted core and keep visual inference distinct from observation. Follow the user's current publishing instructions; the geographic scope remains the existing map.

## Previous local work — neighborhood detail revision 03

Rayid requested that the entire existing map reach and exceed the core's detail level. All fourteen existing sections were rebuilt using the shared recessed-facade system in `model-source/neighborhood_detail_kit.py`, with source-specific controls in `neighborhood-detail-schedule.json`. The pass covers 587 non-core building objects, 547 with mapped street frontages, and adds 235 instanced street objects. It also fixes stretched road/pavement UVs and enables multisample antialiasing for the postprocessing targets.

That pass preserved the core GLB/recipe, six photographic source files, mapped footprints, roads, navigation bounds, vehicle dynamics and collision module. Its photographic coverage remained 77 additional observed building records. The user rejected the insufficient geographic and storefront fidelity; this led to revision 04. See `model-source/DETAIL-PASS-03.md` for the historical pass report.

## Historical foundation — accuracy revision 04

The following summarizes revision 04 at `835ea6c`; its counts and validation predate pass 05. Read `model-source/ACCURACY-PASS-04.md` for that historical audit. Every municipal footprint in the existing extent has an explicit match. Five missing substantial buildings are restored: 73–75 East 7th, 256–258 East 10th, 323–325 East 12th, 195–197 Avenue A and East Side Community School at 420 East 12th. Only the new footprints are aligned to the accepted OSM frame. Existing core geometry remains unchanged.

The facade audit brings photographic coverage to 410 non-core building objects. Individual controls now include bay positions, story/basement separation, actual curved openings, recorded cornices and fire escapes, ground use and special entries. Blue & Gold has a dedicated low frontage profile; 45 East 7th uses the completed replacement building rather than the archive's vacant-site condition. The school's H-shaped outline, grouped glazing, recessed entry and internal courtyard are modeled separately from PS 19.

The compiler now processes all 369 mapped retail/food/bar/bank candidates, website address evidence, city inspection records and reviewed corrections. Of 379 total audit entries, 212 support a name and 167 are excluded or unresolved. Businesses attach to individual street frontages and estimated shop units. The data inventory is not a count of independently photographed storefront designs. Ferns, superseded Pasta de Pasta at 192 First, Blank Street and historical Beron each retain contrary/status evidence. Search in the travel map takes a name or address to its corresponding street.

Cross-street bicycle facilities, Avenue A lanes and Second Avenue's cycle/bus treatment are recorded separately from illustrative street dressing. Existing road widths and vehicle simulation are preserved; protected-side illustrative parking on East 12th is omitted to retain a clear driveable lane within those approximate widths. Building collision and distant silhouettes now preserve courtyard holes. Material variants prevent differing same-name core/neighborhood colors from being incorrectly shared.

All fourteen neighborhood GLBs were rebuilt, followed by affected-section corrections from browser review. The ordinary compiler and source preparation need no external packages or network calls. A final clean preparation/compilation in an isolated directory reproduced the working facade, geometry, business and prop data. The local server uses `npm run dev` at http://127.0.0.1:5173. Production deploys from `main` using the included static assets.

Final validation: `npm run verify` passes on Node.js 24.19.0, including 2,308 road samples, vehicle/navigation invariants, model/texture references, municipal joins, courtyard collision and bounded business partitions. Section exports total 48.67 MiB and 8,761,042 triangles, with at most 46 material batches per section. All 610 original footprints, road centers/widths/directions and driving bounds are unchanged. Core model/recipe and six licensed reference files were byte-identical to the revision 04 comparison baseline.

Actual browser views were inspected across all fourteen sections, then rechecked after correcting the school entrance and over-wide corner shops on 21 buildings. Model/texture requests succeeded and no uncaught exceptions occurred; existing RGBELoader deprecation warnings remain. Name/address searches and invalid-input handling passed in the real interface. Two sequential 180-frame stationary samples on Apple M1 / ANGLE Metal at 1440 × 1000 recorded 30.9 fps near Blue & Gold and 60.0 fps near the school. Default adaptive quality was enabled; this is not a sustained or fixed-quality driving benchmark. See `model-source/accuracy-review-2026-09-06.json` for conditions and `docs/images/` for actual browser captures.
