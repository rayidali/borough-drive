"""Join independently dated place evidence to buildings and individual frontages.

No network or nonstandard packages. Uncorroborated mapped names remain in the
audit, with unnamed shop openings in the model. A website address or inspection
is evidence of occupancy at a date, not an assertion that a shop is open today.
"""
import json
import math
import re
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def normalized(value):
    s = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def address_key(value):
    s = re.sub(r'\b(?:saint|st)\s+mark(?:s|\s+s)?\b', 'st marks', normalized(value))
    s = re.sub(r'\b(first|1st|1) (avenue|ave)\b', 'first avenue', s)
    s = re.sub(r'\b(second|2nd|2) (avenue|ave)\b', 'second avenue', s)
    s = re.sub(r'\bave a\b', 'avenue a', s)
    s = re.sub(r'\be (\d)', r'east \1', s)
    s = re.sub(r'\b(\d+)(?:st|nd|rd|th)\b', r'\1', s)
    s = re.sub(r'\bst$', 'street', s)
    s = re.sub(r'\bpl$', 'place', s)
    return s


def street_key(value):
    return re.sub(r'^\d+[a-z]?\s+', '', address_key(value))


def inside(p, ring):
    x,z = p
    yes = False
    for a,b in zip(ring, ring[1:]+ring[:1]):
        if (a[1] > z) != (b[1] > z) and x < (b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0]:
            yes = not yes
    return yes


def projection(p, f):
    s = (p[0]-f['x'])*f['rx']+(p[1]-f['z'])*f['rz']
    clamped = max(0, min(f['length'], s))
    d = math.dist(p, (f['x']+f['rx']*clamped, f['z']+f['rz']*clamped))
    return s, d


def same_name(a, b):
    a,b = normalized(a), normalized(b)
    if a == b or (min(len(a),len(b)) >= 4 and (a in b or b in a)):
        return True
    return SequenceMatcher(None, a,b).ratio() >= .80


