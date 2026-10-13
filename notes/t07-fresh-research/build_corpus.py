from pathlib import Path
import json,csv,re,collections,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).parent
raw={r['id']:r for r in json.loads((ROOT/'metadata-verified.json').read_text(encoding='utf-8'))}
cr={r['id']:r for r in json.loads((ROOT/'crossref-audit.json').read_text(encoding='utf-8'))}
ann=list(csv.DictReader((ROOT/'annotations.psv').open(encoding='utf-8'),delimiter='|'))
fallback={
'D04':('CVPR Workshops',2019),'F02':('arXiv; chưa xác minh peer review',2026),'F04':('ACM Multimedia 2026; acceptance theo trang tác giả',2026),'F06':('arXiv; chưa xác minh peer review',2026),
'G04':('ICML',2021),'G05':('NeurIPS',2021),'G06':('ICLR',2023),'G07':('CVPR',2023),'G10':('CVPR',2025),
'R02':('CVPR',2022),'R03':('CVPR',2023),'R09':('arXiv; tác giả/code ghi TIP; cần xác minh ấn bản',2024),
'S08':('NeurIPS',2022),'S12':('ICCV',2025)}
loc={
'F03':'Full-text §4.1–4.2, selected §5 experiments',
'F04':'Full-text §3.1, §4.2, §4.4, supplement §2.7 and §6.3',
'G10':'Full-text §3.2–3.3 (Cholesky head)',
'G11':'Full-text abstract, §3.3 and §4.1–4.2 excerpts',
'R02':'Full-text §3.1–3.3',
'R04':'Full-text §3 and beginning §4',
'R09':'Full-text implementation and main results excerpts (not full method audit)',
'S05':'Full-text §3.2–3.5',
'S07':'Full-text input GSD discussion and §4 experimental setup excerpts',
'S12':'Full-text workflow and §3.1–3.2',
'F05':'Publisher-indexed introduction, §3 method and conclusion excerpts; full direct fetch blocked'}
out=[]
for a in ann:
 r=raw[a['id']];c=cr[a['id']]
 doi=c.get('DOI') if c.get('match_verified') else None
 dv='Crossref title exact/near-exact' if doi else 'none verified in Crossref'
 if not doi:
  linked=[u.split('doi.org/')[-1] for u in r.get('links',[]) if 'doi.org/' in u and '10.48550/' not in u]
  if linked:doi=linked[0];dv='DOI linked by primary source; Crossref title query unresolved'
 if c.get('match_verified'):
  venue='; '.join(c.get('venue',[]))
  year=c.get('published',{}).get('date-parts',[[None]])[0][0]
  status='Publication metadata matched in Crossref; see version note'
 else:
  date=r.get('citation_date') or ''
  year=int(date[:4]) if date[:4].isdigit() else None
  venue,year=fallback.get(a['id'],('arXiv; venue chưa xác minh',year))
  status=r.get('comments') or r.get('journal_reference') or 'Venue not verified; primary record exists'
 authors=r.get('authors') or [' '.join([x.get('given',''),x.get('family','')]).strip() for x in c.get('authors',[]) if c.get('match_verified')]
 author_code=[u for u in r.get('links',[]) if 'github.com/' in u]
 depth='M — đọc chọn lọc từ full text' if a['id'] in loc and a['id']!='F05' else ('E — trích đoạn publisher' if a['id']=='F05' else 'A — abstract/metadata')
 rr={**a,'title':r['title'],'year':year,'venue':venue,'status':status,'authors':authors,'primary_url':r['primary_url'],'pdf_url':r.get('pdf_url'),'doi':doi,'doi_verification':dv,'code_url':author_code[0] if author_code else None,'code_status':'Tác giả dẫn link; chưa cài/chạy' if author_code else 'Chưa xác minh link repo',
'read_depth':depth,'evidence_locator':loc.get(a['id'],'Abstract on primary source; metadata/publication comments'),'retrieved':'2026-10-13',
'version_note':r.get('version_history') or 'Primary source checked 2026-10-13; Crossref year may be journal edition after first preprint.'}
 out.append(rr)
