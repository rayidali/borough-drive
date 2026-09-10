# Borough Drive: continuation context

## Current checkpoint — 2026-09-10-09 (published and live-verified; batch process is brainstorming only)

Recorded **2026-09-10T15:03:43-04:00**. The user explicitly authorized pushing the saved work to `main`, and asked to brainstorm an unattended process that finds reference views itself, improves every part of the current map to the First & 7th standard, then eventually covers Manhattan/NYC. **“Don't implement anything yet” applies to new gameplay and job work.** This turn published the existing passes, verified production and refreshed publication/continuation records only. No AI worker, imagery acquisition or batch implementation ran.

- **Exact gameplay/source:** `c76dccebc143960498d21eeab8c55c2d0dbcc5ce`. **Published commit:** `5905b95ff3fcd2c111011ec73097af51dd25e100` (includes the source plus its checkpoint), fast-forward pushed from `477fcdb524407e189f67eb59771d8da84c4a16fe` to the existing `origin/main`. Resumed clean main five commits ahead, fetched first and found no divergence. No force push, new repository or new hosting project.
- **Live deployment:** Vercel success, deployment `3nNFK32d2P9W4E42BnT2aR9ey43G`, https://borough-drive.vercel.app. All **13 changed live files plus 5 preserved assets** matched source SHA-256 over HTTPS, including the three pass 08 corner GLBs, current runtime, core, street-material asset and decoder wrapper. [Publication evidence](model-source/publication-review-2026-09-10.json).
- **Actual validation this turn:** GitHub run `34516930981` passed both Node.js 22 and 24 `npm run verify` jobs. [Production browser smoke](model-source/browser-review-09/live-smoke.json) passed revision 09, fresh Automatic default, five starting sections, mode switch/reset and zero unexpected errors/failed requests. [Live game capture](docs/images/browser-09/live-first-seventh.png) inspected. Initial direct Node asset download and one GitHub detail request timed out; curl and the GitHub retry succeeded. No new local model rebuild, full 26-view review, source compilation, performance benchmark or photographic comparison was needed; prior pass 09 evidence below remains dated history.
- **Local/documentation state:** No game or worker code changed. Publication JSON, live screenshot/smoke, README/start/pass publication wording and these checkpoints are being saved in a separate documentation/evidence commit. Its own SHA/push state is visible in Git history/status; do not amend this checkpoint to insert its hash. Its `dist/` tree is identical to the verified publication. Any automatic deployment of that following documentation commit is distinct from the verified `5905b95ff3fcd2c111011ec73097af51dd25e100` deployment recorded here.
- **Brainstorming proposal, not implemented/approved:** a persistent coordinator chooses a block, assigns each facade/shop/street/intersection/secondary surface, finds dated full/oblique/detail views automatically, records observations, sends small bounded tasks to cheaper models, builds reusable recipes, renders comparisons, repairs limited failures and reports a block for review. Save progress/budget/source hashes so interruption does not restart completed work. Stronger models handle unusual architecture and failed reviews; visual acceptance and unresolved coverage remain explicit. Start by qualifying a few facades, then one complete block before wider map production. User should not have to manually feed each image. Runtime remains browser-first; city scale would need streamed tiles and distance-appropriate rendering, not loading all geometry at once.
- **Current workflow is still offline:** [BLOCK-WORKFLOW.md](model-source/BLOCK-WORKFLOW.md) inventories 1,348 ownership items and prepares/validates three-facade pilot packets. Automatic reference discovery, a persistent execution ledger, paid request dispatcher, coordinator/build/repair loop and automatic publication are not implemented. No scheduled job runs after this chat. Cheaper-model accuracy and end-to-end cost are unevaluated.
- **Google source issue remains:** technical API access works from the prior corner task, but the standard Maps terms §3.2.3 restrict extraction and creating content based on Maps content. Automatically viewing instead of retaining images, or manually uploading Google screenshots, does not by itself establish permission for the proposed derived-content pipeline. A Google adapter would require suitable permission; owner-supplied or appropriately licensed images can enter the same proposed acquisition stage. No new Google imagery request this turn; the local key remains outside `dist/` and Git.
- **Next concrete step:** continue brainstorming the coordinator, automatic source acquisition/permissions and review granularity with the user. Do not implement the pipeline, expand buildings, run paid jobs or resume Unreal without their next instruction. Review the published corner in **Graphics → Automatic**. Prior limits remain: dense driving is not consistently 60 FPS; hidden/unmeasured facade details are unresolved; compiler height resets must be addressed before unattended exports.

