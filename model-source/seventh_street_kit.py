"""Seventh-only additions installed in the existing Blender recipe namespace.

Schedules live under storefront-details.json / seventhEngine. The earlier
ten-block schedules and accepted corner recipes are deliberately preserved.
Shared components express recorded features; hardware dimensions, wear and
small furnishings are authored estimates, never measurements or image copies.
"""
from copy import deepcopy

material('seventh shop blue',(.016,.22,.47),.79)
material('seventh warm plaster',(.68,.62,.51),.93)
material('seventh brass lettering',(.68,.44,.16),.55,.35)
material('seventh worn iron',(.062,.077,.074),.72,.35)
material('seventh terracotta pot',(.37,.17,.10),.96)
material('seventh fresh leaves',(.10,.25,.09),.86)
material('seventh leaf tip',(.28,.40,.12),.88)
material('seventh cloth pale',(.62,.57,.46),.95)
material('seventh mint door',(.37,.52,.38),.83)
material('seventh lilac door',(.36,.23,.48),.83)
material('seventh mint panel relief',(.23,.34,.24),.88)
material('seventh lilac panel relief',(.24,.13,.34),.88)
material('seventh turquoise',(.12,.48,.46),.87)
material('seventh pink reveal',(.66,.22,.30),.88)

# Reuse the measured-shape model and the existing component library, with a
# separate profile for the asymmetrical 50 East 7th elevation actually seen in
# the archive. Heights within the municipal envelope are visual estimates.
_seventh_base_render = render_building
def render_building(b):
    if b['id']!=241829575:
        return _seventh_base_render(b)
    spec={**b['facadeSpec'],**b['facadeSpec']['elevations']['East 7th Street']}
    owner('50 East 7th Street / observed asymmetrical elevation')
    b['renderHeight']=15.15
    wall_mass(b,'warm brick')
    f=main_front(b,'East 7th Street');f.wall='warm brick';f.detail={}
    f.window_frame='white frame';f.window_dressing=True
    trim='cream stone'
    # Left groups of three, right paired windows, with one broad arched group.
    for row,y in enumerate([4.95,8.35,11.75]):
        for at,w,parts in [(.28,f.L*.34,3),(.76,f.L*.21,2)]:
            f.window_shape='round' if row==1 and at<.5 else 'rectangle'
            street_window(f,f.L*at,y,w,2.08,trim,0)
            for j in range(1,parts):f.b(f.L*at-w/2+w*j/parts,y+.99,.12,.052,1.95,.07,'white frame')
            if row!=1 or at>.5:f.b(f.L*at,y+2.23,.10,w+.27,.23,.18,trim)
    # Carved spandrel beneath the left arch; repeated rosettes stand in for
    # unmeasured relief rather than claiming an exact stone carving copy.
    f.b(f.L*.28,7.85,.09,f.L*.36,.42,.14,trim)
    for j in range(7):
        s=f.L*(.13+j*.05)
        for k in range(12):
            t=k*math.tau/12;u=(k+1)*math.tau/12
            f.line((s+math.cos(t)*.115,7.85+math.sin(t)*.115,.176),(s+math.cos(u)*.115,7.85+math.sin(u)*.115,.176),.015,'seventh warm plaster')
    f.strip(4.35,.19,.12,trim)
    render_ground(b,f,b['frontages'][0],{**spec,'entryPosition':.78,'basement':True,'stoop':True},True,3,'warm brick',trim)
    # Cut the rusticated courses around the registered windows and doorway.
    # Solid full-width bands would conceal these recessed openings.
    for yy in [.60,1.18,1.76,2.34,2.92,3.50,4.08]:
        spans=[(0,f.L)]
        for left,low,right,high in OPENINGS[frontage_key(f)]:
            if high<yy-.25 or low>yy+.25:continue
            clipped=[]
            for lo,hi in spans:
                if right+.10<=lo or left-.10>=hi:clipped.append((lo,hi));continue
                if left-.10>lo:clipped.append((lo,left-.10))
                if right+.10<hi:clipped.append((right+.10,hi))
            spans=clipped
        for lo,hi in spans:
            if hi-lo>.04:f.b((lo+hi)/2,yy,.025,hi-lo,.49,.11,trim)
    # Low left balustrade and the three arched lights in the right roof tower.
    f.b(f.L*.30,15.3,-.10,f.L*.59,.20,.30,trim)
    f.b(f.L*.30,14.90,-.10,f.L*.59,.14,.30,trim)
    for j in range(18):f.b(f.L*(.015+j*.033),15.10,-.10,.07,.32,.17,trim)
    f.b(f.L*.76,15.72,-.93,f.L*.34,2.1,2.0,'warm brick')
    for at in [.675,.76,.845]:arch(f,f.L*at,15.18,f.L*.065,.92,trim,False)
    f.b(f.L*.76,16.87,-.04,f.L*.36,.23,.28,trim)
    apex=f.p(f.L*.76,18.08,-1.0)
    rim=[f.p(f.L*.59,16.98,.10),f.p(f.L*.93,16.98,.10),f.p(f.L*.93,16.98,-2.0),f.p(f.L*.59,16.98,-2.0)]
    for a,c in zip(rim,rim[1:]+rim[:1]):face([a,c,apex],'cornice green')
    f.b(f.L*.26,15.5,-2.1,f.L*.42,1.0,.35,'painted ivory')
    for at in [.11,.23,.35]:f.b(f.L*at,15.55,-1.88,.42,.58,.04,'window glass')
    b['renderHeight']=18.12

