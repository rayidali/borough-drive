# Seventh, slowly. — driving and full-street refinement 02

**September 23 resume note:** this is a historical report. [Revision 07](SEVENTH-ENGINE-07.md) is now published and user-endorsed; the [current handoff](../CODEX-HANDOFF.md) governs the next session. Older routes, local-only status, source access and pause instructions below describe their original date. No task is queued at session close.

September 14, 2026. The user accepted the first Godot slice's direction and requested better controls, drifting and engine sound, followed by a highly detailed Seventh Street pass. This revision covers **the original map's entire Seventh Street, Second Avenue through Avenue A with its boundary context**. The First–Second–Seventh–St Marks return circuit remains. The optional extent question received no answer; this full-street assumption was stated before proceeding.

Play at **http://127.0.0.1:5173/seventh/** after `npm run dev`. This is an included Godot 4.7.2 / WebGL 2 export running on the player's device. It needs no GPU server or backend. The original ten-block game at `/`, its accepted corner/core geometry and its photographic records remain intact. The new slice is local and unpublished; see the [checkpoint](../CODEX-HANDOFF.md) for exact source/save/push state.

## Driving and sound

The previous car immediately aligned movement with its heading. The new controller carries planar momentum: steering changes the car's heading while lateral tire grip catches its velocity. Handbraking reduces lateral grip, allowing a sustained slide; releasing and countersteering catches it. Steering reduces at speed, rain reduces grip, and bounded slip assistance makes recovery practical in the narrow streets. Braking, reversing, wall collision, pause and reset clear or constrain momentum consistently.

Use **W/S** to accelerate or brake/reverse, **A/D** to steer and **Space** for the handbrake. Build some speed, turn while briefly holding Space, then release and countersteer. **C** changes camera, **T** changes weather, **R** resets, and **M** enables sound. Sound remains off until enabled, with the preference saved.

The car now has four automatic gears and engine RPM/load response. Original synthesized idle, acceleration, overrun, road, tire and impact layers replace the single speed-pitched tone. Pitch follows RPM, volume follows load, gear changes dip torque/sound, and tires respond to lateral scrub and wetness. Tire marks use a fixed 384-slot pool with a 20-second fade. No marks or audio nodes accumulate indefinitely. The music and rain bed remain original synthesis.

The [handling tests](engine-review-2026-09-14-02/handling.json) exercise dry/wet sliding, symmetric steering, catching the slide, braking/reverse, RPM/gears, reset and equal integration at 30/60/120 Hz. The deterministic maneuver produced 36.20° dry and 38.68° wet slip, compared with 9.18° on ordinary steering; recovery approached zero. [PCM checks](engine-review-2026-09-14-02/audio-levels.json) establish nonempty, unclipped source audio. They do not establish subjective sound quality; the new mix still needs the user's listening review.

## Street coverage and appearance

The slice grows from 154 to **182 building objects**, including **all 82 mapped Seventh-facing objects**. Shared brick, pale masonry, stone and painted-surface treatments apply continuously, with mapped openings, cornices, fire escapes, doors, railings and the inherited corner details retained. The [coverage record](seventh-street-coverage-02.json) lists every Seventh frontage, its evidence, modeled features, capture and unresolved shop state. It does not replace the original ten-block coverage ledger or mark that ledger complete.

This session inspected 67 architectural archive images and 39 additional reference images. Individual elevation schedules retain observed window/arch patterns and add supported areaway rails, masonry bands, intercoms and distinctive ornament. The asymmetrical 50 East 7th profile now has its left arch, paired right windows, setback balustrade and small roof tower. Its relief shapes and dimensions remain interpreted. The 95/97 East 7th schedules retain their four-bay arrangement and rounded window rows. Five First & Seventh corner objects keep their established detail recipes and provenance.

Fifteen shops received new individual layouts and details:

