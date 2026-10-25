# P03 — 145 First Avenue / southwest Ninth corner

Completed locally October 13, 2026, under the user’s “continue onto the next.” One building, two exact faces (`241822237:1`, `241822237:0`), two businesses across three shopfronts. The previous 212 authored and compiled models remain byte-identical. This is a reviewed local candidate, not user acceptance or calibrated photographic 1:1.

## Observed and implemented

The [dated observations](east-village-p03/observations.json) contain eight ordinary-browser Street View inspections and the pizza business’s official address check. Primary storefront evidence is May/September 2024, with April 2026 context and older unobstructed Ninth views for architecture/access. These dates do not establish unchanged October 2026 occupancy. Reference pixels remain outside the repository and are not game textures.

- **Architecture:** mapped irregular five-point footprint and 15.19 m source height; red brick with restrained variation, wrapping green cornice, curved lower window pediments, rectangular higher heads and separate stone sills. First has 16 upper openings; Ninth has 10, including two smaller low west windows and broad blank masonry. Only Ninth has the small escape landing/drop. The 143 join touches with a slight plane difference; it is not an alley.
- **Baji Baji:** dark wood fascia, boxed salmon two-line name, separate 145/phone positions, yellow circular window graphic, recessed right entrance and layered door/frame stickers. Its source has no awning or outdoor seating.
- **East Village Pizza, First:** independently constructed green fascia and projected shade, white lettering, gooseneck lamps, green neon, glazed display case with horizontal trays, grade/door decals, riser graffiti and a layered painted corner pier. The corner entrance remains open visually through a shared shallow room shell.
- **East Village Pizza, Ninth:** three unequal glazed bays, separate green shade/fascia, website/phone, round neon, heart/pizza art and slice neon, skyline-painted base, wooden standing tables and backless stools. The western service wall has a vent, arcing lettering and eight distinct slice motifs. The separate residential entry has its transom, shallow step, intercom and **352 on the right jamb**.
- **Street:** tree-pit bench, inverted-U rack, drain, tactile pads and corner pole/sign/pedestrian signal. Fixtures and the entry path are checked in served obliques.

West-side neighbor `241822239` is deferred. Its photographed recessed pale wall is recorded; P03 stops at the mapped parcel boundary rather than inventing an alley or authoring that neighbor. The 148 First Avenue Ninth return remains outside scope. Fine mural/sticker art, exact fonts, dimensions and shallow interior display cues are approximations; hidden interiors, rear and roof detail remain unknown.

## Runtime and reproducible source

[Author](author_p03.py), [detail kit](p03_kit.py), [schedule](east-village-p03/schedule.json), [runtime props](../engine/first-seventh/scripts/p03_detail.gd) and [review harness](../scripts/review-p03.mjs) are independent of earlier packet recipes. Shared exporter changes required one complete export, with preservation verified; two later model exports rebuilt only `241822237`. Four engine builds and their repairs are retained in [progress](east-village-p03/progress.json) and [logs](east-village-p03/logs/).

The bounded road adapter reaches First Avenue’s visible terminal at **z=−166** (outer cap −171), and opens only the short west Ninth approach centered at **z=−154.7**, visible west terminal **x=−40** (outer cap −44, north cap −164). East Ninth remains closed at its existing curb, **x=10.75**, with a backup barrier at x=13. Second Avenue and Avenue A remain at −119. The minimap reflects this short extension; the Seventh address HUD remains hidden on First/Ninth. Vehicle handling, UI presentation and audio are preserved.

Final build: **2026-10-14T01:13:30.064Z** (October 13 EDT). Shared PCK **8,014,524 bytes**, SHA256 **`509239e48e6fb2928e308a31f11d801821c83298331ce3c51e4809011617cb4c`**. **232 runtime files / 133 source hashes / 213 buildings**; 12 releasable west scenes and 201 pinned, all initially loaded. Required runtime files total **152,561,556 bytes**. New model: **133,137 triangles / 8,635,860-byte GLB / 2,988,511-byte compiled scene**. Keep every required `dist/seventh/areas/` file with the pack. [Exact metrics](east-village-p03/metrics.json).

## Actual review and checks

All **35 unique final detail images** and **18 gameplay images** were opened and inspected. Full elevations, overlapping ground views, front/oblique shop details, both massing directions, entry/mural/corner details, five protected views and golden/dusk/rain coverage are enumerated in [visual review](east-village-p03/visual-review.json). The extra Ninth “shop-complete” diagnostic is cropped; the complete ground coverage comes from the overlapping views. There was no independent second reviewer or calibrated photo registration.

