# October 24 publication verification

<!-- current-project-status -->
> **Current status:** The [project handoff](../../CODEX-HANDOFF.md) governs current scope, publication and next work. This file retains its dated observations, evidence or specialist instructions. See [browser scaling](../../docs/BROWSER-SCALING.md) for the current loading/rendering work; older model counts and paused states describe their original checkpoints.
<!-- /current-project-status -->

The user authorized publication of the complete existing 295-model build, then continuation with East Tenth, Second–First, both sides. The runtime/source release is `de27f5a212d49688a4a74519ac208a628925e777`; subsequent evidence commits preserve the saved game-review captures. Both private user screenshots and the workstation-only workspace remain local.

The original-game, export/preservation and workflow checks passed locally. The original/export checks also passed from an isolated checkout of the staged release, without ignored caches or local-only files. GitHub Node 22 and Node 24 jobs succeeded for `de27f5a`; Vercel reported deployment success. [CI run](https://github.com/rayidali/borough-drive/actions/runs/40153203183) and [deployment](https://vercel.com/rayidalis-projects/borough-drive/7S5HmiWN454iXPM1XzAwzTiDB2x7).

The first production HTTP audit matched all 314 required runtime files and all five route/manifest byte checks. It also found a real hosting defect: a missing content-hashed scene returned 404 with `public, max-age=31536000, immutable`. [Initial evidence](hosting-before-cache-repair.json).

The repair gives the static filesystem a chance to serve existing assets before a dedicated area-file 404 response sets `Cache-Control: no-store`. Existing content-hashed assets keep their immutable headers; root and legacy route mappings remain explicit. Vercel's [routing phases](https://vercel.com/docs/build-output-api/configuration#handler-route) document the filesystem-miss behavior. The offline route contract exercises all shipped files and four missing scene/manifest cases; the final deployed check remains separate.

This is a hosting-only repair. All runtime payloads, authored/compiled models and engine sources remain unchanged; only the build manifest's `vercel.json` source digest is refreshed to identify the deployed hosting configuration. No model import or export was performed. The exact PCK remains `b0100bd00b509f41afce60e8648e42c6892664b73c4757fc8ba49300f2d2b9ab`.

**Final release `888f5b8` is pushed and verified.** Both Node jobs pass in [the final CI run](https://github.com/rayidali/borough-drive/actions/runs/40154754104); [Vercel reports success](https://vercel.com/rayidalis-projects/borough-drive/Exqb762rf4qaLvD7beyc1We51F1X). The [final HTTP audit](hosting.json) matches all 314 runtime files and five route/manifest checks, preserves immutable caching for existing scene/manifest files, and confirms a missing scene returns 404 with `no-store`. [Release metadata](release.json).

The unchanged production game also passes eight driving routes, eight boundaries, four camera modes/reset and all 41 assigned-owner assertions, with 295 models resident and no console errors/warnings or failed requests. [Browser summary](gameplay/summary.json) · [full capture/assertion record](gameplay/captures.json). Three representative images were inspected from 21 captures. The browser run preceded the hosting-only repair; the final HTTP audit afterward proves identical engine payloads and the repaired routing. No new game code required a repeated driving run.

The single production route pass is not a fresh cold/warm startup distribution, paired performance benchmark or repeated all-business fidelity audit. Existing source-date, tenant and performance limitations remain in the October 15 block report. Tenth ownership preparation is local follow-on work, not a completed or published new block.
