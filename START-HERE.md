# Run DriveAround.nyc locally

<!-- current-project-status -->
> **Current October 25:** The 397-building expansion, redesigned minimap and spatial loading are pushed to main in `0073ecd` and [verified live](model-source/publication-2026-10-25/README.md). Continue the assigned Eleventh First–Avenue A and Twelfth Second–First blocks, both sides, without routine stage permission. The [current handoff](CODEX-HANDOFF.md) records active source/model work, exact preservation and performance limits. Earlier dated checkpoints below remain historical.
<!-- /current-project-status -->

**October 25 completed assignment:** All three blocks—Tenth Second–First, Tenth First–Avenue A, and Eleventh Second–First, both sides—are complete locally: 91 reviewed planes, 397 buildings / 398 scenes. Main/live remain the verified 295-model `e1155e5`; new three-block work is local/uncommitted. Ten browser routes, ten boundaries, four cameras/reset, 17 addresses, preservation and recorded startup/weather checks pass. Dated evidence, fine-art and height/depth limits remain explicit. No fourth block is queued. Preserve cache/tools/original/private files and read the [current handoff](CODEX-HANDOFF.md) for exact build, evidence and next review step.

**October 25 active:** Both Tenth blocks are complete locally; final east candidate06 has375 buildings/376 scenes. Main/live remain295-model `e1155e5`. Continue the assigned third block, Eleventh Second–First, both sides (`01-E11-21`), without stage permission.26planes/22owners are inventoried, research next. Preserve all352 ordinary models,24 frozen core scenes, cache/tools/original/private files. [Current handoff](CODEX-HANDOFF.md) records exact validation, source limits and publication state.

**October 25 current:** Tenth Second–First is complete locally; preview north on First, left on Tenth. Two further blocks are assigned and in progress. Main/live remain the295-model release; read the current handoff for exact states and review/performance limits.

**October 24 current state:** the 295-model expansion and review evidence are pushed to `main`; final CI, deployment and live-file/cache verification pass. Follow the [current handoff](CODEX-HANDOFF.md) for exact CI/live state and the assigned Tenth block. Existing tools, login and cached models remain ready; the restart commands below still apply. Earlier October 23 publication statements describe that dated checkpoint.

## After restarting VS Code or Terminal

**Current resume:** Continue the authorized minimap/scaling, publication and two-block assignment from the newest handoff. Preserve the dirty worktree and caches; run `npm run dev -- 5181` only if the preview is absent. No repeated installation, login or stage approval is needed.

**October 23 close:** the project was transferred to this new laptop, its tools and Street View access were restored/tested, and the user is restarting VS Code before returning. Saved work and installed tools persist; terminal-launched preview/browser processes may need restarting. The **295-model expansion is local/uncommitted**; GitHub/live still have the earlier **203-model revision 09**, as checked during restoration. Read [CODEX-HANDOFF.md](CODEX-HANDOFF.md) first. No reinstall, new GitHub login, new model build or publication is needed just to resume.

Open this folder in VS Code, then run in its terminal:

```sh
cd /Users/rayidali/Desktop/borough-drive
git status --short --branch
npm run dev -- 5181
```

Open **http://127.0.0.1:5181/**. Drive north on First, then right on Ninth. If port 5181 is already occupied by the existing preview, use that running server. `/index.html` remains the original ten-block game. `npm install` is unnecessary.

Fresh terminals currently use **Homebrew Node 22.23.4/npm 10.9.9**; all three offline verification suites pass with it. The project-local **Node 24.22.1/npm 11.19.1** is also available and tested. To explicitly select that alternative for one terminal:

```sh
export PATH="$PWD/.tools/node-v24.22.1-darwin-arm64/bin:$PATH"
```

`gh` is already authenticated as `rayidali`, with credentials in macOS Keychain; `gh auth status` confirms it without starting another login. For Python map inventory work in a new terminal, use `source .tools/python/bin/activate` (Python 3.13.17 and the installed libraries). Activation is per terminal; `deactivate` returns to the shell's default Python.

