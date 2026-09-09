"""Apply the bounded First & Seventh benchmark without changing map footprints."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def compile_corner(data):
    schedule=json.loads((ROOT/'model-source/first-and-seventh.json').read_text())
    byid={b['id']:b for b in data['buildings']}
    for r in schedule['buildings']:
        b=byid[r['id']]
        if b['core']:raise ValueError('Corner benchmark cannot replace the accepted core')
        b['cornerReconstruction']={'revision':schedule['revision'],'profile':r['profile'],
                                   'source':'model-source/first-and-seventh.json',
                                   'sources':r['sources'],'limits':r['limits']}
        b['facadeSpec'].update(height=r['height'],floors=r['floors'],wall=r['wall'],observed=True)
        b['renderHeight']=r['height']
        for street,face in r['elevations'].items():
            b['facadeSpec'].setdefault('elevations',{}).setdefault(street,{})['wall']=r['wall']
            b['facadeSpec']['elevations'][street]['cornerSchedule']=face
    # Remove generic street-furniture clusters in the small intersection area;
    # the authored corner kit provides the observed signals, bins and mailboxes.
    def outside(p):return not (-32<p['x']<17 and 216<p['z']<242)
    data['furniture']=[p for p in data['furniture'] if outside(p)]
    for g in data['detailProps']:
        if 'litter-bin' in g['url']:g['placements']=[p for p in g['placements'] if outside(p)]
    data['detailSummary']['streetObjects']=sum(len(g['placements']) for g in data['detailProps'])
    data['referenceSummary']['newObservedBuildings']=sum(b['facadeSpec'].get('observed',False) for b in data['buildings'] if not b['core'])
    data['cornerDetailSummary']={'revision':schedule['revision'],'checked':schedule['checked'],
        'buildings':[r['id'] for r in schedule['buildings']],
        'elevations':sum(len(r['elevations']) for r in schedule['buildings']),
        'source':'model-source/first-and-seventh.json','scope':schedule['scope'],
        'streetViewVerified':False,'acceptance':schedule['acceptance']}
    def obstacle(bid,street,at,d,w,h,kind):
        f=next(f for f in byid[bid]['frontages'] if f['street']==street)
        s=at*f['length']
        data['storefrontObstacles'].append({'record':'first-seventh-'+str(bid),'kind':kind,
            'x':round(f['x']+f['rx']*s-f['rz']*d,3),'z':round(f['z']+f['rz']*s+f['rx']*d,3),
            'rx':f['rx'],'rz':f['rz'],'halfWidth':w/2,'halfDepth':h/2})
    for bid,at,width in [(248142331,.28,1.42),(248142331,.59,1.29),(248142404,.48,1.29),(248142404,.83,1.07)]:
        obstacle(bid,'First Avenue',at,.55,width,.53,'plant rack')
    obstacle(241829631,'East 7th Street',.86+(.99-.86)*.63,.88,.60,.40,'folding table')
    b=byid[248142707];r=next(r for r in b['businesses'] if r.get('design',{}).get('cornerStyle')=='deli')
    f=b['frontages'][r['frontageIndex']];along=(r['unit'][0]+(r['unit'][1]-r['unit'][0])*.24)/f['length']
    obstacle(b['id'],'First Avenue',along,.96,.57,.56,'menu board')
    for kind,positions in [('signal',schedule['streetFurniture']['signals']),('mailbox',schedule['streetFurniture']['mailboxes']),('bin',schedule['streetFurniture']['bins'])]:
        for x,z in positions:data['storefrontObstacles'].append({'record':'first-seventh-streets','kind':kind,'x':x,'z':z,'rx':1,'rz':0,'halfWidth':.33 if kind=='mailbox' else .27,'halfDepth':.31 if kind=='mailbox' else .27})
    return schedule
