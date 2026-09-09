# First Avenue / East 7th Street — study 06

Local comparison pass, September 8, 2026. The user resumed work at this intersection to establish a detailed standard before extending block by block. Use the most recent accessible view. The new work has not been pushed or deployed; [the handoff](../CODEX-HANDOFF.md) records the exact source commit and publication states. The online game remains the previously published pass 05.

## Implemented scope

Five building objects cover the four corners and Saifee's adjoining frontage. Their nine exposed elevations use individual schedules in [first-and-seventh.json](first-and-seventh.json), implemented by [first_seventh_kit.py](first_seventh_kit.py). Eight shops receive bespoke treatments; the overall non-core design inventory increases from 22 to 27 because Tile Bar, Hen House and Yubu already had designs.

| Corner | Building and exterior changes | Shop and street details |
| --- | --- | --- |
| NW | 115 First / 87 East 7th: two avenue window stacks, irregular return openings, thin dark lintels, side fire escape, parapet and antenna rack | Tile Bar's orange-red paint, stepped olive/plum tile patches and checker detail, recessed green 115 door with kickplate, divided low window, paired awning stripes, beer lettering, red tables/folding chairs, board and potted plant |
| NE | 118–120 First / 91 East 7th: seven avenue window stacks, two return stacks beside the broad pale blind panel, bracketed dark cornice, individually placed AC housings | E7 Deli's black slatted signs and striped recessed entry; Hen House's orange script and blue blade; Monkey Sushi's surviving small Unique notice, noren and bamboo blind; 7th Street Burger's projecting wood windows, central door, letterboard, AC and diagonal cellar hatch |
| SW | 113 First / 86 East 7th: three avenue window stacks, five visual stories, painted brick, pale lintels, side escape and stepped roof cornice | E Smoke's raised red letters, category fascia, ribbed soffit, shelving and entry rail; Yubu's narrow wood frame, red awning, AC, notices and slatted folding table with red legs |
| SE | 116 and 114 First: lower four-story buff-brick corner next to five-story painted-red building; two versus three avenue window stacks, grilles, tapered lintels, red/black escapes and roof railing | Connected brown Saifee awnings with individual lettering, hanging vines, six-level wheeled plant racks, pots and visible stock, door notices and open lettering, shutter hardware and facade string lights |

The corner also has separately authored signal housings, pedestrian hands, street/one-way signs, lamp masts, two mailboxes and litter baskets. Their placements are estimates. Generic duplicate furniture was removed in the immediate intersection. The side mural at E7 retains its observed blue field; unseen artwork is not invented.

Saifee 116's rendered roof is estimated at 13.15 m; 113 First's is estimated at 16.7 m to reflect the observed four- and five-story proportions. Original mapped height fields, all 615 footprints and every road/boundary remain unchanged. These are visual estimates, not survey corrections.

## Evidence and its limits

Sixteen source/access records retain individual page and photo URLs, authors/publishers where available, known publication or upload dates, observations and reuse status. New reference photos were inspected and are not bundled as facade textures. Existing core photos and all license notices remain preserved.