def compile_businesses(data):
    raw = json.loads((ROOT/'source-data/osm-raw.json').read_text())
    web = json.loads((ROOT/'source-data/business-web-evidence-2026-09-06.json').read_text())
    web = {r['id']: r for r in web['records']}
    city = json.loads((ROOT/'source-data/nyc-business-records-2026-09-06.json').read_text())['records']
    corrections = json.loads((ROOT/'model-source/business-corrections.json').read_text())
    excluded = {r['osmId']: r for r in corrections['excluded']}
    overrides = {r['osmId']: r for r in corrections['places']}
    buildings = data['buildings']; byid = {b['id']: b for b in buildings}
    aliases = defaultdict(list)
    for b in buildings:
        b['businesses'] = []
        for a in [b['address'], *b.get('addressAliases', [])]:
            if a: aliases[address_key(a)].append(b)
    origin = data['origin']; bearing = math.radians(data['axis']['avenueBearing'])
    cs,sn = math.cos(bearing), math.sin(bearing)
    def point(lat,lon):
        e = (float(lon)-origin['lon'])*111320*math.cos(math.radians(origin['lat']))
        n = (float(lat)-origin['lat'])*111320
        return [round(e*cs-n*sn,3), round(-e*sn-n*cs,3)]
    def locate(p, address='', bin_id=None):
        exact = aliases.get(address_key(address), [])
        exact = [b for b in exact if math.dist(b['center'],p)<60 and b['frontages']]
        if exact: return min(exact, key=lambda b: math.dist(b['center'],p)), 'address'
        contained = [b for b in buildings if inside(p,b['p']) and not any(inside(p,h) for h in b.get('holes',[])) and b['frontages']]
        if contained: return min(contained,key=lambda b: math.dist(b['center'],p)), 'mapped point in footprint'
        if bin_id:
            matches = [b for b in buildings if b['bin']==str(bin_id) and b['frontages']]
            if len(matches)==1: return matches[0], 'municipal BIN'
        near = [(projection(p,f)[1],b) for b in buildings for f in b['frontages']]
        if near:
            distance,b = min(near,key=lambda q:q[0])
            if distance<3.5: return b,'mapped point within 3.5 m of frontage'
        return None,'unresolved'
    def frontage(b,p,address,street=None):
        wanted = street_key(street or address)
        fs = [(i,f) for i,f in enumerate(b['frontages']) if not wanted or street_key(f['street'])==wanted]
        if not fs: fs = list(enumerate(b['frontages']))
        i,f = min(fs,key=lambda q:projection(p,q[1])[1])
        s,d = projection(p,f)
        return i,round(max(.1,min(f['length']-.1,s)),3),round(d,3)
    records=[]; used_city=set()
    for e in raw['elements']:
        t=e.get('tags',{})
        if e['type']!='node' or not t.get('name') or not (t.get('shop') or t.get('amenity') in ['bar','pub','restaurant','fast_food','cafe','ice_cream','pharmacy','bank']): continue
        p=point(e['lat'],e['lon'])
        if not (data['extent'][0]<p[0]<data['extent'][2] and data['extent'][1]<p[1]<data['extent'][3]): continue
        a=' '.join(filter(None,[t.get('addr:housenumber'),t.get('addr:street')]))
        b,basis=locate(p,a)
        override=overrides.get(e['id'],{})
        if override:
            b=byid[override['buildingId']];basis='reviewed exact building identity'
        entry={'id':'osm-node-'+str(e['id']),'osmId':e['id'],'name':override.get('name',t['name']),
               'category':t.get('shop',t.get('amenity')),'mappedAddress':a,'point':p,
               'sources':[{'publisher':'OpenStreetMap contributors','url':f'https://www.openstreetmap.org/node/{e["id"]}', 'snapshot':data['snapshot']}],
               'buildingId':b['id'] if b else None,'buildingMatch':basis,'renderName':False,'status':'mapped identity; independent occupancy unresolved'}
        if not b:
            records.append(entry); continue
        possible=[r for r in city if same_name(t['name'],r['dba']) and (r.get('bin')==b['bin'] or math.dist(p,point(r['latitude'],r['longitude']))<25)]
        if possible:
            r=max(possible,key=lambda r:r['inspection_date']);used_city.add(r['camis'])
            entry['sources'].append({'publisher':'NYC DOHMH','url':f'https://data.cityofnewyork.us/resource/43nn-pn8j.json?camis={r["camis"]}', 'inspectionDate':r['inspection_date'][:10],'name':r['dba'],'address':r['building']+' '+r['street'],'bin':r.get('bin')})
            if r['inspection_date'][:10]>='2025-09-01':
                entry.update(renderName=True,status='dated city occupancy record')
        w=web.get(e['id'])
        if w and w.get('addresses'):
            candidates=[q for q in w['addresses'] if address_key(q) in {address_key(a), *[address_key(v) for v in [b['address'],*b.get('addressAliases',[])]]}]
            # Website may use a more specific unit/corner address than the OSM footprint.
            if not candidates:
                candidates=[q for q in w['addresses'] if any(street_key(q)==street_key(f['street']) for f in b['frontages']) and re.match(r'^\d+',q) and abs(int(re.match(r'^\d+',q)[0])-int(re.match(r'^\d+',a or b['address'])[0]))<=0] if re.match(r'^\d+',a or b['address']) else []
            if candidates:
                entry['sources'].append({'publisher':'Business website','url':w.get('addressSource',w['url']),'checked':w['checked'],'address':candidates[0]})
                entry.update(renderName=True,status='website lists this address')
                if not a:a=candidates[0]
        if override:
            entry['sources'].append({'publisher':'Reviewed occupancy source','url':override['source'],'sourceDate':override.get('sourceDate'),'checked':override.get('checked',corrections['checked']),'basis':override['basis']})
            entry.update(renderName=True,status='individually reviewed occupancy')
            for key in ['profile','fascia','letters','awning']:
                if key in override:entry[key]=override[key]
        i,s,d=frontage(b,p,a,override.get('street'))
        entry.update(frontageIndex=i,street=b['frontages'][i]['street'],along=s,frontageDistance=d)
        if t.get('level') and t['level'] not in ['0','-1','0;1']:entry.update(renderName=False,status='upper-floor place; no verified street sign')
        if e['id'] in excluded:
            rejection=excluded[e['id']]
            entry.update(renderName=False,status=rejection['reason'])
            if rejection.get('source'):entry['sources'].append({'publisher':'Reviewed contrary evidence','url':rejection['source'],'sourceDate':rejection.get('sourceDate'),'checked':corrections['checked']})
        # Architectural photos do not establish sign artwork; use restrained text
        # within the real frontage and expose this distinction in the source record.
        entry['appearance']='Sign lettering, exact shop partition and interior are estimates unless an individual facade profile is supplied.'
        records.append(entry); b['businesses'].append(entry)
    # Preserve prior individually researched occupancy, adding its provenance to
    # the same inventory. A business name never makes a whole building a shop.
    for b in buildings:
        spec=b['facadeSpec'];name=spec.get('business')
        if not name or spec.get('vacant') or spec.get('landmark'):continue
        existing=next((r for r in b['businesses'] if same_name(r['name'],name) or name=='RESTAURANT' and same_name(r['name'],'Superiority Burger')),None)
        if existing:
            if existing.get('osmId') in excluded:continue
            existing.update(renderName=True,status='individually researched occupancy')
            for k in ['fascia','letters','awning','profile']:
                if k in spec:existing[k]=spec[k]
            existing['sources'].append({'publisher':'Existing dated neighborhood research','record':b.get('reference',{})})
        elif b['frontages']:
            i,s,d=frontage(b,b['center'],b['address'],spec.get('frontStreet'))
            entry={'id':'researched-'+str(b['id']),'name':name,'buildingId':b['id'],'street':b['frontages'][i]['street'],'frontageIndex':i,'along':round(b['frontages'][i]['length']*.5,3),'renderName':True,'status':'individually researched occupancy','sources':[{'publisher':'Existing dated neighborhood research','record':b.get('reference',{})}],'appearance':'Partition dimensions and unobserved sign design remain estimated.'}
            for k in ['fascia','letters','awning','profile']:
                if k in spec:entry[k]=spec[k]
            b['businesses'].append(entry);records.append(entry)
    # New occupants absent from the OSM node inventory are admitted only by
    # explicit review of a dated city record and their current identity.
    for reviewed in corrections.get('cityPlaces',[]):
        r=next(r for r in city if r['camis']==reviewed['camis'])
        p=point(r['latitude'],r['longitude']);a=r['building']+' '+r['street']
        b,basis=locate(p,a,r.get('bin'))
        if not b:raise ValueError('Reviewed business has no building: '+r['dba'])
        if any(same_name(reviewed.get('name',r['dba']),e['name']) and e['renderName'] for e in b['businesses']):continue
        used_city.add(r['camis']);i,s,d=frontage(b,p,a)
        entry={'id':'city-'+r['camis'],'name':reviewed.get('name',r['dba']),'category':reviewed.get('category','restaurant'),'buildingId':b['id'],'buildingMatch':basis,'point':p,'street':b['frontages'][i]['street'],'frontageIndex':i,'along':s,'frontageDistance':d,'renderName':True,'status':'reviewed dated city occupancy','sources':[{'publisher':'NYC DOHMH','url':f'https://data.cityofnewyork.us/resource/43nn-pn8j.json?camis={r["camis"]}','inspectionDate':r['inspection_date'][:10],'address':a,'bin':r.get('bin')},{'publisher':'Reviewed identity source','url':reviewed['source'],'checked':corrections['checked']}],'appearance':'Unmeasured partition and sign design remain estimates.'}
        for k in ['fascia','letters','profile','awning']:
            if k in reviewed:entry[k]=reviewed[k]
        for e in b['businesses']:
            if e.get('osmId') in reviewed.get('supersedes',[]):e.update(renderName=False,status='Superseded by reviewed occupant '+entry['name'])
        entry['mappedAddress']=' '.join(a.split()).title()
        b['businesses'].append(entry);records.append(entry)
    for b in buildings:
        groups=defaultdict(list)
        for r in b['businesses']:
            if r['renderName']:groups[r['frontageIndex']].append(r)
        for index,entries in groups.items():
            f=b['frontages'][index];entries.sort(key=lambda r:r['along'])
            # Co-located duplicate OSM nodes must not create duplicate shops.
            unique=[]
            for r in entries:
                if any(same_name(r['name'],q['name']) and abs(r['along']-q['along'])<5 for q in unique):
                    r.update(renderName=False,status='duplicate mapped identity');continue
                unique.append(r)
            for j,r in enumerate(unique):
                left=(unique[j-1]['along']+r['along'])/2 if j else .12
                right=(r['along']+unique[j+1]['along'])/2 if j+1<len(unique) else f['length']-.12
                # A point near a corner does not establish ownership of the
                # entire side elevation. Leave unsupported stretches unnamed.
                # This conservative envelope is explicitly an estimate, not a
                # measured shop width or a new parcel boundary.
                if right-left>14:
                    left=max(left,r['along']-6)
                    right=min(right,r['along']+6)
                r['unit']=[round(left,3),round(right,3)]
                r['unitBasis']='Point order on the selected street frontage, with a bounded envelope for long unpartitioned elevations; dividing walls and unit widths estimated. Unsupported stretches remain unnamed.'
    audit={'revision':'04','checked':'2026-09-06','scope':'Existing map only; includes unresolved candidates. An inspection or website is dated evidence, not a real-time opening guarantee.','places':records,
           'unmatchedCityRecords':[{'camis':r['camis'],'name':r['dba'],'address':r['building']+' '+r['street'],'inspectionDate':r['inspection_date'][:10],'reason':'No corroborating mapped identity; not assigned a new sign.'} for r in city if r['camis'] not in used_city]}
    (ROOT/'model-source/neighborhood-business-audit.json').write_text(json.dumps(audit,indent=2))
    data['businessSummary']={'checked':audit['checked'],'mappedCandidates':sum('osmId' in r for r in records),'namedPlaces':sum(r['renderName'] for r in records),'namedNonCorePlaces':sum(r['renderName'] and r['buildingId'] in byid and not byid[r['buildingId']]['core'] for r in records),'unresolved':sum(not r['renderName'] for r in records),'source':'model-source/neighborhood-business-audit.json','scope':audit['scope']}
    return audit
