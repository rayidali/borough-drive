# Run from repository root after an authorized deployment: python3 model-source/publication-review-09/verify-live.py
import concurrent.futures,datetime,hashlib,json,urllib.request,ssl
from pathlib import Path
root=Path.cwd();build=json.loads((root/'dist/seventh/build.json').read_text())
checks=[]
for host in ['https://www.drivearound.nyc','https://drivearound.nyc','https://borough-drive.vercel.app']:
 for route,local in [('/','dist/seventh/index.html'),('/seventh/','dist/seventh/index.html'),('/index.html','dist/legacy.html'),('/seventh/build.json','dist/seventh/build.json')]:
  checks.append((host+route,local))
for file in build['files']:
 checks.append(('https://www.drivearound.nyc/seventh/'+file,'dist/seventh/'+file))
checks.append(('https://www.drivearound.nyc/reconstruction/ASSET-CREDITS.md','dist/reconstruction/ASSET-CREDITS.md'))
def verify(item):
 url,local=item;expected=hashlib.sha256((root/local).read_bytes()).hexdigest();digest=hashlib.sha256();size=0
 req=urllib.request.Request(url,headers={'Accept-Encoding':'identity','User-Agent':'BoroughDriveReleaseCheck/09'})
 with urllib.request.urlopen(req,timeout=180,context=ssl.create_default_context(cafile="/etc/ssl/cert.pem" if Path("/etc/ssl/cert.pem").exists() else None)) as response:
  status=response.status;final=response.url;headers={key:response.headers.get(key) for key in ['content-type','content-length','etag','last-modified','x-vercel-cache']}
  while block:=response.read(1024*1024):digest.update(block);size+=len(block)
 actual=digest.hexdigest();result={'url':url,'finalUrl':final,'local':local,'status':status,'bytes':size,'sha256':actual,'expectedSha256':expected,'matches':actual==expected,'headers':headers};print(json.dumps({key:result[key] for key in ['url','bytes','matches']}),flush=True);return result
out=root/'model-source/publication-review-09';out.mkdir(exist_ok=True)
report={'recorded':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':__import__('subprocess').check_output(['git','rev-parse','HEAD']).decode().strip(),'method':'HTTPS GET with streaming SHA256 of complete decoded response; all 18 runtime files, 12 route/manifest checks across canonical/apex/Vercel hosts, and refreshed credits.','checks':[]}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for result in pool.map(verify,checks):report['checks'].append(result)
report['complete']=all(x['matches'] and x['status']==200 for x in report['checks']);(out/'live.json').write_text(json.dumps(report,indent=2)+'\n');assert report['complete'];print('ALL_LIVE_HASHES_MATCH',len(checks))