## Previous checkpoint — 2026-09-10-08 (browser pass and offline block workflow saved locally)

Recorded **2026-09-10T05:57:24-04:00**. The user chose smooth browser exploration inspired by slowroads.io, deferred Unreal, and requested improvement of First & 7th followed by a repeatable process suitable for cheaper AI workers. The current corner is the working visual reference; no wider modeling, paid batch or publication began. The prior engine assessment is historical advice, superseded by this direction.

- **Exact gameplay/source:** `main` at `c76dccebc143960498d21eeab8c55c2d0dbcc5ce`. This commit contains [browser pass 09](model-source/BROWSER-PASS-09.md), [the offline block workflow](model-source/BLOCK-WORKFLOW.md), updated current documentation and durable review evidence. Source/model baseline was `219d4e9ccec8e019351d3a27d7dff6dcaf07237d`; session-start documentation HEAD was `4682fef`. Only these two checkpoint documents remained modified before their separate save; identify that documentation commit through Git history. No unfinished runtime/model edits.
- **Runtime:** main-depth ambient shading avoids another city draw; Automatic is the default for new visitors and adapts pixel work during motion, restoring ratio 1/contact shading once stopped. Saved quality preferences are honored. Added authored static clouds and bounded First & 7th asphalt/paint variation, plus fixed-step driving-view interpolation. Physical driving, collisions, 72 checked reconstruction assets/manifests/support modules and the accepted First & 10th geometry are byte-identical to pass 08. No Blender rebuild or new photographic detail claim.
- **Actual performance:** Chrome 152 / Apple M1 / 1440×1000 DPR 1, local HTTP: Saifee Detailed 48.9→52.4 FPS; submitted triangles 3.83M→1.92M, calls 596→301. Automatic warm corner 60.0 FPS; additional warm northbound drive 48.0 FPS overall, final 120 rendered frames 55.9 FPS, reaching ratio 0.70/contact shading off. Detailed drive 27.1→32.9 FPS; fixed-frame paths differ in duration/distance. Stopped Automatic restores quality; idle redraws zero. Local ready 671→525 ms, initial reconstruction transfer about 40.76 MB. These short single-device samples do not establish sustained 60 FPS or slowroads.io parity. Final data: [before/after and preservation](model-source/browser-review-09/).
- **Actual checks:** `npm run verify` passed on final runtime (30 modules, 2,308 road samples, unchanged vehicle/source/export/material/spatial invariants, new frame-budget/interpolation tests). `python3 scripts/verify-block-workflow.py` passed; saved unresolved pilot validates against current sources. Final [26-view browser review](model-source/browser-review-09/review.json) passed fresh Automatic default, controls, resets, quality persistence, idle wake, deferred-core failure/retry and startup fallback/retry with zero unexpected errors/failed requests. Inspected final corner/shop/driving captures; 11 selected unedited captures are in [docs/images/browser-09](docs/images/browser-09/). No new source compilation or Google comparison this turn. Whitespace and 308 relative Markdown links checked before this checkpoint; 336 eligible files scanned with no local credential matches. Ignored root `.env` remains 0600, outside served `dist/`.
- **Workflow:** deterministic inventory of 1,348 ownership items: 672 facade sections, 615 secondary-surface reviews, 43 street segments, 18 intersections. Protected core cannot receive a worker packet; v1 emits only unprotected facade packets. Three-task offline plan, minimal Tile Bar packet, permission/source registry and proposal validator are committed. Patch headers/declarations are checked; actual record changes and visual fidelity still require coordinator review. No automatic merge/build dispatcher, completion ledger or paid runner exists. GPT-5.4 Mini is an unevaluated candidate; illustrative Batch token allowance is $0.162 for three jobs, not a measured end-to-end quote or billing cap. Zero model API requests, model evaluations or background jobs ran.
- **Imagery:** current Google Maps terms §3.2.3 restrict bulk extraction/caching and creating derived content. A working API key or deleting previews does not establish permission for the proposed automation. New Google batch ingestion is disabled; use owner-supplied or appropriately licensed images with permission covering processing/derivatives. No such source is registered yet. Preserve existing pass 08 provenance. No credential belongs in a packet or checkpoint.
- **Remote/publication:** no fetch, push, CI run or deployment this turn. Cached `origin/main` remains `477fcdb524407e189f67eb59771d8da84c4a16fe`; source commit is four commits ahead and the following checkpoint will be a fifth. Last verified public source is `522cd1de77b72186dc98e06a3b9f6ce4db761d8b`, verified September 9 at https://borough-drive.vercel.app; current live state was not rechecked. Passes 08 and 09 remain local.
- **Preview/next action:** opened http://127.0.0.1:5173 and confirmed HTTP 200 / revision 09. Restart with `npm run dev` after closure; select **Graphics → Automatic** if a saved Detailed choice remains. First review the corner presentation/speed on the user's device, then register suitable full-facade/oblique images and qualify the cheaper worker on three facade tasks. Measure correction cost and rendered accuracy before expanding to the adjacent block. No automatic migration, wider expansion, paid work or publishing. Dense-view performance, unmeasured/hidden architectural details and the older compiler's three non-corner render-height resets remain unresolved; see the two current reports.

