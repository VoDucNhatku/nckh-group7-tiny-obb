from pathlib import Path
ROOT=Path(__file__).parent
repo=ROOT.parent.parent
ledger=repo/'notes'/'claims-ledger.md'
row="| C-13 | 2026-10-13 | NEW SCOPE at user request: restart from T1-7 only; 50-paper evidence map; H1 resolution-allocation reliability for OBB as pilot priority, H2–H5 alternatives; 4 weeks 13/10–09/11 and Kaggle/60 USD Modal. Generic gain routing, Gaussian head and SAM+multiscale are already prior art. | Unverified; T1/T2 labels describe intervention only, not journal quartile | No defensible venue band yet. Consider a scope-matched Q2 candidate only after novelty, validity, matched-budget utility and replication gates; Q1/top conference conditional on substantive insight and evidence supporting generality. Do not reuse deterministic tier→quartile mapping. | research candidate — no detector runs; not runnable as stated until data/checkpoint/profile verified | notes/06-uav-research-2026-10-13/t07-fresh-research/REPORT.md; notes/06-uav-research-2026-10-13/t07-fresh-research/DECISIONS.md |"
with ledger.open('a',encoding='utf-8') as f:
 if '| C-13 |' not in ledger.read_text(encoding='utf-8'):f.write('\n'+row+'\n')
index=repo/'notes'/'INDEX.md'
entry='| t07-fresh-research | admin + research-admin + paper-read/synthesize + hallucination-guard | notes/06-uav-research-2026-10-13/t07-fresh-research/REPORT.md; notes/06-uav-research-2026-10-13/t07-fresh-research/CORPUS-50.md; notes/06-uav-research-2026-10-13/t07-fresh-research/EXPERIMENT-PLAN.md | 2026-10-13: fresh scope from original T1-7, 4 weeks/60 USD. 50 records (39 abstract, 10 selected full-text, 1 publisher excerpts); 32 Crossref matches. No new architecture or venue-worthiness verified, no detector runs. C-13; H1 only pilot priority. |'
if 't07-fresh-research |' not in index.read_text(encoding='utf-8'):
 with index.open('a',encoding='utf-8') as f:f.write('\n'+entry+'\n')
print('Registered C-13 and INDEX entry')
