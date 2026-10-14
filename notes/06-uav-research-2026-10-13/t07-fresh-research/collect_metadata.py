from pathlib import Path
import json, re, concurrent.futures, urllib.request, time
from bs4 import BeautifulSoup
ROOT=Path(__file__).parent
ARX={
'D01':'1711.10398','D02':'2102.12219','D03':'1909.00133','D04':'1905.12886','D05':'2001.06303','D06':'2103.05569',
'B01':'1612.03144','B05':'2304.08069','F04':'2604.25300','F06':'2412.06341',
'F01':'2603.09411','F02':'2604.19233',
'G01':'1812.00155','G02':'2008.09397','G03':'2108.05699','G04':'2101.11952','G05':'2106.01883','G06':'2201.12558','G07':'2211.06368','G09':'2205.12785','G10':'2502.01565','G12':'2603.15497',
'R01':'1904.08008','R02':'2103.09136','R03':'2303.14488','R04':'2202.06934','R05':'1812.01600','R06':'2208.08738','R07':'2206.13996','R08':'2412.11582','R09':'2407.16424','R10':'2106.10409','R11':'2404.06180','R12':'2112.10415',
'S01':'1703.06870','S02':'2112.01527','S03':'2304.02643','S07':'2212.14532','S08':'2207.08051','S10':'2306.11029','S11':'2410.01768','R13':'1711.05187'}
OTHER={
'R14':'https://www.microsoft.com/en-us/research/?p=763831',
'F05':'https://www.mdpi.com/1424-8220/26/19/6157',
'F03':'https://openaccess.thecvf.com/content/CVPR2025/html/Al-Emadi_Benchmarking_Object_Detectors_under_Real-World_Distribution_Shifts_in_Satellite_Imagery_CVPR_2025_paper.html',
'G08':'https://openaccess.thecvf.com/content/WACV2025/html/Lee_Hausdorff_Distance_Matching_with_Adaptive_Query_Denoising_for_Rotated_Detection_WACV_2025_paper.html',
'G11':'https://www.ijcai.org/proceedings/2025/101',
'S05':'https://openaccess.thecvf.com/content/ACCV2024/html/Zhang_RS-SAM_Integrating_Multi-Scale_Information_for_Enhanced_Remote_Sensing_Image_Segmentation_ACCV_2024_paper.html',
'S06':'https://openaccess.thecvf.com/content/CVPR2025/html/Shan_ROS-SAM_High-Quality_Interactive_Segmentation_for_Remote_Sensing_Moving_Object_CVPR_2025_paper.html',
'S12':'https://openaccess.thecvf.com/content/ICCV2025/html/Burges_Active_Learning_Meets_Foundation_Models_Fast_Remote_Sensing_Data_Annotation_ICCV_2025_paper.html'}
URLS={k:'https://arxiv.org/abs/'+v for k,v in ARX.items()}|OTHER
def fetch(k,url):
    dest=ROOT/'sources'/'metadata';dest.mkdir(parents=True,exist_ok=True)
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 Academic research source verification'})
        html=urllib.request.urlopen(req,timeout=25).read().decode('utf-8')
        (dest/(k+'.html')).write_text(html,encoding='utf-8')
        s=BeautifulSoup(html,'html.parser')
        def meta(n):
            a=s.find('meta',attrs={'name':n})
            return a.get('content') if a else None
        title=meta('citation_title')
        if not title:
            x=s.select_one('#papertitle') or s.select_one('h1') or s.select_one('title')
            title=x.get_text(' ',strip=True) if x else None
        a=s.select_one('blockquote.abstract') or s.select_one('#abstract') or s.select_one('.abstract')
        abstract=a.get_text(' ',strip=True) if a else ''
        if not abstract:
            t=s.get_text(' ',strip=True);p=t.find('Abstract');abstract=t[p:p+2500] if p>=0 else ''
        comments=s.select_one('td.comments')
        jr=s.select_one('td.jref')
        links=[a['href'] for a in s.select('a[href]') if any(x in a['href'] for x in ['github.com','doi.org'])]
        record={'id':k,'primary_url':url,'title':title,'citation_date':meta('citation_date') or meta('citation_publication_date'),
            'pdf_url':meta('citation_pdf_url'),'journal':meta('citation_journal_title'),'abstract':abstract,
            'comments':comments.get_text(' ',strip=True) if comments else None,'journal_reference':jr.get_text(' ',strip=True) if jr else None,
            'links':links,'retrieved':'2026-10-13','status':'fetched'}
        return record
    except Exception as e:return {'id':k,'primary_url':url,'status':'fetch_failed','error':str(e)}
if __name__=='__main__':
    import sys;sys.stdout.reconfigure(encoding='utf-8')
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        out=list(ex.map(lambda kv:fetch(*kv),URLS.items()))
    out.sort(key=lambda r:r['id'])
    (ROOT/'metadata-verified.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    for r in out:print(r['id'],r['status'],r.get('title',''),r.get('comments',''),r.get('journal_reference',''))
