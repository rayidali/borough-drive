# First Avenue and St. Marks — local revision 08

October 11, 2026. The user confirmed **First Avenue from East Seventh to St. Marks, plus both sides of St. Marks from Second Avenue to Avenue A**, including same-parcel corner returns and street details. This full extent is implemented as a local candidate. No publication or paid imagery job was requested. [Current save state](../CODEX-HANDOFF.md) · [Confirmed scope](FIRST-STMARKS-SCOPE-08.md).

## Included work

The inventory contains 98 primary faces and eight supplemental returns. Four belong to protected First & Seventh surfaces, leaving **102 editable faces on 93 buildings**. The build retains every prior building: 72 existing buildings receive this pass, 110 remain byte-identical, and 21 eastern St. Marks buildings are added, for **203 total**. Counts describe modeled coverage, not calibrated photographic acceptance.

- First Avenue: individual shop divisions, observed signs and number supports, entry placement, glazing/displays, window rhythms, molded hoods, fire escapes and dated scaffold/mesh coverage.
- St. Marks: individual residential and commercial elevations on both sides, varied window and cornice treatments, raised entrances, stoops, fenced forecourts, below-grade access, awnings, shop fronts and same-parcel avenue returns.
- Special forms: the split projection and mansard/dormers at 39; Porto Rico's low front and taller setback; the 62 chapel's tall central glazing and cross doors; 87's right-side pediment; Mogador's striped lower facade and basement shops; the tall numbered entry and projected shop fronts at 109; the projected entry on the southern Avenue A corner.
- Streets: the eastern St. Marks/Avenue A connection, bounded barriers and collision limits, crossings and lane markings, observed trees/pit fences, utilities, bins and corner hardware. The low painted shutter/gate edge west of 110 uses authored geometry; its artwork is an abstraction, not copied photographic pixels.

The original ten-block game/core, accepted First & Seventh corner, both Seventh blocks, controls, UI/audio, routing and third-party notices are preserved. The address HUD remains Seventh-only, and the small existing route diagram retains its previous schematic extent. No UI redesign is included.

## Sources and reproducible implementation

[The browser ledger](first-stmarks-browser-08.json) records **55 dated view locators**, with initial observations on 104 of 106 mapped faces; the other two are protected Seventh returns. The two protected First Avenue faces were inspected but not remodeled. Ordinary browser Street View supplied the references. Imagery includes April 2026 and September 2024; inspection on October 11 does not turn older imagery into verified October business occupancy. Adjacent views resolved the 99/99½ shared facade and the previously unmapped painted site edge.

Source screenshots remain temporary local inspection material. They are not committed, textures, or runtime downloads. Source URLs, imagery dates, per-property observations and explicit unknowns are durable in the ledger. The two private user screenshots remain local and untracked.

The exact-face adapter [first_stmarks_kit.py](first_stmarks_kit.py) applies the engine-only `firstStmarksEngine` namespace after the existing Seventh adapter. [author_stmarks_08.py](author_stmarks_08.py) imports [the First Avenue packet](author_first_stmarks_08.py) and regenerates the complete 102-face schedule. Corner faces retain their distinct source index; protected Seventh dispatch and old schedule namespaces are unchanged. Exceptional massing, well closures and projections are bounded to this new adapter.

The exporter records all 203 building hashes, both street schedules and recipe fingerprints. The original 82 Seventh review faces remain separate from the 102 new exact-face review selectors. The inventory and generated schedule contain authoring-time status notes; use this report and the handoff for subsequent export/review state.

To play, run `npm run dev` and open **http://127.0.0.1:5173/**. Drive north from the initial First & Seventh position, then turn onto St. Marks. No rebuild, credentials, external reference images or previous browser session is needed. Reproduction and review commands are in the [engine README](../engine/first-seventh/README.md#rebuild-and-verify).

## Actual visual review

[The visual review record](first-stmarks-review-08/visual-review.json) distinguishes captured files from individually inspected images and preserves the issues found during review.

| Stage | What was actually inspected |
| --- | --- |
| Full draft | All 102 elevation images; one listed ground crop |
| Repaired complete candidate | All 147 overlapping ground images covering every editable face; the separate 109 elevation |
| Latest 14-face repairs | All 21 ground images and all 14 elevations |
| Perspective | Eleven corner/access/site views from the final traversal package, plus wider 39/40½ roof views |
| Player view | Three final mid-street driving-camera views, plus six representative traversal-end views |