For browser research/review, use the isolated Brave launch command in the setup section below if that profile is not already running. It exposes localhost CDP on port 9222 and leaves the normal Brave profile separate. **Ordinary Google Maps Street View is tested and working** with Node's built-in browser-control capabilities; no extra automation library or API key is needed for that workflow. Paid API validity/billing are untested and unnecessary for browser viewing.

Suggested resume message: **“Read the latest CODEX-HANDOFF.md and SESSION-LOG.md; restore the local preview and continue from the recorded state.”** The next proposed block is Tenth, Second–First, both sides; an instruction to start it begins with exact protected-core ownership preparation. Closing/reopening the editor does not automatically assign that block or publish the local expansion.

## New laptop restored — October 23, 2026

The transferred **295-model October 15 build is intact and playable**. GitHub `main` is still `a2a90a3`; the public site's manifest still identifies the earlier **203-model revision 09**. The expansion is local and uncommitted. No publication occurred during setup. [Current handoff](CODEX-HANDOFF.md) · [Setup verification](model-source/machine-setup-2026-10-23/verification.json).

From this folder, run `npm run dev -- 5181` and open **http://127.0.0.1:5181/** in Brave. Drive north on First, then right on Ninth for the latest block. `/index.html` opens the preserved original game. No `npm install`, API key, or backend is needed.

The initial restoration installed project-local Node **24.22.1** / npm **11.19.1**, Blender **5.2.1**, and Python tooling, and verified the transferred Godot **4.7.2** with matching web templates. Later concurrent setup made Homebrew Node **22.23.4** / npm **10.9.9** and GitHub CLI **2.103.1** the fresh-terminal defaults; both Node versions are supported and tested. Commands `blender`, `godot`, and `uv`, plus the alternative Node/npm links, are available under `~/.local/bin`. Blender is in `/Applications/Blender.app`; project-installed tools live under ignored `.tools/`. Moving this repository again requires updating those user command links. Homebrew is now installed, but neither it nor Vercel CLI is a project requirement for serving the bundled game.

Map inventory tools use the isolated **Python 3.13.17** environment: `source .tools/python/bin/activate`, then use `python3` as usual; `deactivate` returns to the system interpreter. It includes Shapely **2.2.0**, Matplotlib **3.11.2**, NumPy **2.5.4**, and their dependencies. macOS's Python was left unchanged. `npm run verify`, `npm run seventh:verify`, and `npm run workflow:verify` are the existing offline checks. [Engine rebuild instructions](engine/first-seventh/README.md).

The isolated Brave review profile is `.tools/brave-review`, with browser control on localhost port **9222**. To restart it for existing review scripts:

```sh
"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \
  --remote-debugging-address=127.0.0.1 --remote-debugging-port=9222 \
  --user-data-dir="$PWD/.tools/brave-review" --no-first-run \
  --no-default-browser-check --disable-background-timer-throttling \
  --disable-renderer-backgrounding about:blank
```

**Preserve `engine/first-seventh/.godot/` on this machine.** All 295 transferred imported scenes match the reviewed runtime. A clean import produced different compiled hashes; an isolated import using the transferred cache retained all 295. The cache is theoretically regenerable, but deleting it does not preserve reviewed scene bytes. Keep `dist/seventh/areas/` with the player. The local recovery archive and baseline are under `.tools/recovery/2026-10-23/`; this is a local copy, not an off-device backup.

The setup checks passed eight driving routes, eight boundaries, four cameras, 17 browser address cases, four HTTP routes and all 314 runtime hashes. Blender's test GLB export, Python geometry/plotting, and Godot's isolated import/web export also ran successfully. The isolated export using the transferred cache reproduces the complete area manifest and PCK **byte for byte**. The import cache has its own local recovery tar alongside the worktree archive. Installed Python library versions are saved in [requirements.txt](model-source/machine-setup-2026-10-23/requirements.txt). This is setup verification, not a new photographic fidelity review or a full performance benchmark. The proposed next block remains **Tenth, Second–First, both sides**, with exact protected-core ownership preparation before modeling.

