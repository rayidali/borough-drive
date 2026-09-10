# Browser presentation and performance — pass 09

September 10, 2026. The user chose smooth browser exploration, deferred Unreal, and requested further First & 7th improvement followed by a cheaper block workflow. This pass retains all model assets from [corner pass 08](FIRST-SEVENTH-PASS-08.md). The [handoff](../CODEX-HANDOFF.md) records exact local commit and publication state. It is not a PS5-quality or universal 60 FPS claim.

## Implemented changes

- **Contact shading without another city draw.** [DepthAmbientPass](../dist/reconstruction/depth-ambient-pass.js) reuses the main scene depth, estimates geometric normals with edge-aware derivatives, and uses the vendored Three.js SSAO kernel/blur. It runs 16 samples at half CSS resolution. This reduces geometry submissions while retaining contact shading; the shading approximation differs from a separate normal render and needs visual review at thin edges/glass.
- **Automatic graphics for smooth motion.** [The frame budget](../dist/reconstruction/render-budget.js) observes sustained slow frames in 30-frame windows, reduces pixel ratio from 1 toward 0.70, and can disable ambient shading at the floor. Two MSAA samples remain. After a stopped view settles, it restores ratio 1 and ambient shading once, then stops redrawing. Geometry and textures are retained. Detailed still uses up to DPR 1.5/four samples; Faster uses ratio 1/two samples without ambient shading. Saved preferences are honored; Automatic is the default for new visitors.
- **Corner atmosphere and road surface.** [The presentation module](../dist/reconstruction/corner-atmosphere.js) adds static procedural clouds and subtle asphalt/paint variation bounded to First & 7th. Existing licensed surface maps remain. These are authored weather/surface effects, not newly observed weather or measured road repairs. Static clouds preserve idle rendering savings.
- **Smoother driving presentation.** [Vehicle-view interpolation](../dist/reconstruction/vehicle-view.js) blends completed 120 Hz physics poses, including shortest-path heading wrap. It resets on travel/mode changes and never feeds camera motion back into collisions or tire forces. Acceleration, braking, reverse, bounds and the physical vehicle model are unchanged.

All 72 checked reconstruction models/images/JSON manifests and preserved physics/collision/spatial/glass/shared-texture files are byte-identical to `219d4e9ccec8e019351d3a27d7dff6dcaf07237d`. [Preservation evidence](browser-review-09/preservation.json). No Blender rebuild, new architectural inference or imagery request was required. The model total remains 9,435,099 triangles / 52.40 MiB; no facade details were deleted.

## Measurements

[Before](browser-review-09/before.json) and [after](browser-review-09/after.json): Chrome 152 / Apple M1, 1440×1000, DPR 1, local unthrottled HTTP, browser cache disabled. GPU caches/thermal state were not reset. Fixed-frame driving samples cover different distances/durations, so comparisons are indicative. Automatic measurements are additional warm tests after traveling around the map and must not be presented as a cold-drive comparison.

| Sample | Before | Final |
| --- | ---: | ---: |
| Saifee Detailed active rendering | 48.9 FPS | 52.4 FPS |
| Saifee Faster active rendering | 60.0 FPS | 60.0 FPS |
| Northbound Detailed drive sample | 27.1 FPS | 32.9 FPS |
| First & 10th SE Detailed | 29.3 FPS | 33.9 FPS |
| Saifee submitted triangles per Detailed frame | 3,829,758 | 1,915,469 |
| Saifee draw calls per Detailed frame | 596 | 301 |
| Idle scene redraws | 0 | 0 |
| Local initial ready time | 671 ms | 525 ms |
| Initial reconstruction transfer | 40,747,610 bytes | 40,756,645 bytes |

Automatic's warm Saifee view rendered at **60.0 FPS**, ratio 1, with ambient shading enabled. The additional warm northbound drive averaged **48.0 FPS**, with the final 120 rendered frames averaging **55.9 FPS**; it reached ratio 0.70 with ambient shading disabled. Its overall 95th-percentile frame interval remained about 33.4 ms. Stopped inspection restored ratio 1 and ambient shading, including after the reduced-resolution drive; idle redraws returned to zero. High-DPI resize stayed at ratio 1 in Automatic.

Those driving results improve the experience but do **not** establish slowroads.io-equivalent smoothness throughout this dense map. More geometry/streaming and GPU work remains before sustained 60 FPS on this M1 can be claimed. No performance comparison with the slowroads.io site itself was performed.

## Verification and review

`npm run verify` checks 30 imported modules, the unchanged 2,308 road samples, navigation/collision/source/export invariants, exact street materials, spatial triangle preservation and the new presentation tests. The new tests cover stable/sustained frame budgets, one-shot idle recovery, shortest-path yaw, travel reset and isolation from physics.

[The final browser review](browser-review-09/review.json) captures 26 views and exercises controls, resets, loading, forced deferred-core retry, startup fallback/retry, saved quality, idle wake and the fresh Automatic default. [Selected unedited game captures](../docs/images/browser-09/) include the four corners and final driving view. The static checks do not certify visual accuracy; current artwork, dimensions and occlusion limits from pass 08 remain.

Visual inspection covered the [northeast elevation](../docs/images/browser-09/seventh-ne.png), [southeast corner](../docs/images/browser-09/seventh-se.png), [Tile Bar](../docs/images/browser-09/tile-bar.png), [Saifee](../docs/images/browser-09/saifee.png), [Burger glazing](../docs/images/browser-09/7th-street-burger.png) and [Automatic driving](../docs/images/browser-09/automatic-drive.png). Existing facade elements remained visible; lower-resolution motion is visibly softer. This pass's visual review checks presentation regressions against the existing game, not a fresh photographic accuracy comparison.

The separate [block workflow](BLOCK-WORKFLOW.md) prepares finite offline tasks and budget estimates. Its tests validate unique ownership, source permissions, stale input rejection, patch scope and escalation. No paid AI worker, Google batch, citywide job or deployment has started.

```sh
npm run dev
npm run verify
npm run workflow:verify
node scripts/profile-performance.mjs renders/browser-profile --automatic
node scripts/review-first-seventh.mjs renders/browser-review --fresh-default
```

The last two commands require an isolated Chrome with local debugging on port 9222. They inject review instrumentation only into their own tab. Select **Graphics → Automatic** in the game if an earlier saved Detailed preference is still active.