## Previous checkpoint — 2026-09-10-06 (engine direction assessed; game unchanged)

Recorded **2026-09-10T05:02:39-04:00**. The user asked whether the sky, roads and driving can reach a PS5-game standard in the browser, or whether Unreal should provide the final runtime while the current pipeline supplies models. [Engine assessment and proposed corner test](model-source/ENGINE-DIRECTION.md) recommends Blender/source recipes for authoring, Three.js for browser inspection, and an early First & 7th Unreal test before map-wide production. **This is a recommendation, not a user-approved migration decision.** No browser upgrade or Unreal implementation was made in this assessment.

- Gameplay/source remains local `219d4e9ccec8e019351d3a27d7dff6dcaf07237d`. Session-start HEAD `179c994` was clean on `main`, two commits ahead of cached `origin/main`. The only new changes are the assessment and these checkpoint documents, saved in a following local documentation commit; identify it with Git history.
- Read the pass 08 checkpoint below for completed corner work, performance, sources and remaining visual differences. User acceptance remains pending. No new fetch, push, deployment or live verification; September 9 source `522cd1d` remains the last verified publication.
- Read-only inspection confirmed the sky/light setup, flat runtime roads, planar vehicle physics, tile-wide material merging, required Draco compression, external textures and corner vertex colors. Official Epic documentation was checked for atmosphere/Lumen, Chaos, glTF, modular-mesh limitations, macOS hardware and Pixel Streaming. Import and Unreal performance are untested. No game verification was rerun because no game, source model or export changed.
- Proposed next action: settle the engine direction with the user. If they choose Unreal, start with a separate modular export of First & 7th and one driveable street segment; establish materials/lighting/handling and a hardware budget before expansion. If they prefer a browser upgrade, define a bounded sky/road/driving pass and retain performance checks. Do not infer migration, paid GPU hosting or citywide jobs from this recommendation.

## Previous checkpoint — 2026-09-10-05 (Street View refinement committed locally; visual acceptance pending)

Recorded **2026-09-10T04:36:37-04:00**. The user authorized using the working Street View API to improve all four corners of First Avenue/East 7th toward the attention to detail and visual quality of Assassin’s Creed Unity. The bounded five-building, nine-elevation, eight-shop refinement is implemented, exported, reviewed and committed locally. **This remains a stylized reconstruction with documented differences, not a perfect 1:1 or AAA-quality result.** User acceptance of pass 08 is pending; revision 06 remains the accepted minimum standard. Wider expansion and jobs remain deferred.

