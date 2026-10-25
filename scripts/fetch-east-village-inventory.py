#!/usr/bin/env python3
"""Explicit, bounded public map download for EV-000. Never run at game build time.

No credentials, imagery, ownership records or paid endpoints. Original geometry
is retained; inventory processing is separate from runtime reconstruction.
"""
import datetime
import hashlib
import json
from pathlib import Path
import ssl
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-data/east-village-ev000"
BBOX = [-73.998, 40.716, -73.967, 40.738]
LAYERS = {
    "roads": ("https://services6.arcgis.com/yG5s3afENB5iO9fj/arcgis/rest/services/Centerline_view/FeatureServer/0", "OBJECTID,PHYSICALID,FULL_STREET_NAME,STREET_NAME,STNAME_LABEL,STATUS,TRAFDIR,RW_TYPE,STREETWIDTH,FROM_LEVEL_CODE,TO_LEVEL_CODE,L_BLOCKFACEID,R_BLOCKFACEID,L_LOW_HN,L_HIGH_HN,R_LOW_HN,R_HIGH_HN,MODIFIED_DATE"),
    "buildings": ("https://services6.arcgis.com/yG5s3afENB5iO9fj/arcgis/rest/services/BUILDING_view/FeatureServer/0", "OBJECTID,DOITT_ID,BIN,BASE_BBL,MAPPLUTO_BBL,FEATURE_CODE,HEIGHT_ROOF,GROUND_ELEVATION,CONSTRUCTION_YEAR,LAST_EDITED_DATE"),
    "lots": ("https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/ArcGIS/rest/services/MAPPLUTO/FeatureServer/0", "OBJECTID,BBL,Block,Lot,Address,BldgClass,LandUse,NumBldgs,NumFloors,YearBuilt,Version,Landmark,HistDist"),
    "shoreline": ("https://services6.arcgis.com/yG5s3afENB5iO9fj/ArcGIS/rest/services/Shoreline_2022/FeatureServer/21", "OBJECTID,SOURCE_ID,FEATURE_CODE,SUB_FEATURE_CODE,STATUS"),
}


def get(url, params):
    request_url = url + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(request_url, context=ssl.create_default_context(cafile="/etc/ssl/cert.pem"), timeout=90) as response:
        data = json.load(response)
    if "error" in data:
        raise RuntimeError(data["error"])
    return data


def main():
    if (OUT / "manifest.json").exists():
        raise SystemExit("EV-000 snapshot already exists. Preserve it; a later acquisition needs a new dated destination.")
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {"retrievedUTC": datetime.datetime.now(datetime.timezone.utc).isoformat(), "bboxWGS84": BBOX, "purpose": "EV-000 inventory only; selected public geometry/identity fields; not current visual or access evidence", "sources": {}}
    for name, (url, fields) in LAYERS.items():
        metadata = get(url, {"f": "json"})
        (OUT / (name + "-metadata.json")).write_text(json.dumps(metadata, indent=2) + "\n")
        spatial = {"where": "1=1", "geometry": ",".join(map(str, BBOX)), "geometryType": "esriGeometryEnvelope", "inSR": 4326, "spatialRel": "esriSpatialRelIntersects"}
        ids = get(url + "/query", {**spatial, "returnIdsOnly": "true", "f": "json"})["objectIds"] or []
        ids = sorted(ids)
        features = []
        for start in range(0, len(ids), 80):
            page = get(url + "/query", {"objectIds": ",".join(map(str, ids[start:start + 80])), "outFields": fields, "outSR": 4326, "returnGeometry": "true", "f": "geojson"})
            if page.get("exceededTransferLimit") or page.get("properties", {}).get("exceededTransferLimit"):
                raise RuntimeError("Truncated page: " + name)
            features.extend(page["features"])
        got = [f["properties"]["OBJECTID"] for f in features]
        assert sorted(got) == ids, (name, "Missing or duplicate IDs")
        path = OUT / (name + ".geojson")
        path.write_text(json.dumps({"type": "FeatureCollection", "features": sorted(features, key=lambda f: f["properties"]["OBJECTID"])}, separators=(",", ":")) + "\n")
        manifest["sources"][name] = {"url": url, "query": spatial, "outFields": fields, "featureCount": len(ids), "idPagesVerified": True, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "serviceEditingInfo": metadata.get("editingInfo"), "copyright": metadata.get("copyrightText")}
        print(name, len(features), flush=True)
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
