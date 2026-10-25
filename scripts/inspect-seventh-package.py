#!/usr/bin/env python3
"""Read-only PCK v4 census for EV-001. Writes analysis JSON, never an export.

Only the observed unencrypted, non-sparse format is supported. Every directory
entry is bounded and MD5-checked, then SHA256-recorded; unexpected flags fail.
"""
import hashlib
import json
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "model-source/east-village-ev001"


def main():
    pack = ROOT / "dist/seventh/index.pck"
    data = pack.read_bytes()
    magic, version, major, minor, patch, flags = struct.unpack_from("<6I", data)
    assert magic == 0x43504447 and version == 4 and flags == 2
    base, directory = struct.unpack_from("<QQ", data, 24)
    count, = struct.unpack_from("<I", data, directory)
    cursor = directory + 4
    entries = []
    buildings = {str(b["id"]): b for b in json.loads((ROOT / "engine/first-seventh/assets/slice.json").read_text())["buildings"]}
    for _ in range(count):
        length, = struct.unpack_from("<I", data, cursor)
        cursor += 4
        name = data[cursor:cursor + length].rstrip(b"\0").decode("utf-8")
        cursor += length
        offset, size = struct.unpack_from("<QQ", data, cursor)
        checksum = data[cursor + 16:cursor + 32].hex()
        file_flags, = struct.unpack_from("<I", data, cursor + 32)
        cursor += 36
        assert file_flags == 0 and offset + base + size <= directory
        body = data[base + offset:base + offset + size]
        assert hashlib.md5(body).hexdigest() == checksum, name
        match = re.search(r"building-(-?\d+)\.glb-.*\.scn$", name)
        building = buildings[match[1]] if match else None
        category = "building-scenes" if building else "surface-textures" if name.endswith(".ctex") else "audio" if name.endswith(".sample") else "fonts" if name.endswith(".fontdata") else "metadata-code-other"
        entry = {"path": name, "offsetAbsolute": base + offset, "bytes": size, "md5": checksum, "sha256": hashlib.sha256(body).hexdigest(), "category": category}
        if building:
            entry.update({"buildingId": building["id"], "address": building["address"], "runtimePosition": building["position"], "runtimeBox": building["box"], "glbSha256": building["sha256"], "sourceAsset": building["asset"]})
        entries.append(entry)
    assert cursor == len(data) and len({e["path"] for e in entries}) == count
    models = [e for e in entries if e["category"] == "building-scenes"]
    assert {str(e["buildingId"]) for e in models} == set(buildings)
    categories = {}
    for e in entries:
        group = categories.setdefault(e["category"], {"files": 0, "bytes": 0})
        group["files"] += 1
        group["bytes"] += e["bytes"]
    report = {"date": "2026-10-12", "mode": "read-only package census", "pack": str(pack.relative_to(ROOT)), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "format": version, "engineVersion": [major, minor, patch], "flags": flags, "entryCount": count, "payloadBytes": sum(e["bytes"] for e in entries), "directoryAlignmentOverheadBytes": len(data) - sum(e["bytes"] for e in entries), "categories": categories, "allEntryChecksumsPass": True, "entries": entries}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "package-census.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "entries"}, indent=2))


if __name__ == "__main__":
    main()
