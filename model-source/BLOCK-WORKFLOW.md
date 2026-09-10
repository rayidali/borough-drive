# Browser-first block workflow — September 10, 2026

The user chose smooth browser exploration, deferred Unreal, and asked for a repeatable process that can reproduce the First & 7th standard across the existing map using cheaper AI workers. Current [corner pass 08](FIRST-SEVENTH-PASS-08.md) is the visual reference; [browser pass 09](BROWSER-PASS-09.md) improves its presentation and runtime. This document specifies the next production process. It does not claim the wider map has been upgraded or that an AI batch has run.

## What is implemented now

The offline [planner](../scripts/block-workflow.py), [policy](workflow/policy.json), [source registry](workflow/sources.json), [work inventory](workflow/queue.json), [three-task pilot plan](workflow/pilot-plan.json) and [example worker packet](workflow/pilot/packet.json) are saved in the repository. The planner makes no API requests, reads no credentials, applies no patches and publishes nothing. Its validator checks ownership, source registration, stale inputs, assigned files and complete observation categories; it cannot certify visual fidelity.

Patch validation checks file headers and the proposal's declared building/elevation. It does not prove that the patch changes only those JSON records. Before applying any proposal, the coordinator must run `git apply --check` in the isolated checkout and inspect the actual changed record IDs and values. Source permissions in the registry are an owner's attestation, not an independently verified license grant.

The queue contains **1,348 explicitly owned work items**:

| Work | Count | Coverage rule |
| --- | ---: | --- |
| Facade sections | 672 | All 641 non-core sections plus 31 protected core sections. Separate geometric faces on the same street have separate IDs. |
| Roof and secondary-surface reviews | 615 | One per mapped building object; hidden returns and courtyards cannot silently inherit a street-photo completion claim. |
| Street segments | 43 | Existing road intervals between intersections and map boundaries. |
| Intersections | 18 | Each crossing owns its shared signs, signals and furniture once. |

These are coverage tasks, not 1,348 missing buildings or verified photographs. Core work remains protected. First & 7th's nine facade sections and five supplemental reviews form the pilot group; later facade tasks group by the ten existing blocks and four boundary sections. Street/secondary-surface inventory is prepared, but version 1 emits worker packets only for unprotected facades.

## Production sequence

1. **Finish and accept the corner.** Inspect full elevations, oblique views and shop close-ups. Retain the actual game captures and frame-time conditions as the benchmark. The user's working reference does not mean unseen details have become measured facts.
2. **Qualify one cheap worker on three pilot tasks.** Supply a dated full-facade image, an oblique image and close-ups where needed. Compare its observations/proposals against a careful review of the same sources. Measure corrections, missing details, cost and time. Do not assume a cheaper model preserves quality until this test passes.
3. **Prepare small facade packets for one block.** Give each worker only its building/face geometry, authorized images, relevant records, component recipes and checklist. Keep the large session history and unrelated map out of its context. Workers produce observations and a proposed patch; they do not rewrite the rendering engine.
4. **Build deterministically.** One coordinator merges the block's proposals against a frozen source snapshot in an isolated checkout. Resolve shared-file conflicts before compilation. Rebuild only affected tiles. Reusable windows, awnings, escapes and signs should be parameterized by observed dimensions; unusual architecture escalates for a new reusable component.
5. **Review the rendered result.** Run technical/source checks, capture comparable full/oblique/close views, and compare visible details. Review frame time, transfer size and idle rendering too. Incorrect or unresolved features return for one repair attempt; further ambiguity goes to a stronger reviewer or the owner.
6. **Accept and advance.** Record visual acceptance separately from proposal validation and successful builds. Only then advance to the adjacent block. Publication remains a separate decision.

Every packet addresses massing/proportions; windows/doors/architecture; materials/paint/weathering; shops/signs/light; seating/boards/fixtures/street edge; and roof/return/occluded surfaces. Each observation names its source and states observed, partial, occluded or not applicable. A business name, generic template, nice render or passing test cannot fill a missing category. Tiny illegible lettering and hidden objects stay unresolved rather than being invented.