**October 15 checkpoint — current:** [East Ninth, First–Avenue A, both sides](model-source/EAST-VILLAGE-E09-EAST.md) has **50 individually reviewed facade planes / 41 affected buildings**, 42 shopfront/return records and 41 access entries; **295 models** total. Preserve all 254 unrelated prior model pairs, 148’s protected First face/mass and both private screenshots. Dated-source limits include seven unresolved tenant identities and historical Good Beer. Driving/boundary/camera/address checks pass; the report/current handoff record final loading and performance evidence, including slower westbound chase rendering and an unexplained frame stall. Continue roughly one complete block per session without reducing individual detail. **Proposed next: `01-E10-21`, Tenth Second–First, both sides**, only on the next user instruction after exact protected-core ownership preparation. Preserve all uncommitted work; no publication. Preview **http://127.0.0.1:5181/** — north on First, **right on Ninth**. Earlier next-step notes are historical.

**Preceding October 14 full-block checkpoint:** [East Ninth, Second–First, both sides](model-source/EAST-VILLAGE-E09-BLOCK.md) now has all 34 remaining faces implemented and individually reviewed, with 34 storefronts and 33 residential/access entries. All 221 preceding models and both private screenshots remain unchanged; total **255 models**. Integrated driving/control/address/startup checks are recorded in the report/current handoff, including slower loading and five storefront evidence gaps. N02A/N02B/N03/S01/S02/S03 were internal groups, delivered together. Continue using roughly one complete block per session while preserving individual detail and dated evidence. **Proposed next: `01-E09-1A`, Ninth from First to Avenue A, both sides**, on the next user instruction. Preserve all uncommitted work; no publication. Preview http://127.0.0.1:5181/ — north on First, left on Ninth. Earlier next-packet notes below are historical.

**October 14 cadence correction — historical planning checkpoint:** the user expects roughly one full street block per session. Next delivery is **East Ninth, Second–First, both sides (`01-E09-21`)**, completing 34 remaining faces while preserving eight completed faces and the separate P03 return. N02A is the first internal group; continue through the block without a routine handoff after each small group. Keep the storefront/building detail standard and consolidate repeated global checks at block integration. This turn updates planning/instructions only; no new modeling or publication. [Exact workflow and scope](model-source/east-village-block-workflow.json). Earlier small-packet next-step notes below are historical.

**Preceding N01B complete locally — October 14, 2026:** [339–333 East Ninth](model-source/EAST-VILLAGE-E09-N01B.md) adds four distinct facades, six shopfronts and four residential entries, including 339’s open well and 337’s recessed passage. All 217 earlier authored/compiled models remain byte-identical; total **221**. Final source-to-game detail review, six driving legs, seven boundaries, four camera modes/reset, 17 address cases and five cold/five warm startups are recorded with limits. **Next: 01-E09-21-N02A, 331–325 East Ninth**, on the next user instruction. Preserve all preceding uncommitted work. No publication. Preview: http://127.0.0.1:5181/ — north on First, then left on Ninth. Read the current handoff for exact package, timings and dated-source limitations.

**Preceding N01A complete locally — October 13, 2026:** [147 First’s Ninth return and 345–341 East Ninth](model-source/EAST-VILLAGE-E09-N01A.md) add four individual facades, five shopfronts/four businesses and residential access, including a real open basement well. All 213 earlier authored/compiled models remain byte-identical; current total is **217**. Fifty-nine detail images and 18 gameplay images were inspected; six driving legs, seven boundaries, four camera modes/reset, 17 address cases and ten startups pass within recorded limits. **Next: 01-E09-21-N01B, 339–333 East Ninth**, on the next user instruction. Preserve preceding uncommitted work; no publication. Preview: `http://127.0.0.1:5181/` (restart `npm run dev -- 5181`), north on First then left onto Ninth. Read the current handoff for exact package/performance/source limits.