| Item | Current state |
| --- | --- |
| Exact local gameplay/source commit | `219d4e9ccec8e019351d3a27d7dff6dcaf07237d` — Refine First and Seventh from dated Street View observations |
| Previous published gameplay | `522cd1de77b72186dc98e06a3b9f6ce4db761d8b`, performance pass 07. Session-start checkpoint HEAD was `477fcdb524407e189f67eb59771d8da84c4a16fe`; its uncommitted local API setup and notes were preserved and completed. |
| Branch and local changes | `main`; implementation, three GLBs, sources, helpers, current docs and 37 game PNGs saved in the source commit. Only this handoff and session log remained modified before their separate checkpoint commit. No pending export or browser capture. Identify the checkpoint documentation commit using Git history. |
| Push state | No fetch or push in this refinement turn. Cached `origin/main` remains `477fcdb524407e189f67eb59771d8da84c4a16fe`; current remote state was not rechecked. The new source and following checkpoint commit are local. |
| Deployment state | This pass is not deployed. Production was not rechecked; the September 9 verification of `522cd1d` below remains historical. Local preview at http://127.0.0.1:5173 was opened in the user's browser after verification. Use `npm run dev` to reopen later. |
| Sources actually inspected | Eight dated Street View panoramas: six April 2026 views around the intersection, two closer west/Yubu views from September 2024. A nearest November 2017 selection was rejected for current claims. [Observation record](model-source/first-seventh-street-view-08.json) preserves public links, IDs, camera angles and uncertainty. |
| Changes | Tile Bar canopy/return; current Monkey/Hen signs; E7 return, displays and painted panels; Burger red blade/dining enclosure; E Smoke brick/window layout; Yubu shutter hardware; Saifee service windows, two red-brown escapes and complete side hardware/plant frontage; open escape grating, window hardware, utility lids, signals and red tactile paving. [Pass 08 report](model-source/FIRST-SEVENTH-PASS-08.md). |
| Preservation | Only `block-5-1`, `block-5-2`, `edge-south` rebuilt. Twenty-four protected files match the earlier source byte for byte: First & 10th model/recipe/photos, viewer/vehicle/glass/spatial/shared-texture code and eleven other GLBs. All 615 mapped footprints/frontages/heights, roads and bounds preserved. [Evidence](model-source/first-seventh-08-preservation.json). |
| Final technical checks | `npm run verify` passed after final review metadata: 26 modules, 2,308 road samples, collision/navigation/export signatures, exact street materials and spatial batching. Clean prepare/compile reproduced 615 buildings and all three audits. Final GLBs match recorded performance hashes. `git diff --check` passed; 251 relative links across all 19 Markdown files resolved before this final checkpoint refresh. |
| Browser and visual review | [26 final views and controls/recovery](model-source/first-seventh-08-final-review.json), [11 reference-position views](model-source/first-seventh-08-matched-review.json), [37 final game screenshots](docs/images/first-seventh-08/). Start/driving/resets, quality persistence, idle wake, deferred-core retry and startup fallback/Retry passed. Expected injected-failure warning only; no unexpected errors/failed requests. Final inspection confirmed Burger glazing is uncovered and mortar pattern retained. Matching GPS/angles with estimated 2.50 m camera height does not eliminate observed framing/proportion differences. |
| Performance | Chrome 152 / Apple M1, 1440×1000 DPR 1: Saifee Detailed 48.9 FPS, Faster 60.0, northbound driving stress 26.8, First & 10th SE 27.8; 38.86 MiB initial reconstruction transfer; zero idle scene redraws. Total neighborhood models 52.40 MiB / 9,435,099 triangles (+0.49%), maximum 63 material batches. Matte vertex-color batching and surface mortar bands limit the added cost. [Conditions and limits](model-source/first-seventh-08-performance.json). |
| Credentials and images | API key stays in ignored, owner-only root `.env`, outside served `dist/`. Repository scan found no key in 302 eligible files. All 25 temporary Google reference JPEGs were deleted after inspection; no Google pixels enter game assets or tracked screenshots. Access helpers print no keys or authenticated URLs. |
| Remaining quality limits | Exact murals/logos/font outlines, unreadable print, measured dimensions, complete occluded Yubu/Burger arrangements, interiors and some movable objects remain estimates. Lighting, vehicles and vegetation remain stylized. The gap report is not a claim those details are fixed or that the user’s 1:1 standard has been reached. |
| Next concrete step | Have the user review local chapter 08 with the four corner buttons and compare the recorded reference angles. Continue from their specific feedback on this corner; do not treat this checkpoint as visual acceptance, a deployment instruction or permission to expand the map. |

The current recipes are [first_seventh_refinement.py](model-source/first_seventh_refinement.py), [first_seventh_kit.py](model-source/first_seventh_kit.py), [first-and-seventh.json](model-source/first-and-seventh.json) and [storefront-details.json](model-source/storefront-details.json). The new refinement file participates only in affected corner export signatures. Before recompiling, note the inherited compiler behavior documented in the report: it resets three older non-corner `renderHeight` values (`241822303`, `241829661`, `248142640`); preserve their existing exported heights if their models are not rebuilt. Do not compile during a Blender export. All final exports and source checks are already complete.