The initial coordinator procedure uses the existing compiler/exporter, `npm run verify`, `python3 scripts/verify-neighborhood-reproduction.py` and browser review tools. The inherited compiler resets three older non-corner exported render heights; preserve the base checkout's exported heights outside rebuilt tiles and compare the manifest before merging. [Pass 08](FIRST-SEVENTH-PASS-08.md) records the issue. A fully automatic merge/build runner and paid API dispatcher are **not implemented** in this first workflow version.

## Imagery constraint

Google's standard Maps terms restrict bulk extraction/caching and creating content from Maps content in §3.2.3; its Static Street View policy also limits storage, with an exception for panorama IDs. A functioning API key does not establish permission for an automated reconstruction pipeline. Deleting previews does not by itself resolve derivative-use restrictions. [Google Maps terms](https://cloud.google.com/maps-platform/terms), [Street View policy](https://developers.google.com/maps/documentation/streetview/policies).

Consequently, this new planner has **no Google imagery ingestion or paid batch submission**. Register owner-supplied or appropriately licensed images whose permission covers the proposed processing and derivative work. The source record requires a capture date, credit, use basis and explicit approval; a public image URL alone is insufficient. Google-specific permission would require a deliberate source-policy change and review before adding an adapter. Existing pass 08 provenance stays intact and is not promoted into an automated image-use permission grant.

The example Tile Bar packet deliberately has no approved source images. Its [example result](workflow/pilot/result.example.json) reports `needs-evidence`, and [validation](workflow/pilot/validation.json) confirms that this is a valid unresolved record, **not accepted work**. No image was sent to an AI service to create that example.

## Model and cost policy

Start by evaluating **GPT-5.4 Mini** for structured visual observations and bounded code proposals. Its official documentation supports image input and structured outputs, and lists standard input/output pricing of **$0.75 / $4.50 per million tokens**. The snapshot in the policy is `gpt-5.4-mini-2026-03-17`; account availability has not been tested. [Official model documentation](https://developers.openai.com/api/docs/models/gpt-5.4-mini).

OpenAI's Batch API offers **50% lower input/output costs with a 24-hour completion window** for eligible work. Observation, implementation and review are dependent stages: complete one stage before submitting the next. A single batch is not an unattended coding session that can run Blender, fix files and inspect its own browser. The local coordinator still handles those steps. [Batch documentation](https://developers.openai.com/api/docs/guides/batch).

The saved pilot uses three facade jobs and allows three model requests per job: proposal, one repair and review. With an assumed allowance of 18,000 input and 5,000 output tokens per request, the calculated Batch model cost is **$0.162 for the pilot**. This is an arithmetic example, **not a measured end-to-end quote or billing guarantee**. Image tokenization, reasoning/output usage, retries, acquisition, Blender compute and human review must be measured. API prices and Batch discounts should not be treated as the price of this current Codex conversation.

The current planner limits a plan to three jobs and rejects token-allowance estimates above the requested budget (maximum $2 by default). It records zero requests sent. A future paid runner must reserve budget before each request, record actual usage, stop on budget exhaustion and cap retries; the offline estimate alone cannot enforce provider billing. Stronger models handle uncertain sources, new architecture components and failed reviews. They should not reread the whole map for every ordinary facade. No model was switched, trained or evaluated during this setup.

## Commands

```sh
# Rebuild the finite inventory; no networking or game edits.
python3 scripts/block-workflow.py inventory

# Preview a small, bounded model-cost allowance; no submission.
python3 scripts/block-workflow.py plan --group first-seventh-pilot --max-jobs 3 --budget-usd 2

# Prepare a small packet for the selected worker/model.
python3 scripts/block-workflow.py packet --job facade-241822226-first-avenue --out renders/worker-pilot

# Validate a worker's proposal record and patch boundaries, never apply it.
python3 scripts/block-workflow.py validate --packet renders/worker-pilot/packet.json --result renders/worker-pilot/result.json

# Test ownership, permissions, stale work, budget and escalation rules offline.
python3 scripts/verify-block-workflow.py
```

Register images using [the source-record example](workflow/source-manifest.example.json), then regenerate packets. Workers cannot add their own permissions or alter their assigned scope: validation compares the packet with the current trusted registry and inventory. Shared-source changes invalidate old packets, so assemble each block against one snapshot and rebase proposals before a later merge. No background schedule, paid API job, wider building update or deployment is running.