**Preceding P03 complete locally — October 13, 2026:** [145 First Avenue / southwest Ninth corner](model-source/EAST-VILLAGE-P03.md) adds both street faces, Baji Baji and East Village Pizza, with 26 upper openings, individual signs/shades/displays/murals and the separate 352 Ninth entrance. All 212 prior models remain byte-identical; current total is 213. Thirty-five detail views, 18 gameplay views, six driving legs, seven boundaries, four camera modes and 17 address cases were inspected or tested as recorded. Startup medians were slower in this run; read the report for exact evidence and limits. **Next: 01-E09-21-N01A**, four north-side Ninth faces, on the next user instruction. All work remains local/uncommitted; no publication. Preview: `http://127.0.0.1:5181/` (restart with `npm run dev -- 5181`).

**Preceding P02 complete locally — October 13, 2026:** [138–148 First Avenue](model-source/EAST-VILLAGE-P02.md) adds five individually observed facades and five shops, with explicit party-wall/setback review, distinct rooflines/fire escapes and brick/stucco finishes. All 207 preceding models are unchanged; the slice now has 212 models. Fifty detail views, 13 gameplay views, four driving/boundary/camera cases and 17 address cases are reviewed or checked as recorded. Ten startups completed; one 21.7-second warm outlier remains unexplained. **Next: P03, 145 First Avenue / Ninth corner, on the next user instruction.** Changes remain local/uncommitted; production remains revision 09.

**Preceding P01 checkpoint — October 12, 2026:** [137–143 First Avenue](model-source/EAST-VILLAGE-P01.md) adds four individually observed facades / seven businesses, preserving all 203 prior authored and compiled scenes. The local slice now has 207 models, a 7,991,408-byte shared pack and required external scenes. Four driving legs, four boundaries, four camera modes, 17 address cases and final storefront review pass within documented limits. First Avenue alone extends to z=−145; Ninth and other avenue ends stay closed. **Next: P02, five east-side First Avenue faces, on the next user instruction.** Everything remains local/uncommitted; production stays revision 09.

**Preceding October 12 — EV-003 complete locally:** [Loading integration](model-source/EAST-VILLAGE-EV003.md) adds release verification, scene caching and safe resize/retry behavior while preserving all 203 models. Browser/route/ownership checks pass; the 7.61 MiB shared pack still requires every tracked `dist/seventh/areas/` file. **Next: P01, 137–143 First Avenue**, with its [exact adapter handoff](model-source/east-village-ev003/p01-handoff.json). All changes remain local/uncommitted; production remains revision09. Read the [current checkpoint](CODEX-HANDOFF.md).

**October 12 — preceding EV-002 complete locally:** the [browser loading proof](model-source/EAST-VILLAGE-EV002.md) now uses a 7.61 MiB shared pack and 203 unchanged external building scenes. Twelve west-context buildings unload/reload with their colliders; 191 stay resident. Loading/recovery, resource-release, controls and 54 paired review images pass the bounded proof. Keep the complete `dist/seventh/areas/` directory when serving the game. All models still load initially; this is not a startup-byte reduction or whole-area scalability result. **EV-003 integration is next**, on the next session instruction. Changes are local/uncommitted; production remains revision 09. Follow the [current handoff](CODEX-HANDOFF.md).

**October 12 — preceding EV-001 design complete locally:** the [loading/package design](model-source/EAST-VILLAGE-EV001.md) specifies a shared startup pack plus independently fetched building scenes, exact resource ownership and a measured browser proof. All 203 scenes have a read-only dependency census; three native relocation checks pass. **EV-002 is next:** unload/reload 12 existing west-context buildings during real travel while preserving the other 191. Browser speed, appearance and memory still need that proof. Revision 09 remains unchanged; the plan, inventory and design are local/uncommitted. Follow the [current handoff](CODEX-HANDOFF.md).