_seventh_photographed_shop=photographed_shop
class SeventhShopFacade:
    """Keep a deep entrance's backing behind its glazing and display pieces."""
    def __init__(self,f,spec):
        self.base=f
        self.back=min(-.85,-spec.get('recess',.13)-.55,spec.get('windowDepth',.035)-.55)
    def __getattr__(self,key):return getattr(self.base,key)
    def b(self,s,y,d,w,h,depth,mat):
        self.base.b(s,y,self.back if mat=='dark glass' and abs(d+.85)<.001 else d,w,h,depth,mat)
_seventh_observed_awning=observed_awning
def observed_awning(f,a,b,aw):
    if aw.get('stripeWidth',0)<.10:
        return _seventh_observed_awning(f,a,b,aw)
    # Broad alternating fabric panels visible at Agavi; the old corner kit's
    # fine pinstripe implementation is retained for all existing awnings.
    y=aw.get('y',3.1);drop=aw.get('drop',.5);d=aw.get('depth',1.12);val=aw.get('valance',.20)
    count=max(2,round((b-a)/.27))
    for j in range(count):
        l=a+(b-a)*j/count;r=a+(b-a)*(j+1)/count
        mat=aw['material'] if j%2 else aw['stripe']
        face([f.p(l,y-drop,d+.10),f.p(r,y-drop,d+.10),f.p(r,y,.10),f.p(l,y,.10)],mat)
        f.b((l+r)/2,y-drop-val/2,d+.10,r-l,val,.025,mat)
    # A small light name panel keeps the lettering legible across both stripes.
    f.b((a+b)/2,y-drop-val*.5,d+.12,min(1.15,(b-a)*.4),val,.016,'sign white')
    sign_text(f,(a+b)/2,y-drop-val*.5,b-a-.15,aw.get('text',''),aw.get('material','black iron'),aw.get('textSize',.23),d+.14)