The full repaired candidate and latest repair captures have different PCK hashes, recorded in their manifests. Earlier evidence is retained as history, not mislabeled as final-byte evidence. The latest package supersedes the fourteen affected faces; the other 88 face recipes did not change. All full-candidate elevation images were captured, but only the explicitly listed ones are claimed as individually inspected after the draft review.

Repairs included eight intersecting window/door openings; the Lions lateral ramp; lighter white/brown materials; larger source-supported tree crowns; 132 Second Avenue and 66 St. Marks ornament; 39's mass/window separation; 60's raised parlor opening; 62 chapel details; 75 canopy/pane details; 87's off-center pediment; 109's upper row/entry/shop projection; the Avenue A entry projection; La Palapa's tan canopy; Anjelly's blue lettering; and closing the underside of basement wells while retaining descent.

Review manifests and actual game PNGs are retained under [first-stmarks-review-08](first-stmarks-review-08/). They contain no source photographs. The initial 39/40½ perspective crops missed the roofs; the wider replacements in `final-obliques/` were inspected. Source coverage, successful exports and screenshot counts do not establish 1:1 accuracy.

## Validation and package identity

Final PCK: **94,003,244 bytes**, SHA256 **`570ebb253734e69b6eca32002e53b6172ab71ca4f24cf1d8a489fb8ea0d672b8`**. Final model export: **203 buildings / 3,663,275 triangles**. The package manifest records 14 runtime files and 92 source hashes. Its `sourceCommit` remains the old geographic baseline `c76dcce…`; the actual implementation Git commit is recorded separately in the handoff.

- `npm run verify` passes for the original game; [saved output](first-stmarks-review-08/legacy-verify.log).
- `npm run seventh:verify` passes the final package, original geography, all 82 Seventh and 102 new face records; [saved output](first-stmarks-review-08/seventh-verify.log).
- Native handling, Seventh address and camera tests pass; [saved logs](first-stmarks-review-08/native-checks/). These ran before the final facade-only corrections; their gameplay sources are unchanged afterward.
- [Preservation audit](first-stmarks-review-08/preservation.json): all 110 protected/out-of-scope GLBs, every old parsed schedule namespace, the original game/core/UI/audio/credits/routing and both private screenshots match the baseline. The audit checks 1,145 original tracked non-Markdown files, allowing only the twelve explicit task-related changed paths.
- [Opening audit](first-stmarks-review-08/opening-audit.json): 1,847 scheduled window/door rectangles across 102 faces, 22,448 within-face pairs, no horizontal-bound violations or overlapping interiors under the documented tolerances. Shop/ornament completeness and visual accuracy are separate.
- [Final driving checks](first-stmarks-review-08/final-routes-complete/routes.json): **18/18 passes, zero contacts**, through all three weather modes: St. Marks east/west, First north/south, Avenue A north and preserved Seventh east. Real W-key driving traverses each complete segment after setting its start pose. There are zero recorded browser errors or failed HTTP responses. An earlier fixed-duration First-south check stopped short without a collision; the retained `final-routes/` trial is superseded by endpoint-based traversal checks.

The [performance summary](first-stmarks-review-08/performance-summary.json) preserves all runs. Apple M1 / Brave Chromium 155, 1440×1000, local HTTP, same nine sample definitions:

| Run | Mean render FPS | Sample range | Local ready |
| --- | ---: | ---: | ---: |
| Unchanged revision 07 baseline | 58.61 | 51.82–60.01 | 21.303 s |
| Initial final-package pass | 50.33 | 18.56–60.01 | 7.630 s |
| Focused final repeat | 58.97 | 56.79–60.01 | 7.297 s |

The initial final pass contained two long rain-sample pauses; their cause was not proven. The repeat suppressed idle sleep and added visibility/frame-gap diagnostics: every sample remained visible, maximum observed frame gap 182.3 ms, no errors or failed responses. The earlier poor run is not discarded. These short local samples do not prove sustained 60 FPS or performance on other devices, and startup differences are not a measured loading speedup. No runtime performance settings were changed to obtain the repeat.

## Remaining precision and next review

Heights, depths, relief, sidewalk fixture locations and most coordinates within a facade are visual estimates tied to mapped footprints, not new survey measurements. Tree/scaffold occlusions, unreadable number text, concealed surfaces and older business imagery remain explicit in the ledger. Interiors and painted artwork are simplified. The expanded slice is bounded at the confirmed streets; empty surroundings beyond its barriers are context limits, not additional assigned reconstruction.

No calibrated multi-view fit or photographic 1:1 acceptance is claimed. The local pass is ready for the user's visual review; no further street, UI/audio task, paid imagery retry or publication follows automatically. September revision 07's user endorsement and production evidence remain historical and do not endorse this new candidate.
