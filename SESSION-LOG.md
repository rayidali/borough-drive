# Borough Drive session checkpoints

[CODEX-HANDOFF.md](CODEX-HANDOFF.md) holds the current resume state. This log preserves dated milestones in **newest-first order**. Add a checkpoint after meaningful progress and before a planned session handoff; record partial work during long tasks as well. Preserve older entries and record corrections in a later entry.

Use the exact gameplay/source commit as the reproducible baseline. Git history records the commit that saves each checkpoint document:

```sh
git log --oneline -- CODEX-HANDOFF.md SESSION-LOG.md
```

Checkpoint notes describe observed state, not a live monitor. Recheck local files, remote branches and deployment status when resuming. Keep necessary artifacts in the repository and record reproducible commands; temporary directories and old tool/process IDs are not durable checkpoints. Store no tokens, passwords or authentication cookies here.

## 2026-09-06-01 — Revision 04 published; session continuity established

**Recorded:** September 6, 2026, 22:52 EDT (`2026-09-06T22:52:44-04:00`). This first entry summarizes the completed work leading into the checkpoint; it does not invent boundaries for earlier sessions.

**User objective and decisions:** Improve the realism of the entire existing East Village map, preserve the accepted First Avenue/East 10th Street core, publish the complete latest version to `main` and Vercel, and preserve enough context to resume after closing a session. Blue & Gold was an example of map-wide fidelity problems. The user chose GitHub owner `rayidali` and MIT for original contributions; third-party terms remain in their notices. No new geographic expansion or further feature was selected.

**Completed work:** Published all fourteen rebuilt neighborhood sections, restored five missing buildings, added the facade/business evidence and corrections, updated street facilities and map place/address search, and included the reproducible recipes and README screenshots. The active map has 615 building objects, 410 photo-observed non-core building records and 212 supported named places. Added the Vercel static hosting configuration and a public play link. This checkpoint adds the current-state summary, session log/template and agent instructions for keeping both updated.

**Code and publishing state:**

| Milestone | Commit | Result |
| --- | --- | --- |
| Initial public repository | [`e44c343`](https://github.com/rayidali/borough-drive/commit/e44c3431faff77acac14fdaad8d4d6c959ea2ddc) | Original exported map and open-source repository setup |
| Vercel 404 correction | [`0ed0d53`](https://github.com/rayidali/borough-drive/commit/0ed0d53ed1acea382282c601fc9685f34be0b69f) | Served `dist/` at `/`; map still matched the initial public version |
| Complete neighborhood accuracy revision 04 | [`835ea6c`](https://github.com/rayidali/borough-drive/commit/835ea6cb53f7b88ebc0edc9586080f9c371b9d20) | Pushed to `main` and `origin/main`; Vercel deployment completed successfully |

**Production verification:** [borough-drive.vercel.app](https://borough-drive.vercel.app) served the latest homepage. SHA-256 comparisons matched all 35 changed game files, including the fourteen rebuilt section GLBs, against `835ea6c`. The live manifest reported revision `04`, 615 buildings, 410 observed non-core buildings, 212 named places and the `blue_gold` ground profile. The successful Vercel status for this gameplay commit was rechecked while preparing this checkpoint.

**Validation and limits:** Local `npm run verify` passed before publication, including 2,308 road samples, model/texture references, vehicle/navigation invariants, restored buildings, courtyard collision and business partitions. GitHub Actions passed on Node.js 22 and 24. All eight changed Python files parsed, and the final staged diff passed whitespace checks. Earlier local browser review, source reproduction and performance observations are recorded in [the accuracy audit](model-source/ACCURACY-PASS-04.md) and [its review record](model-source/accuracy-review-2026-09-06.json). The deployment comparison establishes file identity; it is not a new visual or frame-rate assessment. This handoff task changes documentation only, so it does not require another model or vehicle test run.

**Local work and blockers:** Gameplay work was fully committed and pushed; the working tree was clean before the checkpoint documentation edits. No unfinished feature, pending model rebuild or known blocker remains. The checkpoint documents are saved in their own Git commit; use the command above to identify it. Local servers and browser processes are not required to recover the project.

**Known limitations:** This remains an uneven reconstruction, with 142 non-core objects having mapped frontages but no individual photographic observation. Unseen geometry, several dimensions, shop partitions, interiors and street dressing remain estimates. Current business evidence is dated September 6, 2026 and photographs may be older. Preserve these distinctions and all original asset credits. Package version `0.4.0` and the page's chapter label are insufficient to identify which map was deployed.

**Next action:** Read the current handoff, inspect the actual Git state, and continue with the user's next request from revision 04. Use `npm run dev` for local review. If the next request concerns accuracy, start from the audit's unresolved coverage and dated evidence. Existing exports are included; do not rebuild the complete neighborhood merely to reopen it.

## Template for the next checkpoint

Add the new entry above the latest checkpoint, update the current-state section of `CODEX-HANDOFF.md`, and replace every placeholder with an observed value, `none`, `not checked`, or `pending` as appropriate. Keep the entry concise and link detailed reports instead of copying them. A documentation-only follow-up can retain the same gameplay commit; its own revision is found through Git history.

```markdown
## YYYY-MM-DD-NN — Concrete milestone or stopping point

**Recorded:** Date, time and time zone.
**User objective and decisions:** Scope, accepted preferences and publishing instructions.
**Completed work:** Changes and relevant files or reports.
**Gameplay/source baseline:** Full commit SHA and branch; identify any later uncommitted work separately.
**Local changes:** Modified/untracked files, unfinished work and necessary artifacts.
**Remote state:** Which commit was pushed, to which branch; or not pushed/not checked.
**Deployment state:** URL and exact commit verified; pending/not deployed/not checked when applicable.
**Validation:** Commands, results and the commit/files tested; distinguish earlier evidence from new checks.
**Unresolved issues:** Failures, uncertainty, blockers and any pending user answer.
**Next action:** The first concrete step and enough context to continue safely.
```