def photographed_shop(f,a,b,r):
    spec=r['design']
    _seventh_photographed_shop(SeventhShopFacade(f,spec),a,b,r)
    w=b-a
    if spec.get('seventhDetail')=='ladybird':
        # The photographed two painted door leaves have recessed circular
        # panels and one arched surround; they are not a glazed shop window.
        c=a+w*.22;ww=w*.35;bottom=.28;shoulder=2.40
        for side,mat in [(-1,'seventh mint door'),(1,'seventh lilac door')]:
            ss=c+side*ww*.25
            f.b(ss,(shoulder+bottom)/2,.15,ww*.49,shoulder-bottom,.14,mat)
            points=[f.p(c,shoulder,.225)]
            for j in range(13):
                t=(j/12*math.pi/2)+(0 if side==1 else math.pi/2)
                points.append(f.p(c+math.cos(t)*ww/2,shoulder+math.sin(t)*ww/2,.225))
            for j in range(1,len(points)-1):face([points[0],points[j],points[j+1]],mat)
            relief='seventh mint panel relief' if side<0 else 'seventh lilac panel relief'
            # One circular top panel crosses the two differently painted leaves.
            for j in range(20):
                t=j*math.pi/20+(-math.pi/2 if side>0 else math.pi/2)
                u=(j+1)*math.pi/20+(-math.pi/2 if side>0 else math.pi/2)
                rr=ww*.21
                f.line((c+math.cos(t)*rr,2.66+math.sin(t)*rr,.29),(c+math.cos(u)*rr,2.66+math.sin(u)*rr,.29),.028,relief)
            # Arched middle panels and framed lower panels seen in the photo.
            rr=ww*.19
            for j in range(20):
                t=j*math.pi/20;u=(j+1)*math.pi/20
                f.line((ss+math.cos(t)*rr,2.0+math.sin(t)*rr,.29),(ss+math.cos(u)*rr,2.0+math.sin(u)*rr,.29),.027,relief)
            for dx in [-rr,rr]:f.line((ss+dx,1.39,.29),(ss+dx,2.0,.29),.027,relief)
            f.line((ss-rr,1.39,.29),(ss+rr,1.39,.29),.027,relief)
            for yy in [.44,1.20]:f.line((ss-rr,yy,.29),(ss+rr,yy,.29),.024,relief)
            for dx in [-rr,rr]:f.line((ss+dx,.44,.29),(ss+dx,1.20,.29),.024,relief)
        f.b(c-ww*.27,1.35,.29,.17,.46,.045,'seventh worn iron')
        f.line((c-ww*.27,1.20,.35),(c-ww*.27,1.51,.35),.024,'brass')
        f.line((c-ww*.21,1.30,.33),(c+ww*.35,1.30,.33),.017,'seventh worn iron')
        # Rusticated white wall between the door and white-framed window.
        f.b(a+w*.50,1.69,.13,w*.19,3.06,.20,'painted ivory')
        for yy in [.46,.94,1.42,1.90,2.38,2.86]:
            f.b(a+w*.50,yy,.242,w*.19,.022,.014,'cream stone')
        f.b(a+w*.50,1.98,.30,w*.17,.40,.04,'painted ivory')
        sign_text(f,a+w*.50,1.98,w*.15,'LADYBIRD','black iron',.09,.33)
        for j in range(32):
            t=j*math.pi/32;u=(j+1)*math.pi/32
            f.line((c+math.cos(t)*(ww/2+.04),shoulder+math.sin(t)*(ww/2+.04),.26),(c+math.cos(u)*(ww/2+.04),shoulder+math.sin(u)*(ww/2+.04),.26),.065,'cream stone')
    if spec.get('seventhDetail')=='trash':
        for at in [.19,.81]:
            ss=a+w*at
            f.b(ss,1.58,-.13,w*.27,1.84,.05,'seventh pink reveal')
            for j in range(3):f.b(ss+(j-1)*w*.063,1.3,-.05,w*.052,.67,.07,'seventh cloth pale' if j%2 else 'black iron')
        seventh_fence(f,a,a+w*.36,.50);seventh_fence(f,a+w*.64,b,.50)
    for bench in spec.get('benches',[]):
        if not bench.get('back'):continue
        ss=a+w*bench['at'];width=min(bench.get('width',1.3),w*.55);d=bench.get('depth',.50)
        for dx in [-width*.4,width*.4]:f.line((ss+dx,.50,d-.18),(ss+dx,1.05,d-.23),.023,'black iron')
        for yy in [.83,.96]:f.b(ss,yy,d-.22,width,.105,.04,bench.get('material','wood'))