**October 12 — preceding EV-000 inventory checkpoint:** the confirmed whole East Village scope is Houston–Fourteenth, Bowery/Third–East River, including Alphabet City, Tompkins Square and waterfront. The [session roadmap](model-source/EAST-VILLAGE-SESSION-PLAN.md) and [first packets](model-source/EAST-VILLAGE-FIRST-SESSIONS.md) now have a [frozen municipal map/ownership inventory](model-source/EAST-VILLAGE-EV000.md): 2,207 lots, 2,365 footprints, 367 street/path/structure records and 53 exact initial faces. These are geographic counts, not completed storefronts. **EV-001 loading/package design is next.** The game remains published revision 09, unchanged. Plan/inventory files are local and uncommitted; follow the [current handoff](CODEX-HANDOFF.md).

**October 11 user-endorsed revision 09:** the actual First Avenue / St. Marks storefronts have been revised after the instruction update: 80 business/return records across 57 faces / 51 buildings now have individual lettering, material patterns, awnings, entrances, displays and furniture. All 203 buildings remain; 152 models are byte-identical to revision 08. [Current report and review limits](model-source/SEVENTH-ENGINE-09.md) · [Exact save/push/deployment state](CODEX-HANDOFF.md). The user-endorsed revision is pushed to `main` and live at [DriveAround.nyc](https://www.drivearound.nyc/); both Node CI jobs, Vercel, live routes and the complete PCK hash passed.

The confirmed extent remains First Avenue Seventh–St. Marks and both sides of St. Marks Second–Avenue A, including same-parcel returns. The [reconstruction skill](model-source/skills/reconstruct-street/SKILL.md) and [storefront standard](model-source/skills/reconstruct-street/references/storefront-individuality.md) retain the user's Tile Bar reference and demand for individual detail. Rendered review is recorded separately from user acceptance and calibrated fidelity.

Run `npm run dev` and open **http://127.0.0.1:5173/**. Drive north from First & Seventh through St. Marks to the new 137–143 west-side shops, or turn at St. Marks west toward Second Avenue or east toward Avenue A. `/seventh/` uses the same included export; `/index.html` remains the original ten-block game. No rebuild or API key is needed to play. Right-drag to orbit/look, Shift + right-drag or middle-drag to pan, wheel to zoom, V to recenter, and C to change POV. Escape → Controls opens the full guide. [Controls/rebuild](engine/first-seventh/README.md).

The accepted Seventh blocks and First & Seventh corner, original game/core, compact interface and audio are preserved. The address HUD remains bounded to Seventh. The [reconstruction skill](model-source/skills/reconstruct-street/SKILL.md) supplies the source/review workflow; the [experience brief](docs/DRIVEAROUND-EXPERIENCE-BRIEF.md) keeps separate branding/music proposals. Ordinary browser Street View supplied dated observations for this pass; no paid API job was used. Publication was subsequently requested after the user endorsed revision 09. Calibrated photographic acceptance remains open. After publication, follow the user's next bounded direction; no further street is queued.

The repository includes the active ten-block game, exported models, textures, reference data, and editable source recipes. You can play without rebuilding anything.

**Historical initial September 14 slice:** The user deferred a GPU machine and authorized implementation with available hardware. The Godot slice ran at `/seventh/` while the ten-block game then occupied `/`; September 15 routing superseded that arrangement. WASD/arrows drive, C cycles four cameras and T changes weather. [Controls and rebuild](engine/first-seventh/README.md), [initial review](model-source/SEVENTH-ENGINE-01.md). Runtime files are included; wider reconstruction and autonomous imagery work remain deferred to explicit future tasks.

## Previous resume state — September 12, 2026

The owner accepted [First & 7th revision 06](model-source/FIRST-SEVENTH-PASS-06.md) as the minimum completion standard: five individual building profiles, nine exposed elevations and eight shops. [Performance pass 07](model-source/PERFORMANCE-PASS-07.md) preserves those models while improving startup, rendering and idle GPU use. The user subsequently authorized [pass 08](model-source/FIRST-SEVENTH-PASS-08.md), a Street View-based refinement of this corner. Passes 08 and 09 were published on September 10; the exact source and verified deployment states are recorded in the handoff. An economical block/street process is now prepared for a small pilot before wider East Village work; Manhattan/NYC remain longer-term objectives.

**September 12 historical instruction: brainstorming only.** September 14 supersedes that pause for the bounded game slice above. The desired future batch process must find useful reference views itself, process each block’s facades and street details, review the results and retain progress without depending on this chat or manual image uploads. Automatic acquisition, a persistent execution ledger and the worker/build/review coordinator are not implemented.

**Historical September 12 planning note:** the direction was browser-first with Unreal deferred. [Browser pass 09](model-source/BROWSER-PASS-09.md) improved the corner's presentation and rendering; [the block workflow](model-source/BLOCK-WORKFLOW.md) prepares small offline worker packets and a finite coverage inventory. No paid AI batch or wider building pass has started. Google API access does not establish permission for bulk/derived-content processing; any future workflow requires suitable imagery rights.

Read the current [handoff](CODEX-HANDOFF.md) and latest [session log](SESSION-LOG.md), then run `git status --short --branch` and `git log -5 --oneline`. Preserve local changes and check the recorded publishing state before pulling or pushing. Existing models are included; old servers, temporary photo folders and browser sessions are not needed to recover the project.

## Start the game

Use Node.js 22 or newer. From the repository folder, run:

```sh
npm run dev
```

Open **http://127.0.0.1:5173** in a browser. Leave the terminal running; press Ctrl+C to stop the server. The preview link works only while this local server is running. To restore the session link at **http://127.0.0.1:5181/**, run `npm run dev -- 5181` instead. If the port is occupied, run `npm run dev -- 5174` and open http://127.0.0.1:5174 instead.

There is no `npm install` step. Runtime libraries and assets are bundled. Blender is optional and only needed to regenerate models. Once the repository is downloaded, the game can run locally without internet access. External source links still need a connection.

The server serves only `dist/` and listens on your computer's loopback address. It does not expose the repository or game to other devices.

## Python alternative

If Python 3 is already installed:

```sh
python3 -m http.server 5173 --bind 127.0.0.1 --directory dist
```

On Windows, use `py` in place of `python3` if needed.

This basic Python server does not apply the project’s rewrites: open **http://127.0.0.1:5173/seventh/** for Seventh and **http://127.0.0.1:5173/legacy.html** for the original game. Use `npm run dev` to reproduce the deployed `/` and `/index.html` routes.

## Host on Vercel

The existing project connects [rayidali/borough-drive](https://github.com/rayidali/borough-drive) to [borough-drive.vercel.app](https://borough-drive.vercel.app), deploying from `main`. Use that setup when continuing this project. For a separate fork, import its GitHub repository and leave **Root Directory** at the repository root (the default). The checked-in [vercel.json](vercel.json) selects the **Other** framework preset, skips installation and building, and serves **`dist/`** as the website. The game is available at `/` on the deployed domain.

Do not use `npm run dev` or `npm start` as a Vercel build command: those commands start the local development server. All production files are already included in `dist/`.

If an earlier deployment shows `404: NOT_FOUND`, deploy the latest commit containing `vercel.json` and check that the project's Root Directory is still the repository root. Redeploying an older commit will retain its old configuration.

## Controls

For the default Seventh game, use the [current driving/camera controls](engine/first-seventh/README.md). The following controls apply to the preserved **legacy game at `/index.html`**:

- On foot: W/A/S/D to move, drag to look, Q/E to turn.
- Click **Drive**: W to accelerate, S to brake and then reverse, A/D to steer, Space to brake.
- M opens the travel map.
- First & 7th detail-study buttons frame each of the four corners.
- Graphics defaults to Automatic for new visitors; saved choices are preserved. Automatic adapts pixel work during slow motion and restores a sharper stopped view. Detailed and Faster remain available.
- Start at First Avenue and East 7th Street, facing north. R returns here in either mode.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Opening `dist/legacy.html` directly fails | Use the local HTTP server; modules and models need HTTP loading. |
| The 3D view cannot start | Use a browser with WebGL2 and hardware acceleration enabled. |
| Initial loading takes a moment | Nearby section models and a 4.18 MiB street-material asset load first; First & 10th streams when approached. |
| The address is already in use | Choose another port, such as `npm run dev -- 5174`. |
| Edits do not appear | Refresh the browser. The server does not provide hot reload. |
| Model or module loading fails after an edit | Run `npm run verify` and check the browser console. |

## Continue development

For a new session, open this repository and start with the current checkpoint in [CODEX-HANDOFF.md](CODEX-HANDOFF.md) and the latest entry in [SESSION-LOG.md](SESSION-LOG.md). The log records completed work, the exact gameplay commit, publishing status, unfinished work and next steps; this close leaves no assigned next street. [AGENTS.md](AGENTS.md) instructs coding agents to read and maintain these records as they work.

A useful opening message is: **“Read AGENTS.md, CODEX-HANDOFF.md and `model-source/skills/reconstruct-street/SKILL.md`. Plan [street, from intersection, to intersection] to our Seventh visual standard, both sides and street details. Prepare the inventory and first bounded packet; do not implement or publish yet.”** Replace the bracketed scope and planning instruction with your actual next task. For branding/music work, point instead to [the experience brief](docs/DRIVEAROUND-EXPERIENCE-BRIEF.md).

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [model-source/NEIGHBORHOOD-NOTES.md](model-source/NEIGHBORHOOD-NOTES.md) before substantial changes. The deployed root entry point is `dist/seventh/index.html`; `dist/legacy.html` preserves the original ten-block game and `dist/prototype.html` preserves the earlier experiment.

The [current First & 7th report](model-source/FIRST-SEVENTH-PASS-08.md) identifies the corner recipes, reference dates, review captures and reproduction commands. For later fidelity work, [storefront-details.json](model-source/storefront-details.json) contains the explicit shop designs and photographic sources; [digital-twin-coverage.json](model-source/digital-twin-coverage.json) lists outstanding frontages. [STOREFRONT-PASS-05.md](model-source/STOREFRONT-PASS-05.md) explains compilation, affected-section export and browser review. The [clean reproduction verifier](scripts/verify-neighborhood-reproduction.py) works in a disposable copy, so it can check source data without resetting the playable exports.

Keep `dist/` in Git: it contains editable source and all required runtime assets. When changing models, roads, controls, module paths, or vehicle behavior, run:

```sh
npm run verify
```

These checks validate code, assets, and road/vehicle invariants. Browser frame rate, visual accuracy, and driving feel need separate hands-on review.

Original code is available under [MIT](LICENSE). Preserve the [third-party notices](THIRD-PARTY-NOTICES.md), [asset credits](dist/reconstruction/ASSET-CREDITS.md), and photographic provenance with redistributed copies.

## Local imagery access checks

These helpers document prior access; reopening the project is not an instruction to call them. The optional research helpers read `GOOGLE_MAPS_API_KEY` from the root `.env`, which Git ignores and the local game server does not serve. Keep credentials out of chat, commits and browser code. `node scripts/check-street-view-access.mjs` checks metadata; add `--image` to retrieve at most one potentially billable preview. Inspect and delete temporary previews after use. No key or Google service is required to play. `scripts/view-first-seventh-reference.mjs` supports bounded reference angles for the authorized corner; it is not an unattended citywide batch.