| Frontage | Features modeled from inspected references |
| --- | --- |
| Kinka, 63 East 7th | Blue fascia, left door/right display, plants, rail and board |
| East Village Hats, 80 East 7th | Black frontage, brass-colored lettering/door border, hat forms and projecting Hatworks sign |
| Setsugekka, 74 East 7th | Dark surround, pale lattice, small sign and board |
| Agavi, 72 East 7th | Broad turquoise/white awning stripes, square blade and menu |
| Tokio 7, 83 East 7th | Turquoise fascia, deep cream recess, paired doors, turf, backed bench and globe |
| Abraço, 81 East 7th | Recessed basement entrance, rail and black/pink projecting sign |
| Studio DuArte, 84 East 7th | Pale signage, silver grille, clothes rail and display |
| AuH2O / Goldwater, 84 East 7th | Circular yellow window logo and clothing display |
| Van Leeuwen, 48½ East 7th | Pale gridded frontage, gold-colored script, right door, benches and plants |
| Ho Foods, 110 East 7th | Dark frontage, compact lettering, menu and entry arrangement |
| Pylos, 128 East 7th | Dark/pale frontage grid, menu, name and terracotta display silhouettes |
| Trash and Vaudeville, 96 East 7th | Two display windows, central entrance, pink reveals and red lettering |
| Ladybird, 111 East 7th | Green/purple arched doors, circular panels, plaque and projecting sign |
| 787 Coffee, 131 East 7th | Pale/orange signage, storefront framing and board |
| Titi, Seventh frontage of 109 Avenue A / 130 East 7th | Dark frontage, yellow projecting sign and menu |

The [source record](seventh-street-reference-02.json) retains original URLs, publication/capture uncertainty and inspection exclusions. In particular, the former Abraço address, interior-only Big Bar image, illustrated 787 image, temporary repair barriers, seasonal props and pandemic dining sheds were not treated as current facade evidence. Archive upload dates are not photographic capture dates. A supported business name is not a fully observed facade.

The street has branching trunks and individually shaped leaves with veins and wind, tree-pit rims, capped/chained hydrants, blue mailboxes, drain grilles and utility lids. Twelve evening lamps have small, distance-faded light volumes; sidewalks have shared concrete and restrained seams. Prop positions and vegetation are authored, not a surveyed street-furniture inventory. No new reference-photo pixels are shipped. Six existing Poly Haven CC0 diffuse/normal images supply generic surface detail, with the [credits](../dist/seventh/credits.txt) preserved.

## Visual review and remaining fidelity

All 82 final engine elevations were inspected in [14 numbered contact sheets](../docs/images/seventh-engine-02/elevations/). These are orthographic street-side checks that expose the modeled architecture; they are **not matched photographic camera views**. Separate actual-browser perspective captures inspect the 15 new shop layouts and the driving presentation. The [capture manifest](engine-review-2026-09-14-02/visual-captures.json) records all saved images and hashes. The coverage record links the respective evidence.

Visual review caught and corrected overly strong surface detail, storefront backing hiding recessed openings, stone bands crossing 50 East 7th's ground-floor openings, obstructed review cameras and an exporter dropping the surface-class color channel. Close review also corrected the striped awning winding and narrowed Ladybird’s entrance beside its white wall/window, with visible door-panel relief. [Binary export checks](engine-review-2026-09-14-02/source-validation.json) verified 358 opaque/emissive primitives across all 182 GLBs. Final surface exports preserve RGBA tags, and textures use mipmaps to limit distant shimmer. These corrections are included in the tested package.

**This is a continuous street refinement, not completion of the user's every-inch fidelity standard.** Some shops still use inherited/estimated designs, including those without usable exterior evidence in the inspected sources. Exact logos and type outlines, murals, measured dimensions, carved reliefs, complete interiors, occluded surfaces and the present position of movable objects remain unresolved. Generic materials and authored trees/props are stylistic interpretations. All 82 records retain their acceptance gaps; none is silently promoted to a measured or user-accepted 1:1 facade. The next fidelity work remains on these Seventh Street gaps unless the user chooses another scope.

## Browser performance and robustness

Final measurements and actual-browser evidence are recorded in [browser-final.json](engine-review-2026-09-14-02/browser-final.json). Conditions: Apple M1 MacBook Air, 8 GB RAM, Brave/Chromium, 1440×1000 CSS pixels, DPR 1, local HTTP. HTTP cache was disabled during the run; browser/driver compilation caches had been warmed by earlier tests. Short samples are not universal performance or network-loading guarantees.