def apply_seventh_schedule(data,schedule):
    byid={b['id']:b for b in data['buildings']}
    sources=schedule.get('sources',{})
    for record in schedule.get('elevations',[]):
        b=byid[record['buildingId']]
        assert not b['core'] and record['street']=='East 7th Street'
        assert all(s in sources for s in record['sources'])
        # A separate elevation prevents an avenue face borrowing Seventh's bays.
        existing=b['facadeSpec'].get('elevations',{}).get('East 7th Street',{})
        b['facadeSpec'].setdefault('elevations',{})['East 7th Street']={**existing,**deepcopy(record['spec'])}
        b['seventhDetail']=record.get('features',{})
    for record in schedule.get('frontages',[]):
        b=byid[record['buildingId']]
        assert not b['core']
        shop=next(p for p in b['businesses'] if p['id']==record['businessId'])
        assert shop['renderName'] and shop['street']=='East 7th Street'
        assert all(s in sources for s in record['sources'])
        f=b['frontages'][shop['frontageIndex']]
        lo,hi=record['span']
        assert 0<=lo<hi<=1
        design=deepcopy(record['design'])
        assert abs(sum(p[1] for p in design['panels'])-1)<.00001
        shop['design']=design
        shop['unit']=[lo*f['length'],hi*f['length']]
        shop['appearance']={'record':record['id'],'sources':record['sources'],'limits':record['limits']}
        shop['unitBasis']='Seventh engine photo-proportion estimate; unmeasured.'
        if record.get('elevation'):
            b['facadeSpec']['elevations']['East 7th Street'].update(record['elevation'])

def seventh_plant(f,s,d,scale=1.0,seed=0):
    rng=random.Random(DETAIL_SEED+seed)
    rod(f.p(s,.18,d),f.p(s,.18+.30*scale,d),.17*scale,'seventh terracotta pot',12,r2=.22*scale)
    rod(f.p(s,.46*scale,d),f.p(s,.49*scale,d),.23*scale,'seventh terracotta pot',12)
    for j in range(7):
        angle=j*math.tau/7;high=rng.uniform(.65,1.1)*scale
        a=(s,.40*scale,d);b=(s+math.cos(angle)*.23*scale,high,d+math.sin(angle)*.23*scale)
        f.line(a,b,.009*scale,'seventh fresh leaves')
        for k in range(3):
            p=tuple(a[t]+(b[t]-a[t])*(.40+k*.25) for t in range(3))
            w=.13*scale;h=.19*scale
            face([f.p(*p),f.p(p[0]+w,p[1]+h*.42,p[2]-.03),f.p(p[0]+w*.7,p[1]+h,p[2]),f.p(p[0]-.025,p[1]+h*.65,p[2]+.02)],'seventh fresh leaves' if j%2 else 'seventh leaf tip')

def seventh_fence(f,a,b,d=1.05):
    if b-a<.3:return
    for yy in [.37,1.20]:f.line((a,yy,d),(b,yy,d),.020,'seventh worn iron')
    for i in range(max(2,round((b-a)/.19))+1):
        x=a+(b-a)*i/max(2,round((b-a)/.19))
        f.line((x,.19,d),(x,1.30,d),.012,'seventh worn iron')
        # Small pyramidal finials and lower cross ties resolve close to the car.
        f.b(x,1.32,d,.038,.065,.038,'seventh worn iron')
    for x in [a,b]:f.b(x,.78,d,.055,1.22,.055,'seventh worn iron')

