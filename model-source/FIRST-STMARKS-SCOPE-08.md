# First Avenue and St. Marks Place — confirmed scope, October 11, 2026

**Latest review:** the full bounded revision 08 is implemented locally. The user likes the overall result but requests substantially richer, more individual storefront detail, naming Tile Bar as the reference. The [storefront standard](skills/reconstruct-street/references/storefront-individuality.md) captures this feedback; this instruction-update follow-up leaves the export unchanged. Read the [current handoff](../CODEX-HANDOFF.md) before treating the original implementation authorization below as unfinished work. The geographic bounds remain resolved.

The user wants to resume reconstruction with First Avenue and the street immediately north of Seventh, **St. Marks Place**, and answered **“Yes, those full bounds”** to the complete extent below. Implementation is authorized. The September close and earlier endpoint question are superseded.

## Confirmed bounds

| Segment, both sides | Mapped facade records | Distinct buildings | Buildings absent from starting Godot slice |
| --- | ---: | ---: | ---: |
| First Avenue, East 7th to St. Marks | 16 | 16 | 0 |
| St. Marks, Second Avenue to First Avenue | 47 | 46 | 0 |
| St. Marks, First Avenue to Avenue A | 35 | 35 | 21 |

The confirmed union has **98 primary faces on 95 buildings**, including shared corner parcels and two geometric faces at 39 St. Marks. Another eight mapped faces are listed as same-parcel corner returns; two of those face Seventh and are protected. These are mapped counts, not a completed photographic property/access/fixture survey. All primary and return faces have stable `buildingId:frontageIndex` keys in the [scope inventory](first-stmarks-scope-08.json).

The endpoint question is resolved. Use the reconstruction [skill](skills/reconstruct-street/SKILL.md#establish-the-task) for the complete confirmed extent; no additional permission cycle is needed for the necessary local implementation and review.

Corner coverage stops at each included corner parcel's first property boundary, with no adjoining avenue block added. Keep the existing First & Seventh corner intact, including First Avenue faces `241822226:1` and `248142707:1`. Site/building `248142717` has no address in the map; its source observations are recorded without inventing a street number. Browser inspection also identified the separate low painted site edge west of 110.

## Baseline and preservation

- Starting checkout: `main`, **`d4e147e1bc559b9ef76429c8c74887048ceb45ac`**. Work branch: `feature/first-stmarks-08`. Cached `origin/main` matches the baseline; no fetch in this task. Initial working tree contained only the two private untracked screenshots. [Baseline preservation hashes](first-stmarks-review-08/baseline.json) freeze 1,145 tracked non-Markdown files, 182 model hashes and the two private screenshots (hashes only).
- Architectural source: **`098f1cc89b41c2067fe1577ddb62df5a3b3c6002`**, revision 07. Published method release: `4b999cd`; last independently verified publication checkpoint: `78aa716`. No new live/CI check in this task.
- Local PCK SHA256 re-read: **`746113ee606ebfb6b6b0e32861974ce2ae3445c25d7a6b509b011c7c6bd393fa`**. Existing Godot slice: 182 building records.
- Preserve the original game and First & 10th core; both Seventh blocks; accepted corner IDs `241822226`, `241829631`, `248142331`, `248142404`, `248142707`; compact interface, controls, audio, routing, credits and private screenshots.
- Source coordinates come from `dist/reconstruction/neighborhood.json`; source x increases east and z increases south. The current runtime uses `z = source_z - 228`. The inventory retains exact mapped tangents, lengths and source hashes. These are existing authored coordinates, not new survey measurements.

## Completed local candidate

The complete confirmed extent is implemented: **102 editable faces on 93 buildings** after excluding the four protected First & Seventh surfaces. All 182 original building objects remain, with 21 eastern St. Marks additions for 203 total. The [revision 08 report](SEVENTH-ENGINE-08.md) records modeled features, actual source-to-game review, package identity, preservation, driving/performance checks and remaining precision.

The [browser ledger](first-stmarks-browser-08.json) contains 55 dated ordinary-browser view locators and initial observations on 104 of 106 mapped faces; the two others are protected Seventh returns. Imagery includes April 2026 and September 2024 and is not a verified October occupancy snapshot. Source pixels remain temporary local inspection material, never committed game assets. The scope JSON remains the frozen confirmation-time inventory; its authoring-time status is historical.

The exact-face [adapter](first_stmarks_kit.py) consumes only the new `firstStmarksEngine` namespace. The complete [authoring packet](author_stmarks_08.py) imports the [First Avenue packet](author_first_stmarks_08.py), keeping old Seventh and legacy namespaces unchanged. Source-to-game review covered all draft elevations, final overlapping ground crops and affected repair elevations, with perspective/player-camera review. These checks do not establish calibrated acceptance.

The bounded St. Marks/Avenue A route is open; all 18 endpoint-based driving checks pass across three weather modes with zero contacts. Original/package checks and preservation pass. Both performance runs, including initial pauses and the focused repeat, are retained in the report. The user can review the included export by running `npm run dev` and driving north from First & Seventh to St. Marks.

Everything remains local on `feature/first-stmarks-08`; read the [handoff](../CODEX-HANDOFF.md) for exact commit/save state. No push, deployment, paid API request or source-image publication is requested. No scope question remains pending, and no further street is queued.
