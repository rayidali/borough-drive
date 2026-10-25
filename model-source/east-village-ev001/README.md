# EV-001 evidence and reproduction

<!-- current-project-status -->
> **Current status:** The [project handoff](../../CODEX-HANDOFF.md) governs current scope, publication and next work. This file retains its dated observations, evidence or specialist instructions. See [browser scaling](../../docs/BROWSER-SCALING.md) for the current loading/rendering work; older model counts and paused states describe their original checkpoints.
<!-- /current-project-status -->

[Design and next-session packet](../EAST-VILLAGE-EV001.md) · [exact asset/area plan](loading-design.json).

These files inspect the existing export; none is a runtime loader. `package-census.json` records all 493 PCK entries and checksums. `native-resource-probe.json` records dependencies for all 203 building scenes and three native relocation/signature checks. `probe-notes.json` preserves diagnostic limits. `validation.json` binds inputs and records runtime/source/private-file preservation. The 203-item `loading-design.json` is a proposed manifest/ownership specification, not an exported browser manifest.

From the repository root, regenerate the read-only census:

```sh
python3 scripts/inspect-seventh-package.py
```

Run the native probe in an empty scratch project, with the repository's installed Godot 4.7.2. It mounts the existing pack only in that scratch process, copies three scene files to scratch, loads and compares them, deletes those three copies and writes a report. It does not run the game or import/export its project:

```sh
BOROUGH_ROOT="$PWD"
EV001_SCRATCH="$(mktemp -d /tmp/borough-ev001.XXXXXX)"
printf 'config_version=5\n' > "$EV001_SCRATCH/project.godot"
"$BOROUGH_ROOT/.tools/godot/Godot.app/Contents/MacOS/Godot" \
  --headless --path "$EV001_SCRATCH" --log-file "$EV001_SCRATCH/probe.log" \
  --script "$BOROUGH_ROOT/model-source/east-village-ev001/probe-resources.gd" -- \
  "$BOROUGH_ROOT/dist/seventh/index.pck" \
  "$BOROUGH_ROOT/model-source/east-village-ev001/package-census.json" \
  "$EV001_SCRATCH/native-resource-probe.json" "$EV001_SCRATCH/loose"
```

Inspect the log and report before replacing durable evidence. Assertions must compare nonempty mesh/LOD/material signatures; no errors may be mistaken for an empty matching result. The final recorded run passed those checks. An earlier invalid probe used a nonexistent LOD accessor and was discarded; the corrected probe inspects the pinned engine's stored `_surfaces` data. This internal inspection API is not a proposed runtime dependency.

The sandboxed native run reported an unused user-data directory creation failure and an OS certificate-store warning. It made no HTTP request; no permission escalation was required for its scratch-file/resource inspection. Reproduction may produce different OS diagnostics. Native weak-reference expiration does not demonstrate GPU release, HTTP loading or single-threaded browser performance. Do not rerun a game export to reproduce these evidence files.

Primary technical sources and their limits are linked beside the decisions in the design report. Upstream `master` source consulted on October 12 explains APIs/implementation; installed-engine observations remain separately pinned by version/hash in the native result.
