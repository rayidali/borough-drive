# Runtime performance pass 07 — September 9, 2026

The owner accepted First & 7th [revision 06](FIRST-SEVENTH-PASS-06.md) as the **minimum completion standard** and requested speed optimization, publication to `main`, and updated documentation. This pass preserves every existing model export and photographic asset. Wider East Village work, economical block/street batches, Manhattan and NYC expansion remain deferred to the next planning discussion. No service, paid imagery access or background job was configured.

Published gameplay/source commit: `522cd1de77b72186dc98e06a3b9f6ce4db761d8b`, live at [borough-drive.vercel.app](https://borough-drive.vercel.app). [Publication evidence](publication-review-2026-09-09.json) verifies every changed served file. The exact starting gameplay/source commit was `0f40856c9c576d1648ddae9c6e76bb550a98b42a`. [CODEX-HANDOFF.md](../CODEX-HANDOFF.md) records the final source commit, push and verified live deployment separately.

## Changes

- Startup loads the original street materials in a reproducible 4.18 MiB subset and prioritizes nearby sections. The unchanged 24.39 MiB First & 10th model loads on approach; mapped silhouettes occupy its distant position beforehand. A failed core request retries after 12 seconds without stopping exploration.
- Content-addressed neighborhood surface images share their download/decode promises across GLBs. This cache excludes model buffers and embedded reference photographs. Per-parser texture settings remain separate; equivalent material textures still share GPU resources.
- Large opaque batches are partitioned into 64 m cells, retaining all triangles, vertex attributes, normals, UVs and transforms. Frustum and shadow culling can skip more out-of-view geometry. Smaller and transparent meshes keep their original batching.
- Clear storefront panes retain physical surface lighting, Fresnel reflection, the corner reflection capture, and visible interiors through alpha compositing. This thin-pane approximation removes the extra city render previously used for 6 mm volumetric refraction. It does not simulate that small refraction offset or transmission blur; close-up interiors remain sharp. It is used in both graphics modes.
- A settled view stops issuing scene renders. Movement, dragging, resize, quality changes, returning to the tab, and streamed assets resume rendering. Simulation/navigation continue independently. Lights are omitted only when their complete influence sphere is outside the camera frustum; the all-direction reflection capture temporarily restores them.
- Detailed remains the default: existing ambient shading, four-sample offscreen antialiasing, 4096 px shadows, materials, exposure and lighting values are retained. Redundant canvas antialiasing is disabled. The fallback image loads only when displayed. The vendored `HDRLoader` replaces its deprecated alias.

## Measured comparison

Chrome 152, Apple M1 / ANGLE Metal, 1440 × 1000, pixel ratio 1, local HTTP with the HTTP cache disabled. [Before](performance-review-2026-09-09/before.json) and [after](performance-review-2026-09-09/after.json) retain settings, resources, timings, whole-frame draw/triangle counts, poses and runtime hashes.

| Sample | Before | After |
| --- | ---: | ---: |
| Saifee corner, Detailed, continuous redraw | 25.2 fps | 50.2 fps |
| First & 10th southeast, Detailed, continuous redraw | 17.9 fps | 28.6 fps |
| Northbound driving/streaming stress sample, Detailed | 20.7 fps | 28.1 fps |
| Saifee corner, Faster, continuous redraw | 56.5 fps | 60.0 fps |
| Settled Saifee view, actual scene redraws | About 25 per second | 0 |
| Initial reconstruction resource transfer | 89.61 MiB | 38.24 MiB |
| Shared surface image requests during startup | 42 | 9 |
| First scene-render submission | 1.25 seconds | 0.43 seconds |
| Neighborhood settled observation, including fixed review allowance | 5.68 seconds | 3.81 seconds |

The Saifee frame submits 3.74 million triangles across all passes, down from 7.45 million, although exported geometry is unchanged. The measured initial download reduction is approximately **57%**. The subsequent First & 10th download still occurs when that area is visited.

These are short single-device comparisons, not a universal frame-rate guarantee or a live-network benchmark. GPU driver shader caches were not reset between runs. Continuous-view samples add a one-microradian yaw change per RAF so they measure real redraws; idle RAF responsiveness is not reported as rendering performance. Driving holds W for 240 RAF intervals, so elapsed time/distance differ between versions; this is a streaming stress comparison rather than an identical timed route. First submission is not the time pixels reach the screen. Dense views, first shader compilation, larger retina viewports and driving still have headroom for improvement.

## Preservation and review

[Preserved asset hashes](performance-review-2026-09-09/preserved-assets.json) confirm 50 unchanged files, including all original GLBs, surface maps, six licensed photographs, both accepted corner recipes and vehicle code. The entire compiled neighborhood manifest is unchanged except the explicit user-acceptance/scope metadata. All 615 footprints/heights, roads, boundaries, facade schedules and collisions remain intact. Three Blender-written silhouette-height fields reset by the metadata compiler were restored from the exact starting manifest before final profiling. No Blender export was performed.

[The browser review](performance-review-2026-09-09/visual-and-runtime.json) records 26 views: start, four First & 7th corners, eight shops, nine elevations and four First & 10th corners. Two additional travel captures cover Avenue A / East 12th and returning to First & 7th. All 28 local unedited PNGs are in [docs/images/performance-07](../docs/images/performance-07/), outside the served game directory. A separate [live-site smoke check](performance-review-2026-09-09/live-smoke.json) loaded all five starting sections and rendered the [production Saifee view](../docs/images/performance-07/live-first-seventh.png) with zero errors or failed requests.

Direct comparisons: [Saifee corner](../docs/images/performance-07/seventh-se.png), [Tile Bar](../docs/images/performance-07/tile-bar.png), [E7 Deli](../docs/images/performance-07/e7-deli.png), [First & 10th](../docs/images/performance-07/first-tenth-se.png). The existing [revision 06 captures](first-seventh-review-2026-09-08.json) remain the accepted visual reference.

`npm run verify` passed: 26 local modules, asset integrity, 2,308 road samples, vehicle/collision/map invariants, storefront/model source signatures and corner schedules. New checks confirm exact reproduction of the street-material subset and preserve triangles, winding, transforms, normals, UVs, bounds and transparency through spatial partitioning. Clean preparation/compilation reproduced the source fields and all three generated audits.

Normal profiling produced zero uncaught exceptions, console errors, warnings or HTTP failures. The separate review checked northbound driving, both resets, four corner controls, quality persistence, idle rendering, drag/resize wake-up, and travel/unloading/return. One intentionally failed core download retried successfully; one intentionally failed startup-material request displayed the fallback photograph, and Retry restored the game. Expected warning/error messages for those injected failures are identified in the report; there were no unexpected errors.

## Reproduce

```sh
npm run dev
# In a separate isolated Chrome instance, enable --remote-debugging-port=9222
# and use a temporary --user-data-dir; do not reuse a personal browser profile.
node scripts/profile-performance.mjs renders/performance
node scripts/review-first-seventh.mjs renders/corner-review
npm run verify
python3 scripts/verify-neighborhood-reproduction.py
```

After an intentional core GLB change, regenerate its exact material subset with `node scripts/prepare-street-materials.mjs`. Existing assets are included, so normal startup requires neither Python nor Blender. Browser review injects its instrumentation only into its isolated tab. Saved review reports/captures are durable; old processes and temporary folders are unnecessary to resume.

## Imagery access for the later discussion

For visual feedback, the owner can attach a Street View screenshot with its location, direction and displayed capture date. A shared image does not itself grant a license for building a reusable derived asset collection. Original photos or imagery explicitly licensed for reconstruction are the clearest basis for a repeatable modeling process.

Google's official [Street View Static API setup](https://developers.google.com/maps/documentation/streetview/get-api-key) provides the technical access route through a Cloud project, billing and an appropriately restricted key, kept locally. However, [Google Maps Platform terms, section 3.2.3](https://cloud.google.com/maps-platform/terms) restrict scraping, bulk Street View downloads and creating content from Maps content. The [Street View policies](https://developers.google.com/maps/documentation/streetview/policies) also restrict caching and require attribution. API access alone therefore does not resolve whether the proposed reconstruction use is permitted; establish suitable permission/licensing before adopting it as a production source.

[Firecrawl's browser interaction tools](https://docs.firecrawl.dev/features/interact) support actions and screenshots, but their documentation does not establish that a Google panorama will be accessible in this environment or grant rights to its imagery. Do not purchase/configure it specifically for Street View on an untested assumption. No Google/Firecrawl credentials were requested, stored in the repository or configured in this pass. These access notes were checked September 9, 2026; no new architectural-photo capture dates or business observations are asserted.
