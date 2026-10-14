from pathlib import Path
import sys,json,urllib.request,concurrent.futures,re
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup
ROOT=Path(__file__).parent
urls={
'F04':'https://arxiv.org/html/2604.25300v2',
'F02':'https://arxiv.org/html/2604.19233v1',
'S07':'https://arxiv.org/html/2212.14532v3',
'R09':'https://arxiv.org/html/2407.16424v2',
'F03':'https://openaccess.thecvf.com/content/CVPR2025/papers/Al-Emadi_Benchmarking_Object_Detectors_under_Real-World_Distribution_Shifts_in_Satellite_Imagery_CVPR_2025_paper.pdf'}
def run(item):
 k,u=item
 try:
  data=urllib.request.urlopen(u,timeout=30).read()
  folder=ROOT/'sources'/'focused';folder.mkdir(exist_ok=True)
  if u.endswith('pdf'):
   from pypdf import PdfReader
   import io
   (folder/(k+'.pdf')).write_bytes(data)
   text='\n'.join('PAGE '+str(i+1)+'\n'+(p.extract_text() or '') for i,p in enumerate(PdfReader(io.BytesIO(data)).pages))
  else:
   (folder/(k+'.html')).write_bytes(data)
   soup=BeautifulSoup(data,'html.parser')
   text=soup.get_text(' ',strip=True)
  (folder/(k+'.txt')).write_text(text,encoding='utf-8')
  return k,len(text)
 except Exception as e:return k,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for r in ex.map(run,urls.items()):print(r)
