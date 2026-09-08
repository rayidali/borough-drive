"""List every non-core street frontage and its remaining digital-twin evidence.

Run after prepare/compile. This inventory never promotes partial observations
to a claim that a facade is surveyed or fully current.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'dist/reconstruction/neighborhood.json').read_text())
rows=[]
for b in data['buildings']:
    if b['core']:continue
    for i,f in enumerate(b['frontages']):
        places=[p for p in b['businesses'] if p['renderName'] and p['frontageIndex']==i]
        designed=[p for p in places if p.get('design')]
        rows.append({'buildingId':b['id'],'address':b['address'],'tile':b['tile'],'street':f['street'],
                     'hasSomeBuildingPhotoEvidence':bool(b['facadeSpec'].get('observed')),
                     'separateElevationSchedule':f['street'] in b['facadeSpec'].get('elevations',{}),
                     'supportedNames':[p['name'] for p in places],
                     'individualDesigns':[p['appearance']['record'] for p in designed],
                     'namesStillUsingEstimatedDesigns':[p['name'] for p in places if not p.get('design')],
                     'fullySurveyed':False})
report={'recorded':'2026-09-08','scope':'All non-core street frontages in the existing map; core remains separate.',
        'limits':'Some building-level photo evidence is not proof of observation of this particular street elevation. A separate elevation schedule is also not a complete survey.',
        'requiredForSurvey':['Dated full exterior and oblique photographs','Measured facade and opening dimensions','Verified current tenant/unit partition','Exact sign and material artwork with reuse provenance','Dated outdoor seating, boards and small fixtures','Secondary elevation evidence','Matched-view visual acceptance'],
        'summary':{'streetFrontages':len(rows),'supportedNames':sum(len(r['supportedNames']) for r in rows),
                   'individualDesigns':sum(len(r['individualDesigns']) for r in rows),
                   'namesStillUsingEstimatedDesigns':sum(len(r['namesStillUsingEstimatedDesigns']) for r in rows)},
        'frontages':rows}
(ROOT/'model-source/digital-twin-coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report['summary']))