| Weather | Northbound (5 s) | Seventh east (8 s) | Seventh west (8 s) |
| --- | ---: | ---: | ---: |
| Golden | 74.8 FPS | 74.2 FPS | 72.0 FPS |
| Dusk | 75.0 FPS | 74.7 FPS | 73.3 FPS |
| Rain | 75.0 FPS | 75.1 FPS | 73.0 FPS |

All nine samples retained full render scale (1.0), with zero wall contacts. The reported 95th-percentile browser frame interval was 14.3–14.4 ms; occasional longer intervals remain possible. These are the final package measurements, separate from the earlier diagnostic prewarming run.

Local playable startup was **4.95 seconds** with warmed browser/driver compilation caches. Healthy runtime recorded **zero errors, warnings or failed requests**. The actual key-driven drift reached **18.10° slip**, then recovered to **−2.59°** with a 320 ms countersteer and no wall contact.

The export uses one shared material family, existing mesh LOD, shared mipmapped surface maps, bounded instances/marks/lights and an adaptive render scale. Four hidden street views upload assets before controls become available, avoiding the first turn's observed upload hitch. Removing redundant mesh UV/tangent data reduced the detailed scene's PCK from 113.86 MiB to **83.21 MiB**, about 27%. Its required player package is **121.29 MiB uncompressed**, versus about 102 MiB for the earlier, smaller 154-building slice. Estimated Brotli PCK + WASM is about 82.52 MiB; actual transfer depends on hosting compression. First download weight remains substantial.

The [native driving review](engine-review-2026-09-14-02/native-driving.json) completed the nine-waypoint return circuit in **66.609 seconds with zero wall contacts** and traversed **545 m of Seventh in 24.904 seconds with zero contacts**. Separate frontage-collision/reverse/reset checks passed. These route checks preceded final surface-tag/startup-upload corrections; vehicle and collision geometry did not subsequently change. Native rendering samples are not the final browser performance evidence.

Actual-browser checks cover all 12 camera/weather combinations, driving/steering/brake/reverse, handbrake slip and countersteer recovery, reset/pause, saved settings, a real tab switch, Retina pixel cap and an actual postcard PNG. Four injected pack-download failures and forced WebGL context loss each exercise a visible Retry and successful return to play. Expected fault-injection errors are recorded separately from healthy runtime.

No public-network startup, mobile controls/device matrix, multiplayer, traffic or 500-user load test was performed. Static delivery avoids server rendering per player; it does not establish hosting bandwidth capacity or shared-world scalability.

## Reproduce and continue

Runtime/source: [engine project](../engine/first-seventh/README.md), [handling model](../engine/first-seventh/scripts/handling.gd), [audio recipe](make_seventh_audio.py), [exporter](export_seventh_engine.py), [Seventh detail kit](seventh_street_kit.py) and `storefront-details.json.seventhEngine`. The engine-only namespace preserves the original storefront data. Rebuild recipes, input/model hashes and all 182 identities are recorded in [slice.json](../engine/first-seventh/assets/slice.json); shipped bytes and 68 source hashes are in [build.json](../dist/seventh/build.json).

`npm run seventh:build` regenerates the browser package after source changes. `npm run seventh:verify` validates the package/source hashes, all 82 Seventh frontages, original geography and preserved corner identities. `npm run verify` checks the original game. Both passed for this revision. The existing Node 22/24 CI workflow now includes the Seventh package check; that remote workflow has not run for these unpublished changes. Native/actual-browser commands and prerequisites are in the engine README. GLBs, import caches and local tools are regenerable; the included `dist/seventh/` package is required tracked source material.

See [preservation evidence](engine-review-2026-09-14-02/preservation.json) for the unchanged original runtime/assets/geography and original storefront namespaces. Save state belongs in the handoff/log. Review the local driving feel, sound and street appearance with the user; do not infer permission to publish, expand to other streets or start autonomous/paid imagery jobs.
