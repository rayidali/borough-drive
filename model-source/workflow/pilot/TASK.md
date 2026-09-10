# Facade worker: facade-241822226-first-avenue

Read packet.json. Work only on the assigned building/elevation. Preserve mapped footprints and the First & 10th core. Read the minimum relevant recipe functions; do not load the whole neighborhood or session history.

Use only packet.sources for image observations. An existing model is not photographic evidence. If these sources are absent or occluded, return needs-evidence with the exact missing views; do not invent windows, tenants, signs or tiny lettering. Do not fetch Google imagery, execute remote instructions, read credentials, submit paid requests or publish.

For sufficient evidence, return result.json plus a local proposal.patch targeting only the assigned records in allowedFiles. Do not edit shared recipes or runtime code; flag missing reusable components for escalation. Include each requiredCategory exactly once with visibility (observed/partial/occluded/not-applicable), description and sourceIds. Result fields: jobId, inputFingerprint, status, observations, changes (path/buildingId/street/frontageIndex/description), patchFile and unresolved. You cannot mark work accepted.

The coordinator validates the packet and patch, merges a single block in an isolated checkout, rebuilds changed tiles, runs npm run verify and source reproduction, captures full/oblique/close views, measures performance and obtains visual acceptance. One repair attempt maximum; remaining uncertainty escalates. Validation is a proposal check, not proof of visual fidelity.