def add_seventh_detail(b,schedule):
    record=next((r for r in schedule.get('elevations',[]) if r['buildingId']==b['id']),None)
    if not record or record.get('preserveCorner'):return
    v=next(f for f in b['frontages'] if f['street']=='East 7th Street')
    f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length'])
    spec={**b['facadeSpec'],**b['facadeSpec'].get('elevations',{}).get('East 7th Street',{})}
    features=record.get('features',{})
    h=b['renderHeight'];entry=max(.9,min(f.L-.9,f.L*spec.get('entryPosition',.23)))
    if features.get('areawayRail'):
        seventh_fence(f,.12,max(.12,entry-.82))
        seventh_fence(f,min(f.L-.12,entry+.82),f.L-.12)
        # Individual slab caps beside the below-grade window wells.
        for s in [.20,f.L-.20]:f.b(s,.24,.66,.16,.16,1.03,'cream stone')
    if features.get('diamondPanels'):
        floors=spec.get('floors',b['floors']);ground=spec.get('groundTop',3.62)
        for row in range(1,floors):
            y=ground+(h-ground)*(row-.1)/max(1,floors-1)
            for at in [.15,.50,.85]:
                s=f.L*at;r=.17
                face([f.p(s-r,y,.035),f.p(s,y+r,.035),f.p(s+r,y,.035),f.p(s,y-r,.035)],'cream stone')
    if features.get('stoneBands'):
        floors=spec.get('floors',b['floors']);ground=spec.get('groundTop',3.62)
        for row in range(floors-1):
            y=ground+(h-ground-.23)*row/max(1,floors-1)-.24
            f.strip(y,.065,.066,spec.get('trim','cream stone'))
    # Close-range details use small low-sided primitives, joined into the same
    # building batches. Their placement is illustrative and separately disclosed.
    if spec.get('groundUse') not in ['shops','basement_shops'] and not b.get('businesses'):
        s=min(f.L-.28,entry+.86)
        f.b(s,1.56,.18,.16,.28,.035,'metal')
        for j in range(4):
            f.b(s-.035,1.64-j*.043,.206,.050,.020,.009,'poster paper')
            f.b(s+.052,1.64-j*.043,.209,.020,.018,.009,'brass')
    if features.get('sillPlanters'):
        for at in features['sillPlanters']:seventh_plant(f,f.L*at,.48,.55,int(at*100))
    for shop in b.get('businesses',[]):
        design=shop.get('design',{})
        if shop.get('street')!='East 7th Street' or not design.get('seventhDetail'):continue
        a,end=shop['unit'];w=end-a;kind=design['seventhDetail']
        for p in design.get('plants',[]):seventh_plant(f,a+w*p.get('at',.5),p.get('depth',.45),p.get('scale',1),int(p.get('at',.5)*100))
        if kind=='hats':
            for k in range(6):
                s=a+w*(.08+k*.085);yy=.90+(k%3)*.22
                f.line((s,.42,-.22),(s,yy,-.22),.016,'brass')
                rod(f.p(s,yy,-.22),f.p(s,yy+.035,-.22),.19,'seventh cloth pale',16)
                rod(f.p(s,yy+.035,-.22),f.p(s,yy+.15,-.22),.12,'seventh cloth pale',12,r2=.10)
            for j,char in enumerate('HATWORKS'):ctext(f,a+w*.94,2.54-j*.20,w*.10,char,'seventh brass lettering',.17,.13)
        elif kind=='tea':
            # The inspected window uses thin pale timber lattice, not brick.
            for at in [.10,.18,.26,.34,.42,.50,.58]:f.b(a+w*at,1.68,.105,.025,1.85,.025,'wood')
            for yy in [.93,1.3,1.67,2.04,2.4]:f.b(a+w*.34,yy,.105,w*.57,.025,.025,'wood')
        elif kind=='tokio':
            f.b(a+w*.26,.175,.75,w*.46,.012,1.12,'seventh fresh leaves')
            # Mannequin/display rail, not a fabricated copy of the changing art.
            for k in range(4):
                ss=a+w*(.17+k*.13)
                f.b(ss,1.22,-.42,.27,.66,.16,'seventh cloth pale' if k%2 else 'shop burgundy')
            f.line((a+w*.08,1.62,-.43),(a+w*.61,1.62,-.43),.023,'metal')
        elif kind=='kinka':
            seventh_fence(f,a+w*.15,end,.9)
            for k in range(4):seventh_plant(f,a+w*(.43+k*.13),-.20,.55,k)
        elif kind=='clothes':
            f.line((a+w*.14,.20,.73),(a+w*.14,1.63,.73),.019,'metal')
            f.line((a+w*.58,.20,.73),(a+w*.58,1.63,.73),.019,'metal')
            f.line((a+w*.14,1.63,.73),(a+w*.58,1.63,.73),.019,'metal')
            for k in range(6):
                ss=a+w*(.18+k*.067)
                f.b(ss,1.16,.73,.19,.68,.10,['seventh cloth pale','shop burgundy','seventh shop blue'][k%3])
        elif kind=='pylos':
            seventh_fence(f,a,a+w*.27,.55);seventh_fence(f,a+w*.76,end,.55)
        for at in design.get('sconces',[]):
            ss=a+w*at
            f.line((ss,2.65,.08),(ss,2.65,.32),.022,'seventh worn iron')
            f.b(ss,2.57,.32,.14,.24,.12,'opal lamp')
            for yy in [2.43,2.71]:f.b(ss,yy,.32,.20,.035,.17,'seventh worn iron')
