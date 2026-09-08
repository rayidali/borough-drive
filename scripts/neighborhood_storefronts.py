"""Compile reviewed exterior designs without promoting occupancy evidence.

Every design selects an existing supported place and a specific street. A
normalized shop span is a photo proportion estimate, never a surveyed dimension.
"""
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def compile_storefronts(data,business_audit):
    source=ROOT/'model-source/storefront-details.json'
    schedule=json.loads(source.read_text())
    byid={b['id']:b for b in data['buildings']}
    for b in data['buildings']:
        b.pop('storefrontRevision',None)
        b['facadeSpec'].pop('elevations',None)
    counts={};obstacles=[]
    for record in schedule['elevations']:
        b=byid[record['buildingId']]
        if b['core']:raise ValueError('Observed extension must preserve core')
        if not any(f['street']==record['street'] for f in b['frontages']):raise ValueError('Missing elevation '+record['id'])
        b['facadeSpec'].setdefault('elevations',{})[record['street']]=record['spec']
    for record in schedule['frontages']:
        b=byid[record['buildingId']]
        if b['core']:raise ValueError('Observed extension must preserve core')
        r=next(r for r in b['businesses'] if r['id']==record['businessId'])
        if not r['renderName']:raise ValueError('Design cannot admit an unsupported tenant: '+record['id'])
        f=b['frontages'][r['frontageIndex']]
        if f['street']!=record['street']:raise ValueError('Design on wrong street: '+record['id'])
        if not record['sources'] or any(s not in schedule['sources'] for s in record['sources']):raise ValueError('Missing photographic provenance')
        lo,hi=record['span']
        if not 0<=lo<hi<=1:raise ValueError('Invalid observed shop proportion')
        design=record['design']
        if abs(sum(p[1] for p in design['panels'])-1)>.00001 or any(p[1]<=0 for p in design['panels']):raise ValueError('Invalid panel schedule')
        r['unit']=[round(lo*f['length'],3),round(hi*f['length'],3)]
        r['along']=round(sum(r['unit'])/2,3)
        r['unitBasis']='Photographic proportion estimate from storefront-details.json / '+record['id']+'; unmeasured.'
        r['design']=design
        r['appearance']={'record':record['id'],'checked':schedule['checked'],'sources':record['sources'],'limits':record['limits']}
        b['storefrontRevision']=schedule['revision']
        for feature in ['blades','awning','windowText','lights','boards','benches','tables','menus','grille','shutter']:
            if design.get(feature):counts[feature]=counts.get(feature,0)+1
        a,end=r['unit'];w=end-a
        for kind,halfwidth,halfdepth,depth in [('boards',.31,.30,.95),('benches',.65,.24,.50),('tables',.90,.38,1.05)]:
            for item in design.get(kind,[]):
                along=a+w*item['at'];d=item.get('depth',depth)
                hw=min(item.get('width',1.3),w*.55)/2 if kind=='benches' else halfwidth
                obstacles.append({'record':record['id'],'kind':kind,'x':round(f['x']+f['rx']*along-f['rz']*d,3),'z':round(f['z']+f['rz']*along+f['rx']*d,3),'rx':f['rx'],'rz':f['rz'],'halfWidth':hw,'halfDepth':halfdepth})
    # Export signatures cover only the evidence used by a tile. They catch stale
    # GLBs without forcing unrelated sections to change their revision marker.
    tile_signatures={}
    recipe_files=['model-source/build_neighborhood.py','model-source/neighborhood_detail_kit.py','model-source/storefront_detail_kit.py']
    recipe_hash=hashlib.sha256(b''.join((ROOT/p).read_bytes() for p in recipe_files)).hexdigest()
    for tile in data['tiles']:
        ids={b['id'] for b in data['buildings'] if b['tile']==tile['id']}
        selected={kind:[r for r in schedule[kind] if r['buildingId'] in ids] for kind in ['frontages','elevations']}
        if any(selected.values()):tile_signatures[tile['id']]=hashlib.sha256((recipe_hash+json.dumps(selected,sort_keys=True)).encode()).hexdigest()
    data['storefrontDetailSummary']={'revision':schedule['revision'],'checked':schedule['checked'],'frontages':len(schedule['frontages']),'buildings':len({r['buildingId'] for r in schedule['frontages']}),'elevations':len(schedule['elevations']),'features':counts,'recipeFiles':recipe_files,'recipeHash':recipe_hash,'tileSignatures':tile_signatures,'scope':schedule['scope']}
    data['storefrontObstacles']=obstacles
    (ROOT/'model-source/neighborhood-business-audit.json').write_text(json.dumps(business_audit,indent=2))
    return schedule
