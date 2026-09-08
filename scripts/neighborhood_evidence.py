"""Apply checked-in municipal evidence without network access or extra packages."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def apply_geography(buildings, point, streets, extent):
    corrections = json.loads((ROOT/'model-source/geography-corrections.json').read_text())
    source = json.loads((ROOT/corrections['source']).read_text())
    municipal = {f['properties']['DOITT_ID']: f for f in source['features']}
    parcels = json.loads((ROOT/'source-data/nyc-pluto-2026-09-06.json').read_text())
    parcels = {str(int(float(p['bbl']))): p for p in parcels['records']}
    dx, dz = corrections['alignment']['translationMetres']
    byid = {b['id']: b for b in buildings}
    for addition in corrections['addBuildings']:
        feature = municipal[addition['doittId']]
        geometry = feature['geometry']
        rings = geometry['coordinates'] if geometry['type'] == 'Polygon' else geometry['coordinates'][0]
        def ring(coords):
            points = [point({'lon': q[0], 'lat': q[1]}) for q in coords]
            points = [[round(x+dx, 3), round(z+dz, 3)] for x,z in points]
            return points[:-1] if points[0] == points[-1] else points
        p = ring(rings[0])
        box = [min(q[0] for q in p), min(q[1] for q in p), max(q[0] for q in p), max(q[1] for q in p)]
        x,z = (box[0]+box[2])/2, (box[1]+box[3])/2
        row = next((i for i in range(5) if streets[i][1] <= z < streets[i+1][1]), None)
        col = 0 if -229 < x < 0 else 1 if 0 <= x < 214 else None
        tile = f'block-{row+1}-{col+1}' if row is not None and col is not None else 'edge-'+('west' if x < -229 else 'east' if x > 214 else 'north' if z < -157.8 else 'south')
        props = feature['properties']
        parcel = parcels.get(props['BASE_BBL'], {})
        h = round(props['HEIGHT_ROOF'] * .3048, 2)
        b = {'id': addition['id'], 'bin': str(addition['bin']), 'address': addition['address'],
             'name': 'East Side Community School' if addition['bin'] == 1005974 else '',
             'p': p, 'box': box, 'center': [x,z], 'height': h, 'heightEstimated': False,
             'floors': int(float(parcel.get('numfloors', round(h/3.25)))), 'core': False,
             'tile': tile, 'buildingType': addition['buildingType'], 'frontages': [],
             'geometrySource': {'publisher': 'NYC OTI', 'doittId': addition['doittId'],
                                'checked': corrections['checked'], 'alignment': corrections['alignment']}}
        if len(rings) > 1:
            b['holes'] = [ring(r) for r in rings[1:]]
        buildings.append(b)
        byid[b['id']] = b
    for change in corrections['addressCorrections']:
        b = byid[change['id']]
        b['address'] = change['address']
        if change.get('retainAlias') and change['retainAlias'] not in b.setdefault('addressAliases', []):b['addressAliases'].append(change['retainAlias'])
        b['addressSource']={k:v for k,v in change.items() if k not in ['id','retainAlias']}
    for match in corrections['municipalMatches']:
        b = byid[match['buildingId']]
        props = municipal[match['doittId']]['properties']
        parcel = parcels.get(props['BASE_BBL'], {})
        record = {'bin': str(props['BIN']), 'doittId': props['DOITT_ID'], 'bbl': props['BASE_BBL'],
                  'matchBasis': match['basis'], 'checked': corrections['checked'],
                  'roofHeightMetres': round((props.get('HEIGHT_ROOF') or 0)*.3048, 2),
                  'edited': props.get('LAST_EDITED_DATE'), 'parcel': parcel}
        b.setdefault('municipalReferences', []).append(record)
    # A directly matched municipal roof observation supersedes an estimated OSM
    # box height. Do not transfer a height through a partial/annex overlap join.
    for b in buildings:
        exact = [r for r in b.get('municipalReferences', []) if r['matchBasis'] == 'BIN' and r['bin'] == b['bin']]
        if b['core'] or len(exact) != 1:
            continue
        r = exact[0]
        if 3 < r['roofHeightMetres'] < 100:
            b['osmHeight'] = b['height']
            b['height'] = r['roofHeightMetres']
            b['heightEstimated'] = False
            b['heightSource'] = {'publisher': 'NYC OTI', 'doittId': r['doittId'], 'checked': r['checked'], 'basis': 'Roof height above local ground; excludes rooftop equipment.'}
        parcel = r['parcel']
        if parcel.get('numbldgs') == '1' and b['heightEstimated']:
            b['floors'] = max(1, round(float(parcel['numfloors'])))
    return {'checked': corrections['checked'], 'municipalBuildings': len(municipal),
            'accountedFor': len(corrections['municipalMatches']), 'restoredBuildings': len(corrections['addBuildings']),
            'source': 'model-source/geography-corrections.json'}
