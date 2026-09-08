# Run Borough Drive locally

The repository includes the active ten-block game, exported models, textures, reference data, and editable source recipes. You can play without rebuilding anything.

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

Import the GitHub repository and leave **Root Directory** at the repository root (the default). The checked-in [vercel.json](vercel.json) selects the **Other** framework preset, skips installation and building, and serves **`dist/`** as the website. The game is available at `/` on the deployed domain.

Do not use `npm run dev` or `npm start` as a Vercel build command: those commands start the local development server. All production files are already included in `dist/`.

If an earlier deployment shows `404: NOT_FOUND`, deploy the latest commit containing `vercel.json` and check that the project's Root Directory is still the repository root. Redeploying an older commit will retain its old configuration.

## Controls

- On foot: W/A/S/D to move, drag to look, Q/E to turn.
- Click **Drive**: W to accelerate, S to brake and then reverse, A/D to steer, Space to brake.
- M opens the travel map.
- Start at First Avenue and East 7th Street, facing north. R returns here in either mode.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Opening `dist/index.html` directly fails | Use the local HTTP server; modules and models need HTTP loading. |
| The 3D view cannot start | Use a browser with WebGL2 and hardware acceleration enabled. |
| Initial loading takes a moment | The detailed core model is about 24.4 MiB and needs to be decoded. |
| The address is already in use | Choose another port, such as `npm run dev -- 5174`. |
| Edits do not appear | Refresh the browser. The server does not provide hot reload. |
| Model or module loading fails after an edit | Run `npm run verify` and check the browser console. |

## Continue development

For a new session, open this repository and start with the current checkpoint in [CODEX-HANDOFF.md](CODEX-HANDOFF.md) and the latest entry in [SESSION-LOG.md](SESSION-LOG.md). The log records completed work, the exact gameplay commit, publishing status, unfinished work and next steps. [AGENTS.md](AGENTS.md) instructs coding agents to read and maintain these records as they work.

A useful opening message is: **"Read AGENTS.md, CODEX-HANDOFF.md and the latest SESSION-LOG.md entry, check the current Git state, and continue from the latest checkpoint."** Add the task you want to work on next.

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [model-source/NEIGHBORHOOD-NOTES.md](model-source/NEIGHBORHOOD-NOTES.md) before substantial changes. The active entry point is `dist/index.html`; `dist/prototype.html` preserves the earlier experiment.

Keep `dist/` in Git: it contains editable source and all required runtime assets. When changing models, roads, controls, module paths, or vehicle behavior, run:

```sh
npm run verify
```

These checks validate code, assets, and road/vehicle invariants. Browser frame rate, visual accuracy, and driving feel need separate hands-on review.

Original code is available under [MIT](LICENSE). Preserve the [third-party notices](THIRD-PARTY-NOTICES.md), [asset credits](dist/reconstruction/ASSET-CREDITS.md), and photographic provenance with redistributed copies.
