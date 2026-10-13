from pathlib import Path
import json,csv,re,collections,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).parent
rows=json.loads((ROOT/'corpus-50.json').read_text(encoding='utf-8'))
cross=json.loads((ROOT/'crossref-audit.json').read_text(encoding='utf-8'))
checks={}
checks['50_records']=len(rows)==50
for field in ['id','title','primary_url']:
 checks['unique_'+field]=len({r[field] for r in rows})==50
checks['csv_matches_json']=len(list(csv.DictReader((ROOT/'corpus-50.csv').open(encoding='utf-8-sig'))))==50
checks['required_fields']=all(all(r.get(k) for k in ['title','primary_url','mechanism','limitation','research_use','read_depth','evidence_locator']) for r in rows)
checks['primary_sources_only']=all(any(x in r['primary_url'] for x in ['arxiv.org','thecvf.com','ijcai.org','microsoft.com/en-us/research','mdpi.com']) for r in rows)
checks['crossref_matches_32']=sum(bool(r.get('match_verified')) for r in cross)==32
checks['exact_read_counts']=dict(collections.Counter(r['read_depth'][0] for r in rows))=={'A':39,'M':10,'E':1}
docs=['REPORT.md','CORPUS-50.md','PROTOCOL.md','EXPERIMENT-PLAN.md','DECISIONS.md','AUDIT.md']
broken=[]
for f in docs:
 p=ROOT/f
 for match in re.finditer(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  link=match.group(1)
  if link.startswith(('https://','http://','#')):continue
  target=link.split('#')[0]
  if not (ROOT/target).exists():broken.append((f,link))
checks['local_links_exist']=not broken
missing_refs=[]
valid={r['id'] for r in rows}
for f in ['REPORT.md','EXPERIMENT-PLAN.md','DECISIONS.md']:
 for id in re.findall(r'\b[DBGFRS]\d{2}\b',(ROOT/f).read_text(encoding='utf-8')):
  if id not in valid:missing_refs.append((f,id))
checks['paper_ids_resolve']=not missing_refs
rates={'T4':.000164,'L4':.000222,'A10':.000306,'A100_40':.000583}
costs={k:round(3600*(v+2*.0000131+16*.00000222),6) for k,v in rates.items()}
checks['l4_budget_arithmetic']=abs(costs['L4']-1.021392)<1e-8
checks['28_calendar_days']=(datetime.date(2026,11,9)-datetime.date(2026,10,13)).days+1==28
checks['design_and_limits_visible']=all(x in (ROOT/'REPORT.md').read_text(encoding='utf-8') for x in ['chưa phải','chưa có','39 bài','10 bài','1 bài','60 USD'])
summary={'date':'2026-10-13','checks':checks,'passed':sum(checks.values()),'total':len(checks),'broken_links':broken,'unresolved_ids':missing_refs,'hourly_example_costs':costs,'note':'Structural checks only; not experiment validation or full literature novelty clearance.'}
(ROOT/'verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
assert all(checks.values()),'Deliverable verification failed'