## Previous checkpoint — 2026-09-09-03 (speed optimization published and verified)

Recorded **2026-09-09T01:19:25-04:00**. The user accepted **First & 7th revision 06 as the minimum completion standard**, authorized speed optimization and a push to main, and requested updated Markdown. The speed pass is implemented, pushed and verified live at **https://borough-drive.vercel.app**. The next discussion is an economical, repeatable street/block process for the existing East Village and eventually Manhattan/NYC. **No expansion or background jobs should start automatically.**

| Item | Checkpoint state |
| --- | --- |
| Exact gameplay/source commit | `522cd1de77b72186dc98e06a3b9f6ce4db761d8b` — Speed up neighborhood loading and rendering while preserving corner detail |
| Accepted visual baseline | `0f40856c9c576d1648ddae9c6e76bb550a98b42a`, First & 7th revision 06; five buildings, nine elevations and eight shop treatments. Accepted by the user September 9 as the minimum standard. |
| Checkpoint documentation | Publication records follow the source in a separate documentation commit. Identify that commit with `git log -- CODEX-HANDOFF.md SESSION-LOG.md`; do not amend to insert its own hash. No unfinished code/model export. |
| Implemented performance work | Exact street-material bootstrap; deferred First & 10th loading with retry; shared surface downloads/decodes; lossless spatial batches; thin clear glass with physical reflections; no idle scene redraws; frustum-culling of local lights; lazy fallback photo; current vendored HDR loader. |
| Preserved quality/data | Every original GLB, both accepted corner recipes, surface maps, six licensed core photographs and vehicle code byte-identical to revision 06. All manifest data identical except acceptance/scope metadata. Detailed remains default with AO/four samples. Tiny volumetric glass refraction is approximated by a thin pane. |
| Current inventory | 615 mapped objects; 411 photo-observed non-core records; 214 supported names, including 204 non-core; 27 individual non-core shop designs, 177 supported non-core names still estimated. 141 objects with a mapped frontage lack an individual photo record. |
| Local and remote | Resumed from clean `e86a480`, two unpublished commits ahead of `a44257a`. Fetched and preserved that work. Fast-forward push `a44257a..522cd1d` to the existing `rayidali/borough-drive` main succeeded. Final publication records are a following documentation-only commit. |
| Deployment | Vercel reported success for source `522cd1d`: [deployment](https://vercel.com/rayidalis-projects/borough-drive/6CxayAae3s7cYSh1cHWNHUy7YA18). All 20 game files changed since published pass 05 matched source byte for byte over HTTPS. Eight additional preserved assets also matched: core, six photographs and Draco WASM. [Publication evidence](model-source/publication-review-2026-09-09.json). |
| Verification | Local `npm run verify`; 26 modules, 2,308 road samples, navigation/vehicle/collision/source signatures; exact street-material subset; lossless triangle/UV/normal/transform/bounds tests. Clean prepare/compile reproduced source fields and three audits. [GitHub Actions](https://github.com/rayidali/borough-drive/actions/runs/34314169298) passed on Node.js 22 and 24. 212 relative Markdown links checked before publication. |
| Browser review | 26 final views plus two travel captures. Start/northbound driving/both resets/core/corner controls/quality persistence/idle wake-up passed. Injected deferred-core failure retried automatically; startup failure showed its lazy photograph and Retry restored play. No unexpected errors. Live browser smoke passed at the production URL: all five starting sections loaded, detailed Saifee view rendered, zero errors or failed requests. |
| Measured performance | Chrome 152 / Apple M1, 1440×1000 DPR 1: Saifee Detailed 25.2→50.2 fps; core SE 17.9→28.6; northbound streaming stress 20.7→28.1; Faster 56.5→60.0. Initial reconstruction transfer 89.61→38.24 MiB (about 57% less), shared image requests 42→9. Settled scene redraws fall to zero. Short local tests, not a universal device/route guarantee. |
| Remaining limits | Dense views/driving still below 60 fps on this device. New shader compilation/retina viewports can cost more. Photograph dates vary; Google panorama access, surveyed dimensions, unseen surfaces and precise artwork remain unresolved. Acceptance is a quality decision, not survey certification. |
| Next concrete step | Review the published speed improvements on the user's device, then discuss the economical block/street workflow. Use the accepted benchmark, source provenance, existing coverage inventory and per-device performance checks. Do not start new geographic work, paid imagery services or unattended batches without that later instruction. |

Read [Performance pass 07](model-source/PERFORMANCE-PASS-07.md), [before/after measurements and asset hashes](model-source/performance-review-2026-09-09/), [accepted corner report](model-source/FIRST-SEVENTH-PASS-06.md) and [source observations](model-source/first-and-seventh.json). All 18 project Markdown documents were refreshed; 28 final local PNGs and one live-site capture are tracked in `docs/images/performance-07/`. No Blender rebuild, engine migration, Firecrawl setup, API key or new photographic source was needed. The performance report records official Street View access options and extraction/derived-content restrictions for the later discussion. Credentials remain local.

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
5. Preserve the accepted First & 7th minimum standard and follow the user's current scope/publishing instructions. The wider process awaits the next planning discussion. For an authorized game publication, include all required models, textures, manifests, runtime modules and source records. Confirm deployment success and compare live content with the intended commit before describing it as live.
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

The public game is connected to this repository's `main` branch. The repository-root `vercel.json` serves `dist/` directly and skips installation and building. Historical gameplay passes include revision 04 in `835ea6c` and pass 05 in `63757cb`. First & 7th revision 06 is accepted; performance pass 07 improves the runtime. Exact current source/push/deployment states are recorded above.

Rayid wants to build a driving game in a recognizable digital twin of New York City, eventually Manhattan and then NYC. The immediate approved scope is ten connected East Village blocks around First Avenue and East 10th Street: East 7th to East 12th, Second Avenue to Avenue A.

The user knows this neighborhood and rejected generic buildings with real business names. Google photorealistic tiles were closer but still did not meet the desired street-level quality. The accepted approach is authored 3D geometry based on actual map footprints and photographic observations. First & 10th is the most individually detailed core and should remain the quality anchor.

Desired atmosphere: cozy, aesthetic, warm, calm exploration, with the relaxed feeling of slowroads.io but substantially stronger geographic and architectural fidelity. Prioritize recognizable facades, building proportions, rooflines, fire escapes, storefront openings, cornices, windows, signage, sidewalk details, materials, and good driving feel. Preserve real geometry while improving lighting and presentation.

Do not mistake a verified business name for a verified facade. Storefront availability and architectural reference dates must remain separately documented. Unknown occupants should stay unnamed; historical signs must remain marked as historical.

## What currently exists

- Ten complete blocks plus four boundary sections, covering three avenues and six cross streets.
- 615 building objects including five restored municipal footprints, annexes and boundary context; this is not 615 independently verified facades.
- 411 additional building records with photographic observations, from 459 combined source records. Coverage varies from storefront observations to fuller facades.
- 620 municipal footprint matches, PLUTO 26v2 parcel attributes and 214 independently supported named place records, including 204 outside the core; September 8 removed two duplicate identities. The audit retains excluded and unresolved entries.
- Blender-generated Draco GLBs with shared textures, streamed by distance.
- A highly detailed preserved First & 10th core, map travel, walk/drive modes, collision, fixed-step vehicle simulation, street props, warm lighting, and source/accuracy information.
- Business baseline checks dated September 6, 2026, two identity corrections/exterior review dated September 8, and OSM snapshot dated September 5. Image dates vary. Twenty-seven non-core shops have explicit exterior designs; remaining named shop designs are estimated.

This remains a reconstruction prototype with uneven detail. There are 141 non-core objects with mapped frontages but no individual photographic observation. Secondary elevations, some road widths, furniture positions, trees, interiors and unseen geometry remain estimated. Many archive photographs have 2012 upload dates and unknown capture dates. Do not describe it as a surveyed, fully current digital twin. Pass 05 browser checks are linked above; older validation below remains historical.

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

## Later map-wide work — bounded pilot prepared

First & 7th revision 06 remains the accepted minimum; pass 08 is the current working visual reference and pass 09 improves browser presentation. The [block workflow](model-source/BLOCK-WORKFLOW.md) now supplies the finite inventory, small pilot plan, source registry and offline proposal validation. Its next step is authorized full/oblique imagery and a three-facade cheaper-model evaluation, followed by rendered review before adjacent-block work. Manhattan/NYC remain longer-term objectives. A working local Google key exists but does not establish permission for the new automated workflow. No engine migration, Firecrawl service, paid worker or citywide expansion has started.

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
