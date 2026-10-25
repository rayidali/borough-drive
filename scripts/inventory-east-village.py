#!/usr/bin/env python3
"""Reproduce EV-000 planning artifacts offline; never modifies runtime assets.

Requires the locally available shapely and matplotlib Python packages. Source
queries are frozen separately; do not refetch them during normal reproduction.
"""
import collections
import csv
import hashlib
import json
import math
import os
import re
from pathlib import Path

from shapely.geometry import LineString, Point, Polygon, box, mapping, shape
from shapely.ops import substring, transform, unary_union

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "model-source/east-village-ev000"
SRC = ROOT / "source-data/east-village-ev000"


def read(path):
    return json.loads(path.read_text())


def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + "\n")


def csv_write(name, rows):
    assert rows
    with (OUT / name).open("w") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    neighborhood = read(ROOT / "dist/reconstruction/neighborhood.json")
    plan = read(OUT / "plan-input.json")
    spec = read(OUT / "boundary-spec.json")
    for path, expected in plan["inventoryInputs"].items():
        assert digest(ROOT / path) == expected, "Baseline changed; do not overwrite the frozen EV-000 inventory: " + path
    manifest = read(SRC / "manifest.json")
    for name, source in manifest["sources"].items():
        assert digest(SRC / (name + ".geojson")) == source["sha256"], "Source snapshot hash mismatch: " + name
    origin = neighborhood["origin"]
    angle = math.radians(neighborhood["axis"]["avenueBearing"])
    scale_x = 111320 * math.cos(math.radians(origin["lat"]))

    def project(x, y, unused=None):
        e = (x - origin["lon"]) * scale_x
        n = (y - origin["lat"]) * 111320
        return e * math.cos(angle) - n * math.sin(angle), -e * math.sin(angle) - n * math.cos(angle)

    def unproject(x, z, unused=None):
        e = x * math.cos(angle) - z * math.sin(angle)
        n = -x * math.sin(angle) - z * math.cos(angle)
        return origin["lon"] + e / scale_x, origin["lat"] + n / 111320

    datasets = {}
    for kind in ("roads", "lots", "buildings", "shoreline"):
        datasets[kind] = [(f["properties"], transform(project, shape(f["geometry"]))) for f in read(SRC / (kind + ".geojson"))["features"]]
    roads = {p["PHYSICALID"]: (p, g) for p, g in datasets["roads"]}
    assert len(roads) == len(datasets["roads"])
    connections = []

    def chain(ids, start):
        coords = [start]
        for physical_id in ids:
            geometry = roads[physical_id][1]
            parts = [geometry] if geometry.geom_type == "LineString" else list(geometry.geoms)
            while parts:
                part = min(parts, key=lambda g: min(Point(coords[-1]).distance(Point(g.coords[0])), Point(coords[-1]).distance(Point(g.coords[-1]))))
                parts.remove(part)
                points = list(part.coords)
                if Point(coords[-1]).distance(Point(points[-1])) < Point(coords[-1]).distance(Point(points[0])):
                    points.reverse()
                gap = Point(coords[-1]).distance(Point(points[0]))
                if gap > 0.1:
                    connections.append({"beforePhysicalId": physical_id, "lengthMetres": round(gap, 3), "fromLocalXZ": coords[-1], "toLocalXZ": points[0], "meaning": "planning boundary join, not an inferred road connection"})
                coords.extend(points)
        return LineString(coords)

    sw = list(roads[159630][1].coords)[0]
    west = chain(spec["westPhysicalIdsSouthToNorth"], sw)
    north = chain(spec["northPhysicalIdsWestToEast"], west.coords[-1])
    south = chain(spec["southPhysicalIdsWestToEast"], sw)
    shore = next(g for p, g in datasets["shoreline"] if p["OBJECTID"] == spec["shorelineObjectId"])

    def shore_end(line):
        x, z = line.coords[-1]
        point = shore.intersection(LineString([(x, z), (1600, z)]))
        assert point.geom_type == "Point", point.wkt
        return point

    ne, se = shore_end(north), shore_end(south)
    east = substring(shore, shore.project(ne), shore.project(se))
    ring = []
    for point in list(west.coords) + list(north.coords)[1:] + list(east.coords) + list(south.coords)[::-1]:
        if not ring or math.dist(point, ring[-1]) > 1e-7:
            ring.append(point)
    boundary = Polygon(ring)
    assert boundary.is_valid, "Boundary self-intersection"
    assert boundary.area > 1000000
    write("boundary.geojson", {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"id": "EV-BOUNDARY-2026-10-12", "kind": "planning boundary", "shorelineImageryDate": "2022-03-18", "notSurveyed": True}, "geometry": mapping(transform(unproject, boundary))}]})
    write("boundary-joins.json", connections)

    extents = {"01": (-229, -158, 214, 228), "02": (-229, -1000, 214, -158), "03": (-1000, -1000, -229, 1200), "04": (-229, 228, 214, 1200), "05": (214, 0, 438, 228), "06": (214, -1000, 895, 0), "07": (438, 0, 895, 228), "08": (214, 228, 895, 1200), "09": (895, -1000, 1800, 1200)}
    phases = {key: boundary.intersection(box(*bounds)) for key, bounds in extents.items()}
    assert boundary.symmetric_difference(unary_union(list(phases.values()))).area < 0.01
    assert abs(sum(g.area for g in phases.values()) - boundary.area) < 0.01
    write("phases.geojson", {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"phase": key, "role": "parcel routing only; exact street faces can belong to a neighboring corridor phase"}, "geometry": mapping(transform(unproject, value))} for key, value in phases.items()]})

    def overlaps(geometry):
        weights = {key: geometry.intersection(g).area for key, g in phases.items()}
        return max(weights, key=weights.get), [key for key, area in weights.items() if area > 1]

    lot_rows, lot_geometries = [], []
    for p, g in datasets["lots"]:
        g = g if g.is_valid else g.buffer(0)
        cut = g.intersection(boundary)
        if cut.area <= 1:
            continue
        owner, touched = overlaps(g)
        bbl = str(int(p["BBL"]))
        lot_rows.append({"lotId": "BBL:" + bbl, "bbl": bbl, "address": p["Address"], "phaseOwner": owner, "touchedPhases": ";".join(touched), "boundaryClipped": not boundary.covers(g), "inScopeAreaFraction": round(cut.area / g.area, 6), "inScopeApproxSquareMetres": round(cut.area, 1), "landUse": p["LandUse"], "buildingClass": p["BldgClass"], "reportedBuildings": p["NumBldgs"], "version": p["Version"], "ownershipState": "parcel routing; exact face/site children require packet inventory"})
        lot_geometries.append((bbl, owner, cut))
    lot_rows.sort(key=lambda r: r["bbl"])
    assert len({r["bbl"] for r in lot_rows}) == len(lot_rows)
    csv_write("lots.csv", lot_rows)

    local_by_bin = collections.defaultdict(list)
    for b in neighborhood["buildings"]:
        if b.get("bin"):
            local_by_bin[str(b["bin"])].append(b["id"])
    building_rows = []
    for p, g in datasets["buildings"]:
        g = g if g.is_valid else g.buffer(0)
        cut = g.intersection(boundary)
        if cut.area <= 1:
            continue
        owner, touched = overlaps(g)
        building_rows.append({"sourceId": "OTI:" + str(p["DOITT_ID"]), "bin": p["BIN"], "baseBbl": p["BASE_BBL"], "mapplutoBbl": p["MAPPLUTO_BBL"], "phaseOwner": owner, "touchedPhases": ";".join(touched), "boundaryClipped": not boundary.covers(g), "inScopeAreaFraction": round(cut.area / g.area, 6), "legacyBuildingIdsByBIN": ";".join(map(str, local_by_bin[str(p["BIN"])])), "featureCode": p["FEATURE_CODE"], "ownershipState": "footprint identity only; no facade, business, visual or current-condition acceptance"})
    building_rows.sort(key=lambda r: r["sourceId"])
    assert len({r["sourceId"] for r in building_rows}) == len(building_rows)
    csv_write("buildings.csv", building_rows)

    # Each roadmap row has one geographic owner. Source road references may be
    # shared; the road registry below gives the physical feature one edit owner.
    z_at = {0: 790, 1: 699, 2: 616, 3: 533, 4: 455, 5: 379, 6: 301, 7: 228, 8: 150, 9: 73, 10: 0, 11: -77, 12: -158, 13: -240, 14: -328}
    x_at = {"Second Avenue": -229, "First Avenue": 0, "Avenue A": 214, "Avenue B": 438, "Avenue C": 667, "Avenue D": 895}

    def street_z(value):
        if "Houston" in value:
            return z_at[0]
        if "Marks" in value:
            return z_at[8]
        return z_at[int(re.search(r"\d+", value).group())]

    def street_x(value):
        return next((x for name, x in x_at.items() if value.startswith(name)), -530)

    unit_geometries, unit_sources = {}, {}
    for u in plan["units"]:
        uid, street = u["id"], u["street"]
        names, region = [], boundary
        if re.match(r"East \d+", street) or street == "St. Marks Place":
            z = street_z(street)
            names = ["ST MARKS PL"] if "Marks" in street else ["E " + str(next(k for k, v in z_at.items() if v == z)) + " ST"]
            a, b = sorted([street_x(u["start"]), street_x(u["end"])])
            region = box(a - 4, z - 12, b + 4, z + 12)
        elif street in x_at:
            x = x_at[street]
            a, b = sorted([street_z(u["start"]), street_z(u["end"])])
            names = [{"First Avenue": "1 AVE", "Second Avenue": "2 AVE"}.get(street, street.replace("Avenue", "AVE"))]
            region = box(x - 8, a - 4, x + 8, b + 4)
        elif street == "Bowery / Cooper Square / Third Avenue":
            a, b = sorted([street_z(u["start"]), street_z(u["end"])])
            names = ["BOWERY", "COOPER SQ", "3 AVE"]
            region = box(-540, a - 4, -300, b + 4)
        elif "Houston" in street:
            names = ["E HOUSTON ST"]
            a = street_x(u["start"])
            b = 1500 if u["phase"] == "09" else street_x(u["end"])
            region = box(a - 4, 500, b + 4, 850)
        elif uid == "03-STUY":
            names = ["STUYVESANT ST"]
        elif uid == "03-COOPER":
            region = box(-526, 145, -435, 380)
        elif uid == "04-E05-1A":
            region = box(0, 310, 214, 445)
        elif uid.startswith("05-TSP"):
            west_half = uid.endswith(("SW", "NW"))
            north_half = uid.endswith(("NW", "NE"))
            region = box(214 if west_half else 326, 0 if north_half else 114, 326 if west_half else 438, 114 if north_half else 228)
        elif uid.startswith("09-"):
            suffix = uid[-1]
            a, b = {"S": (301, 850), "M": (0, 301), "N": (-400, 0)}[suffix]
            region = box(895, a, 1500, b)
        else:
            raise AssertionError("No routing region for " + uid)
        matches = []
        for p, g in datasets["roads"]:
            if names and " ".join(p["FULL_STREET_NAME"].split()) not in names:
                continue
            clipped = g.intersection(region).intersection(boundary.buffer(35))
            if clipped.length > 5:
                matches.append((p["PHYSICALID"], clipped))
        unit_sources[uid] = [pid for pid, _ in matches]
        unit_geometries[uid] = unary_union([g for _, g in matches]) if names and matches else region.intersection(boundary)
        if not matches and names:
            unit_geometries[uid] = region.intersection(boundary)

    # Add mapped Szold Place to the two real connections, never an invented
    # extension of Eleventh through Dry Dock. Avenue D north of Thirteenth is
    # grouped into the Fourteenth utility-edge unit, not omitted from the map.
    for uid, physical_ids in {"06-E11-CD": [103211], "06-E12-CD": [103212], "06-E14-CD": [2748]}.items():
        unit_sources[uid] = sorted(set(unit_sources[uid] + physical_ids))

    units_by_id = {u["id"]: u for u in plan["units"]}
    boundary_names = {"E HOUSTON ST", "E 14 ST", "BOWERY", "COOPER SQ", "3 AVE"}
    road_rows, road_features = [], []
    for p, g in datasets["roads"]:
        name = " ".join(p["FULL_STREET_NAME"].split())
        clipped = g.intersection(boundary)
        if clipped.length <= 1:
            if name not in boundary_names or g.distance(boundary) > 35:
                continue
            clipped = g.intersection(boundary.buffer(35))
            if clipped.length <= 5:
                continue
        middle = clipped.interpolate(0.5, normalized=True)
        phase = min(phases, key=lambda key: middle.distance(phases[key]))
        candidates = [uid for uid, ids in unit_sources.items() if p["PHYSICALID"] in ids]
        # Prefer a specifically named corridor over a large site's catchment.
        named = [uid for uid in candidates if units_by_id[uid]["kind"] not in ("park interior", "housing/utility site", "infrastructure", "waterfront landscape", "plaza and landmark", "site; no through-road assumed")]
        if named:
            candidates = named
        if candidates:
            owner = min(candidates, key=lambda uid: (middle.distance(unit_geometries[uid]), uid))
        else:
            candidates = [uid for uid, u in units_by_id.items() if u["phase"] == phase]
            owner = min(candidates, key=lambda uid: (middle.distance(unit_geometries[uid]), uid))
        x, z = middle.coords[0]
        if x > 895 and name != "E HOUSTON ST":
            band = "N" if z < 0 else "M" if z < 301 else "S"
            if "ROOSEVELT" in name or "OVER FDR" in name or "OPAS" in name or p["RW_TYPE"] in (2, 3, 9):
                owner = "09-FDR" + band
            elif "ESPL" in name or x > 1160 + z * 0.30:
                owner = "09-PARK" + band
            else:
                owner = "09-SITE" + band
        if p["PHYSICALID"] in (103211, 103212, 2748):
            owner = {103211: "06-E11-CD", 103212: "06-E12-CD", 2748: "06-E14-CD"}[p["PHYSICALID"]]
        kind = "mapped street; access unverified"
        if p["STATUS"] != "2" or p["RW_TYPE"] == 12:
            kind = "mapped-only or unbuilt; no inferred road"
        elif p["TRAFDIR"] == "NV" or p["RW_TYPE"] in (5, 6, 7):
            kind = "non-vehicular/path"
        elif p["RW_TYPE"] in (2, 3, 4, 9, 13):
            kind = "highway/structure/connector; gameplay not assigned"
        row = {"roadId": "CSCL:" + str(p["PHYSICALID"]), "name": name, "owner": owner, "phase": units_by_id[owner]["phase"], "statusCode": p["STATUS"], "rightOfWayType": p["RW_TYPE"], "trafficDirection": p["TRAFDIR"], "classification": kind, "leftBlockfaceId": p["L_BLOCKFACEID"], "rightBlockfaceId": p["R_BLOCKFACEID"], "scope": "interior/boundary crossing" if g.intersection(boundary).length > 1 else "boundary carriageway context", "currentAccess": "not verified by centerline inventory"}
        road_rows.append(row)
        road_features.append({"type": "Feature", "properties": row, "geometry": mapping(transform(unproject, clipped))})
    road_rows.sort(key=lambda r: r["roadId"])
    csv_write("roads.csv", road_rows)
    write("roads.geojson", {"type": "FeatureCollection", "features": road_features})
    unit_rows = []
    for u in plan["units"]:
        assigned = [r["roadId"] for r in road_rows if r["owner"] == u["id"]]
        unit_rows.append({"unitId": u["id"], "phaseOwner": u["phase"], "kind": u["kind"], "street": u["street"], "start": u["start"], "end": u["end"], "sourceRoadReferences": ";".join("CSCL:" + str(v) for v in sorted(unit_sources[u["id"]])), "ownedRoadIds": ";".join(assigned), "state": "inventory only; see exception register before authoring"})
    csv_write("units.csv", unit_rows)
    # Keep open/institutional/utility and large/multi-building lots visible in
    # the work list even when they have few or no street-facing buildings.
    sites = []
    geom_by_bbl = {bbl: g for bbl, _, g in lot_geometries}
    specific_site_owners = {"1004030001": "05-TSPNW", "1004320001": "04-E05-1A", "1003820100": "06-E11-CD", "1003820001": "06-E12-CD", "1003800050": "06-E11-CD", "1003810038": "06-E12-CD", "1003870001": "08-E05-BC", "1003950009": "06-E13-BC", "1003950022": "06-E13-BC", "1003830001": "06-E14-CD"}
    for lot in lot_rows:
        if lot["landUse"] not in ("07", "08", "09") and (lot["reportedBuildings"] or 0) < 3 and lot["inScopeApproxSquareMetres"] < 3000:
            continue
        bbl = lot["bbl"]
        point = geom_by_bbl[bbl].representative_point()
        phase = lot["phaseOwner"]
        choices = [uid for uid, u in units_by_id.items() if u["phase"] == phase]
        owner = specific_site_owners.get(bbl) or min(choices, key=lambda uid: (point.distance(unit_geometries[uid]), uid))
        if phase == "09":
            z = point.y
            owner = ("09-PARK" if bbl == "1003160200" else "09-SITE") + ("N" if z < 0 else "M" if z < 301 else "S")
        sites.append({"siteId": lot["lotId"], "mappedAddress": lot["address"], "landUseCode": lot["landUse"], "buildingClass": lot["buildingClass"], "phase": phase, "inventoryCoordinator": owner, "scopeAreaApproxSquareMetres": lot["inScopeApproxSquareMetres"], "state": "coordination owner only; divide large parcels into explicit feature/face sections before authoring", "perimeterRule": "existing street-face packets retain ownership; interior/secondary/roof features need named children; no hidden detail inferred"})
    csv_write("sites.csv", sites)

    # Exact protected IDs remain in their original namespace. Preserve all
    # current models by default; acceptance exists only in the dated reports.
    slice_data = read(ROOT / "engine/first-seventh/assets/slice.json")
    details = read(ROOT / "model-source/storefront-details.json")
    buildings = {str(b["id"]): b for b in neighborhood["buildings"]}
    protected_faces = {r["faceId"] for r in slice_data["streetReviewFrontages"]}
    for record in slice_data["reviewFrontages"]:
        b = buildings[str(record["id"])]
        for i, face in enumerate(b["frontages"]):
            if face == record["frontage"]:
                protected_faces.add(str(b["id"]) + ":" + str(i))
    core_ids = sorted(b["id"] for b in neighborhood["buildings"] if b.get("core"))
    for bid in core_ids:
        protected_faces.update(str(bid) + ":" + str(i) for i in range(len(buildings[str(bid)]["frontages"])))
    protected_runtime = sorted(b["id"] for b in slice_data["buildings"])
    protected_faces.update(str(bid) + ":" + str(i) for bid in protected_runtime for i in range(len(buildings[str(bid)]["frontages"])))
    write("protected.json", {"policy": "Preserve current runtime objects/core by default, including context; this list does not imply all surfaces are accepted. A later exact packet may explicitly transfer an unreviewed context face. No protected geometry is editable in EV-000.", "runtimeBuildingIds": protected_runtime, "coreBuildingIds": core_ids, "faceIds": sorted(protected_faces), "revision09ExplicitFaces": sorted(r["faceId"] for r in details["firstStmarksEngine"]["elevations"])})
    packets, seen_faces = [], set()
    for packet in plan["firstPackets"]:
        faces = []
        for fid in packet["faceIds"]:
            assert fid not in seen_faces and fid not in protected_faces, fid
            seen_faces.add(fid)
            bid, face_index = fid.split(":")
            b = buildings[bid]
            face = b["frontages"][int(face_index)]
            faces.append({"faceId": fid, "buildingId": b["id"], "address": b["address"], "sourceFace": face, "bin": b.get("bin"), "municipalReferences": [{k: r.get(k) for k in ("bin", "doittId", "bbl", "matchBasis")} for r in b.get("municipalReferences", [])], "geometryOwner": packet["id"], "evidenceState": "needs dated property/business inspection"})
        packets.append({"id": packet["id"], "parent": packet["parent"], "faces": faces, "allowlistState": "exact legacy face records; future engine file allowlist must be established by EV-001/packet start", "massAndRoofOwners": sorted({f["buildingId"] for f in faces}), "editState": "not started"})
    mass_owners = collections.defaultdict(list)
    for p in packets:
        for bid in p["massAndRoofOwners"]:
            mass_owners[bid].append(p["id"])
    assert all(len(owners) == 1 for owners in mass_owners.values()), dict(mass_owners)
    write("next-packets.json", packets)

    # Shared intersection fixtures receive one stable owner from incident roads.
    nodes = collections.defaultdict(set)
    for f in road_features:
        g = transform(project, shape(f["geometry"]))
        parts = [g] if g.geom_type == "LineString" else [p for p in getattr(g, "geoms", []) if p.geom_type == "LineString"]
        for part in parts:
            for coord in (part.coords[0], part.coords[-1]):
                nodes[(round(coord[0], 2), round(coord[1], 2))].add(f["properties"]["roadId"])
    road_by_id = {r["roadId"]: r for r in road_rows}
    intersections = []
    for (x, z), incident in sorted(nodes.items()):
        if len(incident) < 2:
            continue
        owners = sorted({road_by_id[r]["owner"] for r in incident})
        intersections.append({"nodeId": "EV-NODE:" + str(x) + ":" + str(z), "localX": x, "localZ": z, "incidentRoads": ";".join(sorted(incident)), "fixtureOwner": owners[0], "otherUnitReferences": ";".join(owners[1:]), "state": "mapped shared endpoint only; grade/access/actual fixtures require evidence"})
    csv_write("intersections.csv", intersections)

    hashes = {str(path.relative_to(ROOT)): digest(path) for path in [ROOT / "dist/reconstruction/neighborhood.json", ROOT / "engine/first-seventh/assets/slice.json", ROOT / "model-source/storefront-details.json", ROOT / "dist/seventh/index.pck"]}
    summary = {"session": "EV-000", "date": "2026-10-12", "mode": "inventory only", "boundaryAreaApproxKm2": round(boundary.area / 1e6, 3), "counts": {"lotsIntersectingOver1SquareMetre": len(lot_rows), "buildingFootprintsIntersectingOver1SquareMetre": len(building_rows), "physicalRoadFeaturesIncludingBoundaryContext": len(road_rows), "sharedEndpointNodes": len(intersections), "roadmapUnits": len(unit_rows), "futurePropertyPackets": len(packets), "exactFutureFaces": len(seen_faces), "protectedRuntimeBuildings": len(protected_runtime), "protectedCoreBuildings": len(core_ids), "protectedMappedFacesIncludingContext": len(protected_faces)}, "lotsByPhase": dict(sorted(collections.Counter(r["phaseOwner"] for r in lot_rows).items())), "footprintsByPhase": dict(sorted(collections.Counter(r["phaseOwner"] for r in building_rows).items())), "roadClassCounts": dict(collections.Counter(r["classification"] for r in road_rows)), "limitations": ["Counts are snapshot GIS feature counts, not businesses, facade counts, current occupancy or visual acceptance.", "Boundary-clipped sites retain their entire identity but only the in-scope portion is authorized; outside portions remain context.", "Parcel/footprint phase routing uses greatest overlap; exact frontage packets override it. Face enumeration outside the first nine packets remains future per-corridor work.", "Municipal centerlines do not establish current public access. Dated waterfront/utility/site evidence is required before rendering roads as drivable.", "2022 shoreline imagery is a planning edge, not proof of 2026 flood-work conditions.", "Only coincident mapped endpoints are joined. Grade-separated crossings are not assumed to connect.", "The initial project-time estimate remains provisional until actual detailed storefront pilot sessions are timed."], "preservedInputHashes": hashes, "nextSession": "EV-001"}
    summary["counts"]["specialSiteCoordinationRecords"] = len(sites)
    write("summary.json", summary)
    write("validation.json", {"boundaryValid": boundary.is_valid, "phasePartitionGapOrOverlapSquareMetres": round(boundary.symmetric_difference(unary_union(list(phases.values()))).area, 8), "uniqueLotIds": len(lot_rows), "uniqueFootprintIds": len(building_rows), "uniqueRoadIds": len({r["roadId"] for r in road_rows}), "allRoadOwnersExist": all(r["owner"] in units_by_id for r in road_rows), "all193UnitsHaveOnePhase": len(unit_rows) == 193 and all(r["phaseOwner"] in phases or r["phaseOwner"] == "00" for r in unit_rows), "all53FacesUniqueAndExcludeProtected": len(seen_faces) == 53, "allFutureMassesHaveOneOwner": all(len(v) == 1 for v in mass_owners.values()), "boundaryJoinsOverPointOneMetre": len(connections), "largestBoundaryJoinMetres": max((r["lengthMetres"] for r in connections), default=0), "scope": "offline geometry/identity validation; no visual/gameplay/performance tests"})

    os.environ.setdefault("MPLCONFIGDIR", "/tmp/borough-drive-matplotlib")
    os.environ.setdefault("XDG_CACHE_HOME", "/tmp/borough-drive-cache")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    colors = {"01": "#df805c", "02": "#e3b46f", "03": "#9b97c9", "04": "#d597b0", "05": "#83b88d", "06": "#85b8cf", "07": "#6fa6a2", "08": "#c5b271", "09": "#90a9bb"}
    fig, ax = plt.subplots(figsize=(12, 10), facecolor="#f5f1e8")
    ax.set_facecolor("#dfeaf0")
    for key, g in phases.items():
        polygons = [g] if g.geom_type == "Polygon" else list(g.geoms)
        for poly in polygons:
            x, y = poly.exterior.xy
            ax.fill(x, y, color=colors[key], alpha=0.50)
    for _, _, g in lot_geometries:
        polys = [g] if g.geom_type == "Polygon" else [v for v in getattr(g, "geoms", []) if v.geom_type == "Polygon"]
        for poly in polys:
            x, y = poly.exterior.xy
            ax.plot(x, y, color="#4c5457", linewidth=0.24, alpha=0.5)
    for f in road_features:
        g = transform(project, shape(f["geometry"]))
        parts = [g] if g.geom_type == "LineString" else [p for p in getattr(g, "geoms", []) if p.geom_type == "LineString"]
        for part in parts:
            x, y = part.xy
            ax.plot(x, y, color="#faf8f1", linewidth=1.5, linestyle="--" if f["properties"]["trafficDirection"] == "NV" else "-")
    x, y = boundary.exterior.xy
    ax.plot(x, y, color="#263f48", linewidth=2)
    for key, (x, z) in {"01": (-105, 12), "02": (-100, -270), "03": (-330, 410), "04": (-105, 480), "05": (326, 114), "06": (550, -200), "07": (630, 118), "08": (550, 455), "09": (1100, 250)}.items():
        ax.text(x, z, key, ha="center", va="center", fontsize=18, weight="bold", color="#273c44", bbox={"facecolor": "#faf8f0", "edgecolor": "none", "alpha": .8, "pad": 3})
    for x, label in [(-229, "Second"), (0, "First"), (214, "Ave A"), (438, "Ave B"), (667, "Ave C"), (895, "Ave D")]:
        ax.text(x, -380, label, ha="center", fontsize=9, color="#263f48")
    for z, label in [(-328, "14th"), (-158, "12th"), (0, "10th"), (150, "St. Marks / 8th"), (228, "7th"), (455, "4th")]:
        ax.text(-560, z, label, ha="right", va="center", fontsize=9)
    ax.text(350, 815, "Houston — inward side", ha="center", fontsize=10)
    ax.text(1340, 130, "East River", rotation=90, fontsize=12, color="#3d6374")
    ax.set_title("East Village • EV-000 inventory\nNine planning phases, municipal lots and real mapped connections", loc="left", fontsize=16, pad=22)
    ax.text(0, -0.065, "October 12, 2026  ·  NYC OTI centerlines/buildings; DCP MapPLUTO 26v2; 2022 shoreline\nStreet-aligned local frame (up follows the avenues, not true north). Dashed = non-vehicular. Access/conditions need dated review.", transform=ax.transAxes, fontsize=9)
    ax.set_aspect("equal")
    ax.set_xlim(-730, 1480)
    ax.set_ylim(870, -420)
    ax.axis("off")
    fig.savefig(OUT / "inventory-map.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
