# Bounded work packet and review return

Copy the template below into a durable, task-specific Markdown file under `model-source/` when a future task is authorized. Fill it with the actual unit and baseline; this template is not an implemented queue, JSON schema or automatic runner. Do not append it to the legacy planner's JSON expecting compatibility.

The coordinator inventories the whole requested street first. Each worker receives only its unit, relevant source records/component interfaces and the images it must actually inspect. A corner with multiple faces needs separate face IDs and shared-feature ownership. Workers proposing edits to shared JSON return per-record patches for serial integration; do not let independent workers rewrite the whole file.

## Scope bootstrap when there is no ready facade packet

For a planning-only request with no verified inventory, first create a `scope-bootstrap` packet: record the requested street/endpoints/sides, baseline, protected scope, unresolved corner-return extent/date policy and known local data sources. Set facade IDs, feature observations, source inspection and adapter status to `unverified` or `needs-evidence`; do not invent them to fill the template. Inspect permitted existing local geography to enumerate exact IDs/faces when within the request. A restriction on new research/downloads does not by itself prohibit reading the existing local map.

The output is a planning draft with the next inventory/evidence action, not an execution-ready modeling job. Once the full bounded inventory exists, select one ordinary facade and fill its task packet. Keep the scope-bootstrap record linked to the complete inventory. If endpoints or corner extent remain ambiguous, resolve them before dependent implementation while continuing independent planning.

## Task packet template

```markdown
# Street task: <stable task ID>

## Instruction and baseline
- User request/mode: <plan | implement | review; exact authorized scope>
- Street bounds/sides: <street, from, to, included corner returns/sites>
- Assigned unit: <building ID + face/segment ID; display address>
- Neighbor/context IDs: <left/right, corner partner; read-only where applicable>
- Owner of shared street fixtures: <task ID>
- Target conditions: <date or explicit mixed-date policy; conflicts>
- Baseline: <branch, commit, dirty files, source-record hash, package hash>
- Protected records/assets: <IDs and paths; baseline hashes>
- Allowed files AND records: <exact patch scope>
- Outputs: <observation, proposal/source, captures, review, checkpoint paths>
- Budget/time/repair limit: <user limit or no paid calls; one focused repair default>
- Publication: <actual instruction; normally not part of a facade packet>

## Evidence
- Acquisition/inspection method: <ordinary browser Street View preferred when available; actual fallback and reason>
| Source ID | URL/panorama/local permitted path | Capture/publication/retrieval dates | View/crop/pose | Identity confirmation | Use/credit | Inspected by/when | Visibility limits |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <ID> | <durable locator> | <separate dates/unknown> | <front/oblique/detail> | <neighbor/footprint anchors> | <source registry or use record> | <actual inspection> | <occluded features> |

## Local geometry key
- Ground datum, unit scale, face endpoints and outward direction: <verified convention>
- Horizontal origin/direction: <explicit facing-building left/right and coordinates>
- Vertical/depth convention: <units; positive projection/negative recess if applicable>
- Dimension anchors: <footprint/height/photographic ratios; uncertainty>
- Effective record and consumer: <JSON path, function, precedence/overrides>
- New-street adapter status: <existing support verified | needs adaptation>

## Feature schedule
| Feature ID/location | Observation and exact source view | Dimensions/basis/uncertainty | Component + effective parameter | Required comparison | State / unresolved issue |
| --- | --- | --- | --- | --- | --- |
| <ground-entry-left> | <one leaf + fixed sidelight; source A crop> | <estimated ratios, no surveyed claim> | <record path/function> | <front closeup + oblique> | <observed, not yet modeled> |

Include floor-by-floor openings; door/access; every shop/sign; material zones,
ornament and ironwork; roof/returns; street/site/temporary features. Explicitly
mark occluded and not-applicable categories. Record exact lettering separately.

## Bounded proposal
- Current discrepancy: <source vs rendered result>
- Proposed parameter/geometry edits: <per feature; evidence>
- Shared component impact: <callers affected; isolation/preservation approach>
- Collision/streetscape joins: <affected surfaces/objects and ownership>
- Build/review plan: <real commands verified for this scope; output folders>
- Missing input or component: <small concrete issue; next evidence/action>

## Return and resume
- Source/export state: <not started | proposed | edited | exported; exact hashes>
- Visual states: <captures and actual inspection; per-feature unresolved list>
- Technical/performance state: <actual checks, device/settings, evidence paths>
- Reviewer decision: <needs-evidence | needs-component | needs-repair |
  needs-review | reviewed-candidate | accepted; identify accepting party/scope>
- Required next action: <one executable step and why>
- Attempts/actual usage: <observed values or unavailable, never invented>
- Changed files/records: <exact list; conflicts/stale baseline>
- Git/push/deployment: <three separate states; not checked where applicable>
```

## How to fill the detail rows

Write “ground residential entry left of shop; one moving glazed leaf and fixed left sidelight, `48 1/2` transom text; reference X, detail crop Y,” not “door looks accurate.” Record approximate width ratios independently from observed leaf count. For each upper floor, list opening groups from the verified face origin, widths/spacing, shapes and exceptions. A grouped bay and its sash subdivisions are different counts.

The checklist in [quality-standard.md](quality-standard.md) supplies the categories. Record small hardware/lettering wherever visible; unsupported details stay on the unresolved list. A worker can finish its code proposal while the unit still needs visual review.

## Reviewer return template

```markdown
# Review: <task ID, source and package hashes>
- Evidence actually inspected: <source IDs + views; missing sources>
- Renders actually inspected: <full elevation, two directions, entry/sign crops>
- Correct identity, scope and preserved neighbors: <finding/evidence>

| Feature | Source expectation | Actual rendered result | Pass / mismatch / unknown | Severity and specific repair |
| --- | --- | --- | --- | --- |
| <entry> | <one leaf + sidelight> | <two symmetric leaves> | mismatch | correct leaf split in <record> |

- Critical omissions/wrong counts/types/identities: <explicit list or none observed>
- Proportion/depth/material/small-detail findings: <with image locations>
- Camera comparability: <diagnostic only or calibrated evidence + second view>
- Runtime/preservation/performance evidence: <actual checks and limits>
- Decision and remaining scope: <recommendation; no invented user acceptance>
- One bounded repair request: <prioritized exact records/features, or none>
- Next action/checkpoint: <durable path>
```

## Completion and restart rules

Keep separate evidence, geometry, visual-review and user-acceptance fields. `needs-evidence` is useful saved progress, not failure to keep working on independent units. A model that cannot see images must not pass the visual gate. A capture script cannot be its own visual reviewer. The number of reviewed records is not a percentage of architectural accuracy.

After the proposed one repair, return a persistent ambiguity to a focused reviewer/evidence task. Record what was tried so the next session does not repeat it. Before merging, recheck source hashes and inspect actual changed records; file-level patch checks alone cannot enforce ownership inside a shared JSON file.

At a milestone, update the street inventory and project checkpoint. Record source/gameplay commit, local edits, tests actually run, unresolveds, push and deployment separately. Save all needed metadata and permitted evidence outside temporary folders. If source-image storage is restricted, retain a permitted durable locator and observation; do not pretend a deleted preview can be inspected offline.

For cost comparison, record model/effort when available, actual token/cost reports, acquisition/build/review time, repair count and omitted features. If the platform exposes no usage, write `unavailable`. Compare total cost per reviewed unit, not the cheapest initial proposal or a historic price example.
