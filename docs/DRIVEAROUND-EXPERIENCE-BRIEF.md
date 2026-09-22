# DriveAround.nyc — brand and calm-driving experience brief

Prepared September 21, 2026 as a planning-only brief, then partially implemented and published at the user's request. The [interface pass](../model-source/INTERFACE-PASS-05.md), source `b194dc6`, now ships compact launch/HUD/pause layouts, bundled Inter, charcoal/sage styling, the original logo in the interface and tab icon, and revised loading/retry presentation. Checkpoint `533570e` passed CI and Vercel deployment; the branded root and legacy route were verified live. Models and audio are unchanged. The original logo pixels remain intact; dedicated small icons, social artwork and legacy branding remain future work.

The initial request also calls for better, more audible music with a calming lo-fi feel. The audio specification below remains unimplemented. Read the current handoff rather than treating the historical baseline table as the new UI state.

Read the [current handoff](../CODEX-HANDOFF.md) before starting. This brief records the future product work separately from street reconstruction. It does not authorize map expansion or alter the saved Seventh Street quality reference.

## Resume status

| Area | State at session close | Next bounded work, only when requested |
| --- | --- | --- |
| Interface and identity | Implemented, reviewed and published; [styling contract and captures](../model-source/INTERFACE-PASS-05.md). | Refine from user feedback while preserving the established layout/type/palette. |
| Website | [DriveAround.nyc](https://www.drivearound.nyc/) serves Seventh at `/`; `/index.html` serves the legacy game. Both matched the final files after checkpoint `533570e`. No DNS work was needed. | Recheck host/route state when a later task depends on it; do not create another project. |
| Icons and sharing | Original full PNG is used for Seventh favicon/touch icon and identity; no dedicated tiny-icon or social-art derivatives. | Inspect/prepare deliberate native-size artwork and legacy treatment. |
| Music and levels | Original 12-second track and −23 dB music gain remain; no new listening or mixed-output measurement. | Audition music balance/arrangement using the specification below, with repeatable listening evidence. |
| Reconstruction | Portable skill is ready; no next street assigned. | User supplies a bounded street/task; use its inventory and review gates. |

The specifications below include both completed interface requirements and remaining proposals. Read this status table and the implementation report before starting so a new session does not redo the published UI or silently begin the audio backlog.

## Intended experience

An unhurried evening drive through a recognizable New York neighborhood. The street remains the main attraction. Branding, loading, controls and audio should feel like parts of one considered experience: warm, restrained, easy to understand and comfortable over a long visit.

Keep the established “Seventh, slowly.” chapter identity under the **DriveAround.nyc** product name. Retain the existing apricot car, muted blue-green/cream palette and golden/dusk/rain moods as the starting point. Improve visual consistency and sound balance before adding more decoration. The user's calm direction is not a request for extra moving grain, flashing effects, repeated notifications or a large landing page that delays playing.

## Historical baseline before the interface pass

This is a source/document audit of checkout `e65e835` on `main`, with gameplay/model baseline `d4fbafe9a6af4497de81e2220d31c878f930612e` and routing fix `bfbc8d764f838708f753a53de9b7f054101b45f0`. No new browser session, performance run or listening review was performed.

| Area | Current state | Future work |
| --- | --- | --- |
| Supplied mark | [drivearoundnyclogo.png](../drivearoundnyclogo.png): a grey Statue of Liberty rising behind a front-facing car, on a white square with generous margins. Inspected directly; 2000 × 2000 PNG, **no alpha channel**. It is the user-supplied master, included unchanged with the documentation publication. | Preserve the original and create deliberate web/icon derivatives when implementation is requested. |
| Seventh shell | Product/chapter text, warm gradient loading screen, serif heading, progress, Retry, graphics-loss recovery and local credits. Favicon is an inline “7” tile; the supplied logo is absent. | Apply the actual identity across loading, tab icon, error/retry and metadata. |
| In-game interface | Text-only product name, chapter title, weather/sound/pause, map/speed/address, camera/postcard, intro and pause panels. HUD buttons currently use `FOCUS_NONE`; many dimensions/hints are fixed. | Consistent logo/type/spacing and tested narrow-layout behavior; make settings and menus usable by keyboard. Do not claim current keyboard shortcuts establish menu accessibility. |
| Legacy game | DriveAround.nyc text and metadata; blank `data:,` favicon. | Share the identity where appropriate while preserving this distinct game's behavior. |
| Music | Original synthesized `cornerlight.wav`, 12 seconds, mono, 22,050 Hz; four chords and a beat every 0.75 seconds (80 BPM). Runtime music gain is **−23 dB**. | Audition a more audible music balance and a less repetitive, smoother arrangement. |
| Sound controls | One Sound/M toggle for music, rain and driving sounds; sound defaults off for a fresh visitor and the preference is saved. No separate music/effects levels. | Simple, persistent music/effects balance and immediate mute, with a deliberate first interaction to enable sound. |
| Audio evidence | [Existing PCM report](../model-source/engine-review-2026-09-14-02/audio-levels.json) records source-file peaks/RMS/duration and boundary deltas. The [revision 02 report](../model-source/SEVENTH-ENGINE-02.md) explicitly leaves subjective listening review open. | Measure and listen to the actual mixed browser output. Source peaks alone cannot establish its balance, seamlessness or comfort. |
| Hosting | Last recorded live verification is September 15 at `borough-drive.vercel.app`. Both current Seventh shell files contain a `drivearound.nyc` canonical URL; that is branding intent, not evidence the domain works. | Use the verified deployment host for canonical/share URLs until the custom domain is separately connected and checked. |

Original-logo SHA-256: `9156dec61cc0ab10adb5b471e7f80d77d4e79102c2a4069e09227f93462f5448`. Keep this master recoverable; do not overwrite it while making derivatives. The September 21 push follow-up saves this original source asset with the documentation; no web/icon derivative is implemented.

## Brand and interface specification for a later implementation

### 1. Turn the supplied mark into usable assets

- Keep the car/Liberty relationship, proportions and recognizable silhouette. Inspect the supplied pixels instead of generating a substitute. Do not silently redraw the statue or assign a new brand concept.
- The original's white field is real image content. Decide deliberately between a clean light backing and a carefully prepared transparent derivative; inspect antialiasing at the silhouette edge and inside the car openings. Do not use a crude near-white cutoff that damages details or introduces a halo.
- Crop excess outer margins for use at practical sizes, preserving breathing room around the torch and car. Pair the mark with a clean `DriveAround.nyc` wordmark for loading/intro; use a restrained compact treatment in the HUD.
- Prepare an actual small-icon treatment, inspected at 16, 32 and 48 pixels at normal display size. The full detailed statue may become illegible; a simplified derivative must visibly retain the supplied identity. Keep the full mark for larger placements. Do not fall back to the old “7” just because it is easier to read.
- A proposed deliverable set is favicon ICO/PNG sizes, a 180-pixel touch icon, a suitable social-preview image, and light/dark logo placements. A manifest/PWA installation flow is not required merely to provide icons. Avoid adding external font or asset requests to startup.
- A possible shared web destination is `dist/brand/`, referenced with absolute `/brand/...` paths to avoid the Seventh shell's `<base>` changing their resolution. This folder and its assets do not exist as a result of this brief. Godot requires an imported asset under its own project if the logo appears inside the canvas. Make both uses reproducible from the preserved master.

### 2. Carry one identity through every state

| Surface | Required result |
| --- | --- |
| Browser tab and bookmark | Legible supplied-identity favicon, purposeful page title and no stale old icon after cache refresh. |
| Initial loading | Logo/product first, chapter second, calm short copy, meaningful loading progress, readable help and credits. Avoid showing two competing full identity screens as the HTML loader hands off to the engine intro. |
| Intro | One clear primary action to drive, immediately understandable sound choice, concise keyboard/mouse guidance. Preserve the user's choice to play silently. |
| Driving HUD | Small identity, clear control hierarchy, quiet panels and enough unobstructed street. Address labels stay limited to the established First–Second segment until a later geography task changes that scope. |
| Settings and pause | Readable labels, predictable controls and saved audio settings; muted/on states distinguishable without relying on color alone. Preserve camera-only recenter versus car reset. |
| Download/graphics failure | Same logo, typography and spacing; plain explanation, visible Retry and reliable recovery. Keep technical logs out of normal product copy. |
| Credits and sharing | Readable, reachable existing notices; coherent preview/title/description and host-correct absolute metadata. Do not use a photographic source or private screenshot as promotional artwork. |
| Preserved legacy route | Matching favicon/product treatment where requested; original controls, geometry and credits remain intact. |

Use a small shared palette, type hierarchy, spacing scale and radius treatment across HTML and Godot. Record those choices once in a durable brand specification so later street chapters do not invent new UI styles. Existing shell values such as deep blue-green `#283f46` and warm cream are useful starting references, not an approved final brand guide.

Review at ordinary desktop sizes, a small laptop, narrow windows, high pixel density and increased text/browser zoom. Long hints, intro panels and footer text must not collide or hide primary actions. Narrow presentation support is not evidence that touch driving exists; describe the current keyboard/mouse requirement honestly. Preserve CSS-pixel canvas sizing and the existing rendering budget.

Provide visible focus, useful accessible names and an orderly keyboard path for settings, start, pause and retry. Interaction with a slider or menu must not also steer the car. Respect reduced-motion preferences in added decorative transitions; avoid flashing. Check actual text/panel readability over golden, dusk and rainy scenes, including credits and muted labels. Do not claim full accessibility based on a canvas `aria-label` alone.

## Music and sound specification for a later implementation

### Establish balance before selecting a new track

The saved music has source RMS about `0.1231`; applying the current −23 dB gain gives an approximate isolated RMS of **−41.2 dBFS** before other processing. This is a calculation from historical source measurements, not a recording of the current browser mix or a perceived-loudness measurement. Engine and rain are controlled independently in code and can mask it. Turning up the entire master would also increase those sounds.

First create short, repeatable A/B captures of the current mix and a modest music-only increase (for example **+4 to +6 dB as audition candidates**), keeping device output and driving/weather conditions fixed. Choose the result by listening; these numbers are not the user's approved mix. Adjust music against engine, tires, impact and rain rather than assuming a particular gain solves perceived loudness.

The goal is music that is clearly present while cruising, with enough driving feedback to understand motion and traction. Rain should feel like atmosphere, not broadband noise covering the chords. An impact should be noticeable without becoming startling. Do not change physics to make the audio demo easier.

### Improve musical comfort

- Preserve the warm, relaxed harmonic direction and moderate tempo. Favor soft keys, rounded bass, restrained percussion and gentle variation; exact instrumentation is a proposal for listening review.
- The current 12-second repetition is a candidate improvement, not proof the track is unpleasant. Audition a longer arrangement with subtle changes and a carefully composed return to its beginning. Listen for recognizable restart patterns, abrupt reverb cuts, clicks and silence between repetitions.
- Keep transients and bright percussion controlled. Add hiss, vinyl noise, detuning or stereo movement only if they improve long-session comfort; “lo-fi” does not require constant crackle or harsh filtering. Check mono/laptop playback if using stereo.
- Smooth enable/disable, level changes and track transitions. Decide and implement explicit behavior for pause, hidden tabs, focus return and reload; the existing sound toggle does not itself specify these policies. A sensible calm default is to fade or pause while hidden and resume only in a predictable way, without sudden full-volume restarts.
- Add separate music and effects levels with a master mute if the later UI scope permits. Persist them with existing settings, handle unavailable storage gracefully, and preserve fresh-visitor silence until a user interaction enables sound. Rain can initially belong to effects; a third ambience slider is optional, not mandatory complexity.
- Start with the original reproducible synthesis, which has an existing local provenance chain. A replacement recording must carry its actual source, creator/license, permitted redistribution and durable local asset record. Do not assume a track labelled “lo-fi” or available to stream can be shipped in the game. No acquisition or paid generation is authorized by this brief.

Use headroom across the **sum** of music and simultaneous effects. Check a loud realistic case: acceleration, tire scrub, rain and impact. Source normalization to a peak of about `0.76` does not guarantee the sum will stay unclipped. Record source/output peaks and a consistent loudness measurement when tools are available. EQ, compression or a limiter may help after the balance is understood; do not hide distortion or audible pumping behind a nominal peak result.

## Implementation map and invariants

| File or area | Responsibility |
| --- | --- |
| [Source shell](../engine/first-seventh/web/shell.html) | Browser metadata, favicon, HTML loading/error/retry UI and canvas sizing. Preserve `$GODOT_*` template fields. |
| [Exported shell](../dist/seventh/index.html) | Actual served Seventh HTML, derived from the source template. A patch here alone will be lost during the next export. |
| [HUD](../engine/first-seventh/scripts/hud.gd) | In-canvas intro, identity, controls, panels and settings UI. |
| [Main runtime](../engine/first-seventh/scripts/main.gd) | Audio setup, enabled state, preference persistence and focus/pause integration. |
| [Car audio](../engine/first-seventh/scripts/car_audio.gd) | RPM/load/tire/road/impact mix. |
| [Audio recipe](../model-source/make_seventh_audio.py), `engine/first-seventh/assets/audio/` | Reproducible original WAVs; running the current recipe rewrites music **and** effects, so scope changes carefully. |
| [Legacy shell](../dist/legacy.html) | Preserved original game metadata/favicon and its existing entry point. |
| [Exporter](../scripts/export-seventh.mjs), [verifier](../scripts/verify-seventh.mjs), [build manifest](../dist/seventh/build.json) | Reproducible runtime export and exact package/source hashes. The original logo, Inter WOFF2 and OFL file are explicitly copied/verified; font sources are hashed. Additional assets must enter this path because arbitrary web files are not copied automatically. |
| [Vercel routes](../vercel.json), [local server](../scripts/serve.mjs) | `/` → Seventh; `/index.html` → legacy; `/seventh/` remains directly usable. |

**Keep `dist/index.html` absent.** Vercel serves filesystem entries before rewrites; creating that file would break the intended root route. Keep `/seventh/` as the shell's base and preserve JS/PCK/WASM resolution on both root and direct visits. `dist/` contains required tracked assets, not disposable output.

For later shell-only work, keep template/exported HTML and `build.json` file bytes/hashes plus source-shell hash synchronized. For Godot HUD/audio changes, use the documented `npm run seventh:build` path so the shipped PCK contains the new code/assets. Do not “fix” hashes to imply stale runtime assets include source changes. Do not regenerate buildings for a branding/audio-only change. Preserve model/provenance files, the accepted core/corner and required license notices.

## Acceptance and handoff for that later work

1. **Identity review:** inspect actual loading/intro/HUD/pause/error states and icons at native display size. Confirm original mark recognizable, text consistent, margins deliberate, all states legible, and no new asset/network failures.
2. **Interaction review:** test keyboard focus, mute/sliders and saved settings, unavailable storage, pause/focus/resume, retry, reduced-motion behavior, narrow layouts and zoom. Confirm camera controls, driving, address scope and postcard remain usable.
3. **Listening review:** record/listen on ordinary laptop speakers and headphones at consistent device volume. Compare idle, cruising, acceleration, drift, impact, rain, pause/resume and several consecutive musical loops. Include a continuous session long enough to judge repetition and fatigue. Save the actual listener's observations, not only telemetry. User listening feedback is needed to settle subjective comfort.
4. **Technical checks:** run `npm run seventh:verify` and `npm run verify` for changed runtime/source as applicable. Reuse relevant existing browser review scripts for interaction regressions. Verify `/`, `/seventh/`, `/index.html`, brand asset URLs and credits locally; injected load/context failures must recover. Check download-size/startup/frame cost against the same environment if new assets or rendering effects could affect them.
5. **Evidence:** record exact candidate/source hashes, before/after UI captures, audio files/mix parameters and measured results with their environment. Label unperformed tests and subjective questions. Historical September reports do not test the new package.
6. **Save:** update the current handoff and session log with actual local/commit/push/deployment states. Follow the session's current publication authorization; September 21's finished interface is already published and the domain works. A future feature's local review does not itself establish live deployment or photographic fidelity.

The user is closing the session. Continue from their next bounded request about the published interface, music/icons or a named street. Nothing is queued to run after closure.
