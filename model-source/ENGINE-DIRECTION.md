# Rendering and driving direction — September 10, 2026

**Superseded as the active direction:** later on September 10 the user chose smooth browser-first play and deferred Unreal. Follow [browser pass 09](BROWSER-PASS-09.md) and [the bounded block workflow](BLOCK-WORKFLOW.md). The assessment below remains historical; it is not permission to migrate.


The user asked whether the sky, roads and driving can reach a PS5-game standard in the current browser project, or whether Unreal should handle the final experience while the current pipeline supplies models. This is an assessment and recommendation, **not an accepted migration decision or an implemented graphics pass**. The playable source remains `219d4e9ccec8e019351d3a27d7dff6dcaf07237d`, locally reviewed First & 7th pass 08.

## Recommendation

Use Blender and the reproducible neighborhood data/recipes to author the city, retain Three.js for convenient browser inspection, and test Unreal Engine as the final game runtime. Start with First & 7th and one driveable street segment before extending the map. A small Unreal comparison will establish whether the materials, lighting, asset structure, hardware and handling meet the user's target. Importing the same models alone will not produce a AAA result.

The browser can still gain better clouds, road variation, steering, camera response and sound. Major investment in rebuilding a complete vehicle and high-end lighting stack here would duplicate work if Unreal is the intended destination. That tradeoff is a project recommendation, not a claim that browsers cannot produce attractive games.

## What the current source actually does

| Area | Existing implementation | Work toward the requested result |
| --- | --- | --- |
| Sky and light | Three.js analytic Sky, one sun/shadow map, hemisphere fill, HDR environment, linear fog, screen-space AO and AgX tone mapping in [viewer.js](../dist/reconstruction/viewer.js). No authored cloud layer or dynamic bounced-light system. | Coherent atmosphere/clouds, sky light and reflections; tune exposure, shadow detail and indirect light against the actual facades. |
| Roads | Flat runtime geometry, repeated metre-scale asphalt/pavement maps, raised paint boxes and estimated widths in [neighborhood-render.js](../dist/reconstruction/neighborhood-render.js). | Authored asphalt materials with appropriate aggregate scale, repairs, paint wear and curb/gutter transitions; source-supported layout and surface geometry. Potholes and repairs must not be described as observed without evidence. |
| Driving | A 120 Hz planar tire-force model with yaw inertia, speed-dependent steering, braking and reverse; visual pitch/roll and a simple hood. No per-wheel ground contact, suspension travel or drivetrain torque/gear simulation. [vehicle.js](../dist/reconstruction/vehicle.js). | A complete vehicle asset, wheel/suspension/contact physics, drivetrain tuning, controller input, camera response and sound. Good handling requires iterative driving tests in addition to the physics system. |

Epic provides integrated [atmosphere, cloud and fog components](https://dev.epicgames.com/documentation/en-us/unreal-engine/environmental-light-with-fog-clouds-sky-and-atmosphere-in-unreal-engine), [Lumen indirect lighting and reflections](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine), and [Chaos vehicle setup](https://dev.epicgames.com/documentation/en-us/unreal-engine/how-to-set-up-vehicles-in-unreal-engine). These provide a more suitable foundation for the requested final experience; quality and frame rate still depend on authored assets, configuration, hardware and testing.

## Preserve the work; prepare a separate export

The editable recipes and source records are the durable city asset. The browser GLBs are one optimized delivery format. [build_neighborhood.py](build_neighborhood.py) merges building geometry by material across each tile and externalizes shared textures. The three inspected corner files require Draco compression and include a vertex-color paint material; their material-batch counts are not building identities.

For an Unreal test, add a separate export path from the same recipes that preserves building/prop identities, transforms and reusable components. Include a verified scale/axis conversion, collision meshes and complete texture dependencies. Test paint vertex colors, normals, glass and material channels explicitly. Keep the existing browser export available. Do not assume the compressed files or custom browser shaders transfer unchanged. Unreal supports [glTF/GLB import](https://dev.epicgames.com/documentation/en-us/unreal-engine/gltf-file-format-support-in-unreal-engine), but import has not been tested on this project. The roads, sky, UI and vehicle simulation are JavaScript runtime systems, so they need a separate Unreal implementation or export.

Modular exports also matter for lighting: Epic documents limitations with large combined meshes and complex interiors in [Lumen's surface cache and distance fields](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-technical-details-in-unreal-engine). Model organization should be tested in Unreal before scaling the production process.

## Proposed first test

1. Export the five First & 7th buildings and associated props separately, with source IDs and textures. Verify mapped scale, alignment and material appearance in Unreal.
2. Build one road segment with coherent asphalt, markings, sidewalks and collision. Establish sky, sun, indirect light and reflections using repeatable reference views.
3. Add one correctly set up Chaos vehicle and tune acceleration, braking, steering, suspension, camera and audio. Test a straight run, intersection turn, stop, reverse and curb contact.
4. Compare the same corner on the intended hardware, measuring frame time and memory as well as appearance. Agree on the quality standard before expanding.

No Unreal project, importer, runtime change or deployment was created during this assessment. Steps above are proposed future work.

## Hardware and delivery tradeoffs

The prior local browser benchmark used an Apple M1. Epic's current [macOS feature requirements](https://dev.epicgames.com/documentation/unreal-engine/macos-development-requirements-for-unreal-engine?lang=en-US) list software Lumen for M1+, Nanite/Virtual Shadow Maps for M2+ with beta support, and no hardware-ray-traced Lumen support on macOS. The current computer therefore should not be assumed to demonstrate the complete intended high-end rendering configuration. No Unreal installation or hardware benchmark was performed.

The current static browser deployment is inexpensive to distribute and runs locally on each player's machine. An Unreal native build has a different distribution path. Epic's [Pixel Streaming](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-pixel-streaming-in-unreal-engine) can put an Unreal experience in a browser by running and rendering it on another computer; this introduces running GPU capacity, network and latency considerations. It is not a drop-in replacement for serving this repository's static `dist/` directory from Vercel. No hosting service or paid capacity has been provisioned.
