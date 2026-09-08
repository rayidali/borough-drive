# Storefront fidelity pass 05 — September 8, 2026

The user's target is a digital twin of the entire existing neighborhood, including outdoor seating, boards, illuminated signs, paint, size and architectural detail. The start/reset now uses First Avenue/East 7th Street, facing north. This pass replaces estimated shop templates at **22 businesses across nine sections**, with **26 separately controlled building elevations** and **29 source records**. It is incremental work; it does **not** establish 1:1 completion.

## Changes

[storefront-details.json](storefront-details.json) is the editable source. It separates observed feature types from estimated dimensions and ties each design to an existing supported business on a specific street.

- **First & 7th:** Tile Bar's striped blue awning, green recessed door, low divided window, orange/red surround, tiled base, illuminated window lettering, red folding furniture and board replace the old cafe template. Its two upper elevations have separate opening schedules.
- **Nearby First Avenue:** Hen House has orange script lettering and a round projecting sign in the northern 120 First Avenue unit. The corner building gains seven avenue bays, dark trim/cornice and a blind white panel on its East 7th return. Yubu is narrowed to the small western unit at 86 East 7th, with timber glazing, red awning and a small folding table. Nudibranch's lettering goes on glass. Two additional 7th Street elevations receive observed trim, escape color and roof railing.
- **Avenue A:** Individual designs distinguish Ray's turquoise frontage/fries blade; Maya's outlined lettering, gooseneck lights and board; St Dymphna's yellow base/green divided doors; Superiority Burger's lightbox/message board; and Luster's two-line blue fascia. Others cover Lucy's script and diamond grilles, Doc Holliday's curved awning, Ralph's serving frontage/menu panels, Baba Doner's round blade/bench, Danny & Coop's oval sign/shutter, Tompkins Square Bagels, Lucinda's illuminated script/six-panel timber front, Niagara, Miss Lily's, Peace and The Rabbit's scalloped awning/recessed doors.
- **Cross streets:** Existing Irving Green and Casey Rubber Stamps observations now control windows, doors, signs, bench and display details. These two records reuse earlier written observations; no new photographic inspection of them is claimed.

The recipe respects a separately observed side escape when the primary elevation has no escape. Five previously ineffective records are in the affected southern sections. The accepted First & 10th GLB, recipe and six licensed photographs remain preserved.

Two business joins are corrected: Ralph's Famous and the researched Ralph's Italian Ices are one shop; Danny & Coop's belongs to 151 Avenue A rather than being duplicated at 153. There are now **210 named places, 200 outside the core**. These are identity corrections, not newly asserted openings or closures.

## Evidence and limits

Newly inspected photographs include the Tile Bar website, EV Grieve, Kevin Walsh's Forgotten NY photographs and Village Preservation's archive. They are **observation only**; no downloaded reference pixels are redistributed. Dates, unknown capture dates, publishers and URLs remain in the schedule. Two reused cross-street observations are identified separately.

Shop spans, frame depths, furniture dimensions/positions and paint values are visual estimates. Materials are representative surfaces, not calibrated paint samples or masonry scans. OFL-licensed Damion approximates some script signs, without reproducing original logo outlines. Unreadable menus/stickers and temporary message-board wording remain simplified. Murals and unseen rooms are not invented as verified artwork. Furniture and shutters show a photographed configuration, not guaranteed present-day conditions.

**This does not cover every shop in the rebuilt sections.** Of 200 supported names outside the core, 178 still use estimated shop designs. The 410 observed-building count describes partial evidence, not complete elevation coverage. [digital-twin-coverage.json](digital-twin-coverage.json) lists all 641 non-core street frontages and their remaining evidence needs. Regenerate it with `python3 scripts/audit-storefront-coverage.py` after compilation. Current photographs, measurements, exact artwork and secondary-elevation evidence remain outstanding for much of the map.

## Reproduction and review

```sh
python3 scripts/compile-neighborhood-details.py
blender -b -t 6 --python-exit-code 1 --python model-source/build_neighborhood.py -- \
  --tile block-2-1 --tile block-2-2 --tile block-3-1 --tile block-3-2 \
  --tile block-4-2 --tile block-5-1 --tile block-5-2 --tile edge-east --tile edge-south
npm run verify
python3 scripts/verify-neighborhood-reproduction.py
```

For clean data preparation, run `scripts/prepare-neighborhood.py` first. Models and the typeface are included. Per-section source signatures detect stale storefront exports separately from the underlying revision 04 facade markers.

For actual browser review, run `npm run dev` and a separate Chrome process with `--remote-debugging-port=9222 --user-data-dir=/tmp/borough-browser-review`, then `node scripts/review-storefronts.mjs`. This uses Node's built-in WebSocket support and Chrome DevTools; it adds no npm packages or instrumentation to the published app. It checks the start, northbound driving, keyboard reset, walking reset, every new frontage, seven projecting-sign views and all 26 elevation schedules. Captures default to ignored `renders/`.

The final local exports passed `npm run verify` on Node.js 24.15.0, including 2,308 road samples, source/model signatures, safe start and map spawns, walking collision for ten observed furniture/board objects, module/assets and vehicle invariants. Fourteen neighborhood GLBs total 49.14 MiB and 8,906,922 triangles; nine were rebuilt. The largest section uses 50 material batches. These checks do not establish visual accuracy or frame rate.

Actual Chrome review on Apple M1 checked 56 viewpoints with zero uncaught errors or failed HTTP responses. The new start is `(0, 228)`, northbound; initial load, driving and both reset modes passed. Storefront and upper/side elevation captures were visually inspected. Trees and parked vehicles partly occlude some views. The browser's existing automatic quality adjustment disabled ambient occlusion; no performance benchmark was performed. Unedited game captures show [First & 7th](../docs/images/first-and-seventh-revision-05.png), [Tile Bar](../docs/images/tile-bar-revision-05.png), and [Hen House](../docs/images/hen-house-revision-05.png).

[storefront-review-2026-09-08.json](storefront-review-2026-09-08.json) saves the browser poses, graphics settings, asset hashes, preservation checks and limitations. A disposable clean prepare/compile matched all 615 building source records and three generated audits. This review also fixed duplicate address aliases in preparation/compilation. Three pre-existing landmark `renderHeight` fields are written by Blender (St Cyril, St Mary and a ruin); source reproduction compares the pre-export schedules separately from these exported subdivisions and GLB metadata. The core GLB/recipe, vehicle module, six licensed photographs, all 615 mapped footprints/heights and the roads/driving bounds match revision 04. The current handoff/session log records commit, push and deployment states separately.

## Engine decision and remaining work

Blender authors meshes; Three.js renders the browser game. Keep that combination while improving evidence and individual assets. Changing engines cannot supply missing photographs, dimensions, sign artwork or outdoor configurations.

For a future desktop application with dense scans, Unreal is a reasonable candidate: [Nanite](https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-virtualized-geometry-in-unreal-engine) supports dense geometry, including photogrammetry. Capture, cleanup and target-device checks would still be needed. [Godot's web export](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html) has its own rendering/platform limits. No migration was made or assumed authorized.

Continue frontage by frontage within the existing bounds: collect dated head-on and oblique photos, separate current tenant evidence, measure facade/opening/sign/threshold dimensions, and record outdoor setups as date-specific. Resolve secondary elevations and small architectural features before marking them observed. Use licensed imagery or user-owned capture for photographic textures. Compare each export against matching real viewpoints; code checks cannot certify visual fidelity.