| Exterior | Most recent accessible view used in this pass |
| --- | --- |
| Saifee | [EV Grieve, September 5, 2025](https://evgrieve.com/2025/09/sept-5.html), supported by October/November 2024 display views |
| Monkey / former Unique | [EV Grieve, July 3, 2025](https://evgrieve.com/2025/07/openings-monkey-sushi-on-1st-avenue.html); June 20 photo filename; still shows the old small Unique notice |
| E7 Deli | [eastvillage.com](https://eastvillage.com/shopping/e7-deli-cafe/e7-deli/), March 2024 image upload; capture date unknown |
| Hen House | [EV Grieve, November 24, 2023](https://evgrieve.com/2023/11/signage-alert-hen-house-on-1st-avenue.html) |
| Tile Bar | [Official site](https://www.tilebarnyc.com/), July 26, 2023 filename; capture date not independently confirmed |
| Yubu | [EV Grieve, July 21, 2021](https://evgrieve.com/2021/07/openings-yubu-on-7th-street-evil-katsu.html) |
| 7th Street Burger | [EV Grieve, June 7, 2021](https://evgrieve.com/2021/06/openings-7th-street-burger-on-7th-street.html); current address corroborated separately |
| E Smoke | Business-credited exterior photo with unknown capture date; official address and dated retail-license evidence retained |
| Upper architecture | Individual Village Preservation archive views, generally 2012 upload paths with unknown capture dates; Saifee additionally visible in the 2025 photograph |

Google Maps place listings were accessible, but the Street View interface returned “No Street View imagery available here”; its panorama thumbnail request returned HTTP 403. No capture date could be obtained. This pass cannot be described as a comparison with the newest Google panorama. The source record explicitly preserves that failure.

The modeled openings, paint families, signs and movable objects follow these references. Exact fonts/logos, mural artwork, tiny product labels, complete room layouts, surface scans, dimensions and partly obscured return details remain incomplete or inferred. Windows and street-object positions are not surveyed. Daylight rendering combines views taken in different seasons and at different times. This pass is ready for comparison as an authored reconstruction; it is not certified 1:1, photogrammetry or an accepted final benchmark. The whole-map inventory still has 177 supported non-core names with estimated shop designs.

## Inspect the local game

Run `npm run dev`, then open http://127.0.0.1:5173. The game starts at `(0, 228)`, facing north. Four **First & 7th · detail study** buttons frame NW / NE / SW / SE. Walk closer to inspect the stores. R returns to the start in either walking or driving mode.

**Detailed** graphics preserve ambient occlusion and four-sample antialiasing. **Faster** uses simpler glass and two-sample edge smoothing to reduce GPU cost; **Automatic** can adjust after section loading. The choice persists locally. New storefront glass uses physical transmission and a reflection capture of the reconstructed intersection. Small interior lights illuminate the observed display zones. The accepted First & 10th model and recipe are unchanged.

Actual game captures: [NW](../docs/images/first-seventh-nw-revision-06.png), [NE](../docs/images/first-seventh-ne-revision-06.png), [SW](../docs/images/first-seventh-sw-revision-06.png), [SE](../docs/images/first-seventh-se-revision-06.png), [Tile Bar](../docs/images/tile-bar-revision-06.png), [Saifee](../docs/images/saifee-revision-06.png). They are unedited browser screenshots, with the normal game UI and any visible occlusions. [Credits](../dist/reconstruction/ASSET-CREDITS.md).

## Reproduce and validate

```sh
python3 scripts/compile-neighborhood-details.py
blender -b -t 6 --python-exit-code 1 --python model-source/build_neighborhood.py -- --tile block-5-1 --tile block-5-2 --tile edge-south
python3 scripts/audit-storefront-coverage.py
npm run verify
python3 scripts/verify-neighborhood-reproduction.py
```

Changes to the dedicated corner kit affect those three sections. This initial integration also regenerated six existing detailed sections because their shared-recipe signature changed: block-2-1, block-2-2, block-3-1, block-3-2, block-4-2 and edge-east. Their geometry/texture payloads and metadata, except the export signature, were confirmed byte-identical to pass 05. Core GLB, core recipe, vehicle code and six licensed photos are byte-identical to the published baseline.

Do not run the data compiler while Blender is exporting: it writes the manifest at completion. For browser review, start a separate Chrome instance with `--remote-debugging-port=9222 --user-data-dir=/tmp/borough-browser-review`, run the local server, and execute `node scripts/review-first-seventh.mjs`. The script checks start, northbound driving, both resets and corner buttons; captures 22 viewpoints; records model hashes, HTTP/JavaScript errors and short stationary samples in both graphics modes. It adds no browser instrumentation to the published game. See [first-seventh-review-2026-09-08.json](first-seventh-review-2026-09-08.json) for the completed run and its conditions. These checks do not certify visual accuracy or sustained driving performance.

Final checks passed on Node.js 24.15.0: 2,308 road samples; code/assets, export/source signatures, corner schedules, navigation and collision; clean prepare/compile with all three generated audits matching. All 22 saved game views completed with zero uncaught exceptions, console errors or failed HTTP responses. Existing RGBELoader deprecation warnings remain. Fourteen neighborhood sections total 51.78 MiB and 9,389,484 triangles; largest material batch count is 62.

Two sequential 120-frame stationary samples at 1440 × 1000 on Apple M1 / ANGLE Metal measured **25.0 fps Detailed** and **56.3 fps Faster**. Detailed retained ambient occlusion, four-sample antialiasing and physical glass; Faster used two samples, no AO and simpler glass. These short samples do not establish sustained driving performance.