assert len(out)==50 and len({r['id'] for r in out})==50
assert {r['id'] for r in out}==set(raw)
(ROOT/'corpus-50.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'corpus-50.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader()
 for r in out:w.writerow({k:'; '.join(v) if isinstance(v,list) else v for k,v in r.items()})
md=['# Corpus 50 — T07 nghiên cứu mới','',
'Ngày kiểm tra: 13/10/2026. Corpus có chủ đích theo cơ chế và quyết định nghiên cứu, không phải xếp hạng 50 bài gần nhất toàn thế giới. 55 ứng viên có tên đã được kiểm tra trong lượt này; 5 bài nền được nhường chỗ cho prior trực tiếp. Search không vét cạn.','',
'**Mức đọc:** A = abstract và metadata; M = các đoạn phương pháp/thực nghiệm được chỉ rõ, không có nghĩa đã đọc trọn bài; E = trích đoạn publisher. Không có bài nào được gắn nhãn đã tái lập. Không được suy gap từ việc chưa đọc mục đó.','',
'Các limitation có nhãn [suy luận] là hạn chế của việc chuyển kết quả sang nghiên cứu mới, không nhất thiết là lỗi của bài gốc. DOI null nghĩa chưa xác minh, không nghĩa bài không thật. Năm là năm ấn bản nếu Crossref xác minh; có thể khác năm arXiv/acceptance. Code link chỉ đã thấy tác giả dẫn, chưa chứng minh chạy được.','',
'## Mục lục','',
'| ID | Bài | Năm/venue | Vai trò | Đọc |','|---|---|---|---|---|']
for r in out:md.append(f"| [{r['id']}](#{r['id'].lower()}) | {r['title']} | {r['year']} · {r['venue']} | {r['role']} | {r['read_depth'].split(' — ')[0]} |")
for r in out:
 md.extend(['',f"## {r['id']}",'',f"**[{r['title']}]({r['primary_url']})**",'',
 f"- Năm/venue: {r['year']} — {r['venue']}. Trạng thái: {r['status']}.",
 f"- Vai trò: {r['role']}; liên quan {r['relevance']}/5 (đánh giá chủ quan); ưu tiên: {r['priority']}.",
 f"- Đã đọc: {r['read_depth']}; vị trí: {r['evidence_locator']}.",
 f"- Cơ chế: {r['mechanism']}",
 f"- Giới hạn: {r['limitation']}",
 f"- Dùng vào đề tài: {r['research_use']}",
 f"- DOI: "+(f"[{r['doi']}](https://doi.org/{r['doi']}) — {r['doi_verification']}." if r['doi'] else "chưa xác minh."),
 f"- Code: "+(f"[Link tác giả]({r['code_url']}) — {r['code_status']}." if r['code_url'] else "chưa xác minh.")])
md.extend(['','## Screening decisions','',
'- ViTDet (arXiv 2203.16527), Deformable DETR (2010.04159), DINO (2203.03605), SAM 2 (2408.00714), SkySense (2312.10115): nguồn/abstract đã xem nhưng chuyển sang background; nhường chỗ cho DenseScout, Dynamic Zoom-in, Remix, AFWD-Net và Visual Accommodation vì trực tiếp chặn claim novelty về resolution allocation.',
'- Không tính arXiv và bản journal của cùng phương pháp thành hai bài. Mask R-CNN có metadata Crossref bản TPAMI 2020; không suy ra phương pháp ra đời năm 2020.',
'- DOTA-v1 và DOTA-v2 là hai công trình benchmark khác nhau, nhưng có quan hệ ảnh; không tính chúng là hai miền độc lập.',
'- Các bài chỉ có snippet không rõ nguồn, bài ngoài miền không có cơ chế chuyển giao rõ, nguồn giả thuyết tự sinh và nguồn xuất bản sau 13/10/2026 không dùng làm chứng cứ.',
'- Danh sách được cập nhật bằng citation chaining; số 55 là số ứng viên đã định danh để xử lý, không phải số kết quả search hay thống kê PRISMA.'])
(ROOT/'CORPUS-50.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
stats={'count':len(out),'roles':dict(collections.Counter(r['role'] for r in out)),'read_depth':dict(collections.Counter(r['read_depth'] for r in out)),'crossref_matches':sum(c.get('match_verified',False) for c in cr.values()),'primary_html_cached':len(list((ROOT/'sources'/'metadata').glob('*.html'))),'doi_verified_or_source_linked':sum(bool(r['doi']) for r in out)}
(ROOT/'corpus-stats.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(stats,ensure_ascii=False))
