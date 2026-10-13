from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
index_path = root / 'notes/INDEX.md'
index_text = index_path.read_text(encoding='utf-8-sig')
registry_key = '| t07-problem-map |'
if registry_key not in index_text:
    row = '\n| t07-problem-map | admin + Sol/high x2 + Astra/high | notes/t07-problem-map/PROBLEM-MAP.md; notes/t07-problem-map/QUESTION-BANK.md; notes/t07-problem-map/EVIDENCE-UPDATE.md; notes/t07-problem-map/FINAL-REVIEW.md | 2026-10-13: user drops cost filter; 13 improvement goals, 5 research programmes, 120 questions/12 cards; 18 added source records + 4 metric/method sources. Independent critique and changed-span re-review done; no novelty/performance/venue claim; no experiments. |\n'
    index_path.write_text(index_text.rstrip()+'\n'+row, encoding='utf-8')
ledger_path = root / 'notes/claims-ledger.md'
ledger_text = ledger_path.read_text(encoding='utf-8-sig')
marker = 'USER-REQUESTED SCOPE EXPANSION: remove cost filter'
if marker not in ledger_text:
    claim_ids = [int(x) for x in re.findall(r'^\| C-(\d+) \|', ledger_text, re.M)]
    claim_id = max(claim_ids, default=0)+1
    row = f'\n| C-{claim_id} | 2026-10-13 | USER-REQUESTED SCOPE EXPANSION: remove cost filter; C-13 H1 pilot priority remains historical/context-specific, not best scientific direction. 13 diagnostic axes, 5 research programmes, 120 questions; add temporal/MOT/streaming/segmentation/domain/annotation priors. | Unverified research questions; no architecture or novelty tier established | No venue band assigned; no superiority claim. Select a falsifiable question, audit closest prior and validate task-specific evidence before architecture/venue decisions. | exploratory problem map; no detector runs or runnable protocol asserted | notes/t07-problem-map/PROBLEM-MAP.md; notes/t07-problem-map/AUDIT.md |\n'
    ledger_path.write_text(ledger_text.rstrip()+'\n'+row, encoding='utf-8')
    print(f'Appended C-{claim_id}')
else:
    print('Existing scope-expansion ledger entry preserved')
print('Artifact registry verified')
