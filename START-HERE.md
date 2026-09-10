# Run Borough Drive locally

The repository includes the active ten-block game, exported models, textures, reference data, and editable source recipes. You can play without rebuilding anything.

## Resume state — September 10, 2026

The owner accepted [First & 7th revision 06](model-source/FIRST-SEVENTH-PASS-06.md) as the minimum completion standard: five individual building profiles, nine exposed elevations and eight shops. [Performance pass 07](model-source/PERFORMANCE-PASS-07.md) preserves those models while improving startup, rendering and idle GPU use. The user subsequently authorized [pass 08](model-source/FIRST-SEVENTH-PASS-08.md), a local Street View-based refinement of this corner. The exact source, push and verified deployment states are recorded in the handoff; the earlier performance publication does not mean this refinement is deployed. An economical block/street process is now prepared for a small pilot before wider East Village work; Manhattan/NYC remain longer-term objectives.

The latest direction is browser-first: Unreal is deferred. [Browser pass 09](model-source/BROWSER-PASS-09.md) improves the corner's presentation and rendering; [the block workflow](model-source/BLOCK-WORKFLOW.md) prepares small offline worker packets and a finite coverage inventory. No paid AI batch or wider building pass has started. Google API access does not establish permission for bulk/derived-content processing; the new workflow requires suitable imagery rights.

Read the current [handoff](CODEX-HANDOFF.md) and latest [session log](SESSION-LOG.md), then run `git status --short --branch` and `git log -5 --oneline`. Preserve local changes and check the recorded publishing state before pulling or pushing. Existing models are included; old servers, temporary photo folders and browser sessions are not needed to recover the project.

## Start the game

Use Node.js 22 or newer. From the repository folder, run:

```sh
npm run dev
```

Open **http://127.0.0.1:5173** in a browser. Leave the terminal running; press Ctrl+C to stop the server. If the port is occupied, run `npm run dev -- 5174` and open http://127.0.0.1:5174 instead.

There is no `npm install` step. Runtime libraries and assets are bundled. Blender is optional and only needed to regenerate models. Once the repository is downloaded, the game can run locally without internet access. External source links still need a connection.

The server serves only `dist/` and listens on your computer's loopback address. It does not expose the repository or game to other devices.

## Python alternative

If Python 3 is already installed:

```sh
python3 -m http.server 5173 --bind 127.0.0.1 --directory dist
```

On Windows, use `py` in place of `python3` if needed.

## Host on Vercel

The existing project connects [rayidali/borough-drive](https://github.com/rayidali/borough-drive) to [borough-drive.vercel.app](https://borough-drive.vercel.app), deploying from `main`. Use that setup when continuing this project. For a separate fork, import its GitHub repository and leave **Root Directory** at the repository root (the default). The checked-in [vercel.json](vercel.json) selects the **Other** framework preset, skips installation and building, and serves **`dist/`** as the website. The game is available at `/` on the deployed domain.

Do not use `npm run dev` or `npm start` as a Vercel build command: those commands start the local development server. All production files are already included in `dist/`.

If an earlier deployment shows `404: NOT_FOUND`, deploy the latest commit containing `vercel.json` and check that the project's Root Directory is still the repository root. Redeploying an older commit will retain its old configuration.

## Controls

- On foot: W/A/S/D to move, drag to look, Q/E to turn.
- Click **Drive**: W to accelerate, S to brake and then reverse, A/D to steer, Space to brake.
- M opens the travel map.
- First & 7th detail-study buttons frame each of the four corners.
- Graphics defaults to Automatic for new visitors; saved choices are preserved. Automatic adapts pixel work during slow motion and restores a sharper stopped view. Detailed and Faster remain available.
- Start at First Avenue and East 7th Street, facing north. R returns here in either mode.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Opening `dist/index.html` directly fails | Use the local HTTP server; modules and models need HTTP loading. |
| The 3D view cannot start | Use a browser with WebGL2 and hardware acceleration enabled. |
| Initial loading takes a moment | Nearby section models and a 4.18 MiB street-material asset load first; First & 10th streams when approached. |
| The address is already in use | Choose another port, such as `npm run dev -- 5174`. |
| Edits do not appear | Refresh the browser. The server does not provide hot reload. |
| Model or module loading fails after an edit | Run `npm run verify` and check the browser console. |

## Continue development

For a new session, open this repository and start with the current checkpoint in [CODEX-HANDOFF.md](CODEX-HANDOFF.md) and the latest entry in [SESSION-LOG.md](SESSION-LOG.md). The log records completed work, the exact gameplay commit, publishing status, unfinished work and next steps. [AGENTS.md](AGENTS.md) instructs coding agents to read and maintain these records as they work.

A useful opening message is: **"Read AGENTS.md, CODEX-HANDOFF.md and the latest SESSION-LOG.md entry, inspect Git and publication state, and preserve the accepted First & 7th minimum standard and measured performance improvements. Keep the browser-first direction, read the block workflow, and use my next instruction for the corner/pilot; do not start paid batches or expansion automatically."** Add your review or next task.

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [model-source/NEIGHBORHOOD-NOTES.md](model-source/NEIGHBORHOOD-NOTES.md) before substantial changes. The active entry point is `dist/index.html`; `dist/prototype.html` preserves the earlier experiment.

The [current First & 7th report](model-source/FIRST-SEVENTH-PASS-08.md) identifies the corner recipes, reference dates, review captures and reproduction commands. For later fidelity work, [storefront-details.json](model-source/storefront-details.json) contains the explicit shop designs and photographic sources; [digital-twin-coverage.json](model-source/digital-twin-coverage.json) lists outstanding frontages. [STOREFRONT-PASS-05.md](model-source/STOREFRONT-PASS-05.md) explains compilation, affected-section export and browser review. The [clean reproduction verifier](scripts/verify-neighborhood-reproduction.py) works in a disposable copy, so it can check source data without resetting the playable exports.

Keep `dist/` in Git: it contains editable source and all required runtime assets. When changing models, roads, controls, module paths, or vehicle behavior, run:

```sh
npm run verify
```

These checks validate code, assets, and road/vehicle invariants. Browser frame rate, visual accuracy, and driving feel need separate hands-on review.

Original code is available under [MIT](LICENSE). Preserve the [third-party notices](THIRD-PARTY-NOTICES.md), [asset credits](dist/reconstruction/ASSET-CREDITS.md), and photographic provenance with redistributed copies.

## Local imagery access checks

The optional research helpers read `GOOGLE_MAPS_API_KEY` from the root `.env`, which Git ignores and the local game server does not serve. Keep credentials out of chat, commits and browser code. `node scripts/check-street-view-access.mjs` checks metadata; add `--image` to retrieve at most one potentially billable preview. Inspect and delete temporary previews after use. No key or Google service is required to play. `scripts/view-first-seventh-reference.mjs` supports bounded reference angles for the authorized corner; it is not an unattended citywide batch.