Repairs addressed awning text buried in its shade, the corner shell blocking the First doorway, lower sills colliding with fascias, upright display motifs, buried 352 lettering, mural lettering/vent overlap, entry-rail clearance and sign direction. Earlier trial captures/builds remain separate from the final package.

- Six real-key driving legs pass with **zero contacts and zero loading holds**. Sampled p95 frame intervals range **17.5–18.7 ms**, maximum **18.8 ms**.
- Seven held-throttle boundary cases pass, including the still-closed east Ninth curb and unchanged avenue terminals. Four camera modes retain the stationary car/mode during orbit and zoom; reset returns to Seventh. The new building has one visual/collision owner. [Route record](east-village-p03/routes-final/captures.json).
- All **17 existing address cases** pass. Required `npm run seventh:verify` and `npm run verify` pass. [Validation](east-village-p03/validation.json).
- Local root, Seventh, legacy and pack responses match saved hashes; all **232** runtime files respond with expected sizes. [HTTP evidence](east-village-p03/http-validation.json).
- All **212 previous GLBs and compiled scenes**, **2,375 other tracked non-Markdown files**, prior packet/runtime source hashes and both unchanged/untracked private screenshots match the P03-start snapshot. The nine changed tracked non-Markdown paths are explicitly listed in [preservation](east-village-p03/preservation.json); newly authored/untracked files are recorded by the build and Git status.

Two failed route trials were fixture errors: braking too late hit the real north terminal; expecting the backup east barrier missed that the existing curb stopped the car first. Corrected fixtures preserve vehicle handling and runtime boundaries. Failed attempts remain in `routes-01/`, `routes-02/` and logs.

## Startup cost and timing

Five cold and five cache-enabled startups were run both before and after P03 with the same harness/profile. Before and after were sequential, not interleaved; device temperature and other background conditions were not controlled. With five samples, the reported p95 is the maximum.

| Ready time | P02 baseline this session | Final P03 |
| --- | ---: | ---: |
| Cold median / p95 | 6.950 / 7.385 s | 8.048 / 8.984 s |
| Warm median / p95 | 7.395 / 7.849 s | 8.951 / 10.251 s |

Both after medians are slower. The new scene adds about 2.99 MB to cold content; these runs do not isolate the cause of the timing change. Cold encoded transfer rises from 149,356,755 to 152,353,251 bytes; warm from 48,248,057 to 48,255,789 bytes. Historical P02’s 21.687-second warm outlier remains unexplained, not erased by these later runs. Full-area startup/resource scalability remains unproven.

P01 took approximately 78 minutes and P02 74.1 minutes; P03 took approximately **83.6 minutes elapsed**, as saved in [progress](east-village-p03/progress.json). It includes research, fresh startup baselines, three model exports, four builds, visual repairs, tests and planning/documentation. Stage activities overlap and were not independently instrumented; user wait was zero and no subagents were used.

The [roadmap](EAST-VILLAGE-SESSION-PLAN.md) now targets **3–5 faces** per ordinary session, with a complex corner handled separately. Pending street allowances increase explicitly; the provisional total is **630–1,340 sessions / roughly 630–2,250+ model/tool hours**. This is an assumption-based capacity adjustment, not an extrapolation of a stable measured business rate. Recalibrate after eight detail sessions. The old forecast is preserved in [planning baseline](east-village-p03/planning-baseline.json).

## Save state and next session

Everything remains **local/uncommitted** on `main`; checkout/cached `origin/main` remain **`a2a90a3e08540e15f40e0ede0f8af14921f54675`**. Published architecture is `0de4b54dc9d0e711f11962688f0e6fca3aa01c50`; production remains the previously verified revision 09 release `3457a29`. No fetch, commit, push, CI, deployment, paid imagery or fresh production check occurred.

Preview: **http://127.0.0.1:5181/**. Refresh an older open tab to select the current release; restart with `npm run dev -- 5181` if the local process later stops.

Next, on the next user instruction: **`01-E09-21-N01A`**, the Ninth face of 147 First plus 345, 343 and 341 East Ninth. The previous eight-face N01 group is now a non-executable parent with four-face N01A/N01B children, retaining every assigned face. [Exact next handoff](east-village-p03/next-handoff.json). No next-packet source inspection or implementation has started.
