# Browser loading, rendering and map growth

Current status, publication identity and assigned blocks: [project handoff](../CODEX-HANDOFF.md). This document describes the October 25 scaling work; final measurements belong in its linked validation record.

The target is a detailed browser driving game that can grow beyond the East Village. A larger authored map must not require downloading, instantiating or drawing every building before play. Full Manhattan support remains an engineering target, not a tested capability of the current 397-building catalog.

## Implemented runtime changes

- An index of complete building bounds selects nearby and visible scenes. Long corner returns occupy every intersected cell. The initial neighborhood, normal movement, inspection cameras and teleports use the same ownership records.
- The camera retains its 370 m far plane and all existing inspection controls. Scenes required by a proposed camera view must be ready before that view is shown. Nearby collision owners load together with their visual models; delayed loads can hold movement safely.
- A bounded latency/speed horizon prepares nearby scenes. Requests and staged bytes remain limited. Distant owners retire after a grace period, one per frame; weak-reference diagnostics check resource release. Content-hashed HTTP assets retain their existing integrity checks and immutable cache policy.
- Static street details retain their exact geometry and materials while batching by local world-space cell. Cell size is measured against draw-call overhead; smaller is not automatically faster. Imported building meshes retain their existing LODs.
- The minimap follows the car, uses the actual building footprints and authored road extents, and queries only nearby map cells. A bounded 456 × 312 pixel cached patch shifts beneath the view; geometry redraws only after leaving its safety margin. Its position marker redraws separately, and the map yields space in narrow windows.

The [October 25 report](../model-source/BROWSER-SCALE-2026-10-25.md) and [validation](../model-source/browser-scale-2026-10-25/validation.json) record exact tests and tradeoffs. Final local weather/route averages were 95.25–120.00 fps; several routes remain slower than the preceding all-resident build. Spatial residency removes the requirement to keep the entire growing building catalog loaded, but does not establish whole-Manhattan performance.

Implementation: [spatial index](../engine/first-seventh/scripts/spatial_index.gd), [residency](../engine/first-seventh/scripts/area_streamer.gd), [street batching](../engine/first-seventh/scripts/world.gd), [minimap](../engine/first-seventh/scripts/minimap.gd). [Baseline and candidate evidence](../model-source/browser-scale-2026-10-25/) preserve the exact builds, including unsuccessful trials.

## Gates before publication and further block integration

Preserve every preceding authored/compiled model and the original game. Verify routes, endpoint collisions, camera inspection/reset, resize, address behavior and scene ownership. Exercise delayed, missing and corrupt scene responses and explicit retry. Compare startup transfers and resident resources, not only the size of the shared PCK. Measure frame intervals in golden, dusk and rain conditions without capture/export jobs running at the same time. Inspect the map at desktop and narrow sizes and the actual streets after release/reload.

A catalog count is separate from the number of resident scenes and physical buildings. Capturing an image is separate from inspecting it. A successful local test is separate from an actual CDN response or a low-powered-device result. Keep every result attached to its tested package identity.

## Remaining work for a much larger city

The current index keeps the whole lightweight catalog in memory. Manhattan growth will also require paged geographic metadata, independently resident street/prop chunks, distant skyline representations derived from authored geometry, and explicit resident-memory/transfer budgets tested on slower computers and networks. Full-detail scenes remain unchanged near the player; reducing detail everywhere is not the plan. The protected core texture bundle is still shared, and individual scene decode/activation cannot be interrupted in the present single-threaded web export.

Do not claim a city-wide performance guarantee from this local map. Establish repeatable cold/warm and constrained-network baselines as density and route length increase. Preserve individual storefront evidence and geometry while selecting, batching and retiring work the player cannot currently see.

Godot's [3D performance guidance](https://docs.godotengine.org/en/stable/tutorials/performance/optimizing_3d_performance.html) describes demand-loaded tiles and the tradeoff between draw calls and visibility granularity. Its [occlusion-culling documentation](https://docs.godotengine.org/en/stable/tutorials/3d/occlusion_culling.html) describes a separate technique; this change uses spatial residency and frustum checks and does not claim occlusion culling is enabled in the shipped web template.
