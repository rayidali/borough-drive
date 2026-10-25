# P01 — 137–143 First Avenue

<!-- current-project-status -->
> **Current status:** The [project handoff](../CODEX-HANDOFF.md) governs current scope, publication and next work. This file retains its dated observations, evidence or specialist instructions. See [browser scaling](../docs/BROWSER-SCALING.md) for the current loading/rendering work; older model counts and paused states describe their original checkpoints.
<!-- /current-project-status -->

**October 12, 2026 — complete locally; awaiting user review.** The user’s “go onto next” starts the first facade packet after EV-003. Four west-side properties and seven observed businesses are implemented. The exact schedule, dated evidence, unsuccessful trials and final review records live in [the packet](east-village-p01/). No P02 or publication is started.

The previous 203 authored and compiled building files are unchanged. P01 adds four independently loaded scenes and extends First Avenue alone to the visible terminal at z=−145, with outer cap −150. Other avenues remain at −119. Ninth is closed; the address HUD retains its Seventh-only boundary. Existing controls, audio, interface and legacy map are preserved.

## Source and authoring

[Observations](east-village-p01/observations.json) retain full ordinary-browser Street View locators and inspection dates. April 2026 is the ground-floor target; the September 2024 141/143 view supplies upper-elevation detail only. Its Smart Smokers identity is superseded by April’s observed Paquitos/Banshee arrangement. No reference photographic pixels enter the repository or runtime. Municipal footprints/heights are inherited; visible dimensions and movable fixtures are estimates.

| Property | Individual businesses / defining features |
| --- | --- |
| 137 | Spirals: powder-blue joinery, italic serif sign, separate lighting bar, dated window collaboration marks, pane arrangement and black brick base. Crispy Burger: orange molded piers, cream/red sign and chicken emblem, open glass leaf, red food panels, green neon and menu board. |
| 139 | V-One Nail Spa: orange script/charcoal sign, fine silver framing, circular nail graphics, coral chairs, polish display and white menu board. SKWR: green fascia/skewer, large white letters, narrow entry, purple Open sign and window counter. |
| 141 | Kikoo: custom letter strokes/bowl mark, sushi substrip, thin bronze framing, vertical blue tubes, menu layers and pale near-window chairs. Separate numbered residential portal with its rounded light. |
| 143 | Paquitos: tall red letters/sombrero, divided glazing, red chair and low blue menu. Banshee: burgundy/ivory curved canopy, scalloped hem, two-sided Guinness blade, green timber and white window name. Central residential entrance retained without inventing an unreadable number. |

There are 68 upper window groups (20/16/16/16), four residential entrances, separately composed cornices/hoods and three observed fire escapes. Source-based sparse/leafy trees, school streetlight and U-rack are authored in a packet-only street dressing script. Protected 83 St. Marks, 134 First return and Tile Bar receive read-only game comparisons.

The first rendered pass exposed small sign lettering, a red-shifted burger palette, generic menu boards and a misplaced open-door handle. Subsequent passes repaired these, removed an unsupported SKWR board, sealed shallow display side walls, reduced the Banshee notice and removed an invented bottle lineup. Exact logo artwork, tiny menu copy, finish and dimensions remain approximations; hidden interiors are unknown. The partially obscured 137 leaf/fixed split is explicitly uncertain. This is not calibrated 1:1 acceptance or a numerical “100×” score.

## Reproduce

`python3 model-source/author_p01.py` writes the independent packet schedule. `p01_kit.py` consumes it after the unchanged shared kits; old 08/09 schedules must not be rerun for P01. For packet-only recipe changes, export all four explicit IDs with Blender, then run `npm run seventh:build` and `npm run seventh:verify`. Shared recipe changes require the full export.

```sh
blender -b -t 4 --python-exit-code 1 --python model-source/export_seventh_engine.py -- --only 241822278 --only 241822337 --only 241822304 --only 241822211
node scripts/review-p01.mjs model-source/east-village-p01/new-review
node scripts/review-p01.mjs model-source/east-village-p01/new-routes routes
```

Review requires the local server and an isolated review browser on port 9222. Capture is not acceptance: inspect full elevations, overlapping ground views and all front/left/right business views. The old 102 First/St. Marks and 82 Seventh review faces stay separate from four `packetReviewFrontages`.

## Verification and timing

Final package: **7,991,408 bytes**, SHA256 `d79b539d31a624ba19f32fdcd86f02888f16d54989abd99e4d6733c913145656`; 226 runtime files / 120 source hashes. [Preservation](east-village-p01/preservation.json) checks all 203 old GLBs/compiled scenes, 2,372 other tracked non-Markdown files and both unchanged/untracked private screenshots.

[Storefront review](east-village-p01/visual-review.json) covers 36 inspected images: 21 business views, four elevations, eight overlapping ground views and three protected neighbors. [Driving](east-village-p01/routes-final/captures.json) verifies four routes, four held-throttle barriers, four camera modes and reset; 17 legacy address cases pass. Required `seventh:verify` and original `verify` pass.

Five cold starts: median 6.598 s / p95 7.297 s. Five cache-enabled starts: 8.965 s / 9.687 s. [Raw startup/route metrics](east-village-p01/metrics.json). Five-run p95 is the maximum; browser-cold is not OS/GPU/WASM-cold. EV-003 measurements are historical, not a new paired control. The warm median is about 35.5% slower than the historical EV-003 warm run; this session does not establish the cause or claim a startup-speed win. All 207 scenes hit browser cache on repeat. Earlier stale-server timings are retained separately. New scenes add roughly 2.9 MB to the retained set; all 207 still open initially. No whole-area scalability claim.

P01 elapsed about **78 minutes** through the handoff, including research, first geographic adapter, failed/repaired build/review trials and documentation. Retain the provisional whole-area forecast until P03.

The last build rotates only the new north terminal label toward the driver. [Final label capture](east-village-p01/terminal-final/terminal-facing.png) is inspected. The 36 storefront images, route tests and timings identify the immediately preceding package; all 207 scene hashes and the area manifest are identical. Only `world.gd` differs in the source manifest. Required package verification is rerun on the final build. This avoids relabeling older captures as new evidence.

## Save and next session

Checkout and cached origin remain `a2a90a3e08540e15f40e0ede0f8af14921f54675`; reviewed published architecture remains `0de4b54dc9d0e711f11962688f0e6fca3aa01c50`. Roadmap/EV-000–003/P01 changes are local and uncommitted. No push, CI, deployment, paid imagery or fresh production check. Both private screenshots remain unchanged and untracked.

Next proposed session is **P02**, five east-side faces at mapped 138, 140, 142, 144 and 148 First Avenue. Start only on the next user instruction. Re-estimate the whole-area schedule after P03 as planned; one packet is insufficient to replace the provisional 390–725 sessions / 300–1,100 hours.
