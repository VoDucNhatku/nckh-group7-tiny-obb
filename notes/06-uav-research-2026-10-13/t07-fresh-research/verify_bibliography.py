from pathlib import Path
import sys,json,re,urllib.request,urllib.parse,concurrent.futures,time,difflib
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).parent
rows=json.loads((ROOT/'metadata-verified.json').read_text(encoding='utf-8'))
for r in rows:
 if r['id']=='F05':
  r.update(title='Differentiable Resolution Allocation for Tiny Object Detection in UAV Imagery',citation_date='2026',journal='Sensors',abstract='Publisher search extract: AFWD-Net couples differentiable adaptive foveation, local wavelet recovery and density-conditioned sparse detection; full direct HTML fetch blocked.',status='verified_primary_search_extract',verification_note='Primary publisher page and /notes verified with web search 2026-10-13; direct urllib request blocked.',links=['https://doi.org/10.3390/s26196157'])
 if r['id']=='G11':
  r.update(abstract='Primary PDF abstract read: oriented detection via 3D Gaussians in feature space projected to 2D; decoder optimizes Gaussian parameters and supports adaptive count at inference.',pdf_url='https://www.ijcai.org/proceedings/2025/0101.pdf')
 cache=ROOT/'sources'/'metadata'/(r['id']+'.html')
 if cache.exists():
  s=BeautifulSoup(cache.read_text(encoding='utf-8'),'html.parser')
  r['authors']=[x.get('content') for x in s.select('meta[name=citation_author]')]
  r['version_history']=s.select_one('.dateline').get_text(' ',strip=True) if s.select_one('.dateline') else None
def norm(t):return re.sub('[^a-z0-9]','',t.lower())
def fetch(r):
 u='https://api.crossref.org/works?rows=1&query.title='+urllib.parse.quote(r['title'])
 try:
  data=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'T07-Literature-Audit/1.0'}),timeout=18))
  item=data['message']['items'][0];title=item.get('title',[''])[0]
  score=difflib.SequenceMatcher(None,norm(title),norm(r['title'])).ratio()
  return {'id':r['id'],'queried_title':r['title'],'match_title':title,'similarity':round(score,4),'DOI':item.get('DOI'),'venue':item.get('container-title'),'published':item.get('published'),'published_online':item.get('published-online'),'authors':item.get('author'),'type':item.get('type'),'match_verified':score>=0.97}
 except Exception as e:return {'id':r['id'],'error':str(e),'match_verified':False}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 out=list(ex.map(fetch,rows))
(ROOT/'metadata-verified.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'crossref-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
for r in out:print(r['id'],r.get('match_verified'),r.get('similarity'),r.get('DOI'),r.get('venue'),r.get('published'))
