from pathlib import Path
import csv
import json
import re
from collections import Counter

BASE = Path(__file__).resolve().parent
papers = list(csv.DictReader((BASE.parent / 't07-fresh-research/corpus-50.csv').open(encoding='utf-8-sig')))
updates = json.loads((BASE / 'evidence-update.json').read_text(encoding='utf-8-sig'))
questions = (BASE / 'QUESTION-BANK.md').read_text(encoding='utf-8-sig')
report = (BASE / 'PROBLEM-MAP.md').read_text(encoding='utf-8-sig')
qids = re.findall(r'^\d+\.\s+\*\*(Q\d{3})\s', questions, re.M)
cards = re.findall(r'^### P\d{2}\s', questions, re.M)
goals = re.findall(r'^\| \*\*(M\d{2})\.', report, re.M)
programmes = re.findall(r'^### P[1-5] —', report, re.M)
known = {p['id'] for p in papers + updates} | {'X01', 'X02', 'X03', 'X04'}
refs = set(re.findall(r'\b(?:[BDFGRS]\d{2}|N\d{2}|X\d{2})\b', report + questions))
bad_links = []
for filename in ['PROBLEM-MAP.md', 'QUESTION-BANK.md', 'ROOT-SOURCES.md', 'SESSION.md']:
    body = (BASE / filename).read_text(encoding='utf-8-sig')
    for target in re.findall(r'\]\(([^)]+)\)', body):
        if target.startswith(('https://', 'http://', '#')):
            continue
        target = target.strip('<>').split('#')[0]
        if not (BASE / target).exists():
            bad_links.append({'file': filename, 'target': target})
normalize = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
old_titles = {normalize(x['title']) for x in papers}
duplicate_titles = [x['id'] for x in updates if normalize(x['title']) in old_titles]
required = {'id', 'title', 'primary_url', 'task', 'mechanism', 'demonstrated_scope', 'remaining_question', 'read_depth', 'evidence_locator'}
checks = {
    '120_unique_questions_in_sequence': qids == [f'Q{i:03}' for i in range(1, 121)],
    '12_question_groups': len(re.findall(r'^## [A-L]\. ', questions, re.M)) == 12,
    '12_priority_cards': len(cards) == 12,
    '13_unique_goals': goals == [f'M{i:02}' for i in range(1, 14)],
    '5_research_programmes': len(programmes) == 5,
    '18_new_evidence_records': len(updates) == 18,
    'new_evidence_ids_unique': len({x['id'] for x in updates}) == 18,
    'no_new_title_duplicate_of_original_50': not duplicate_titles,
    'evidence_required_fields': all(required <= set(x) for x in updates),
    'report_and_question_source_ids_resolve': not (refs - known),
    'local_links_exist': not bad_links,
    'HARD_scope_visible': all(x in report for x in ['Car', '2 giây', 'không có queue']),
    'segmentation_protocol_visible': all(x in report for x in ['given-box', 'teacher', 'IoU']),
    'hypothesis_vs_module_falsification_explicit': 'Điều gì bác giả thuyết trung tâm' in report and 'chưa là preregistration hoàn chỉnh' in report,
}
out = {
    'date': '2026-10-13',
    'checks': checks,
    'passed': sum(checks.values()), 'total': len(checks),
    'counts': {'questions': len(qids), 'priority_cards': len(cards), 'goals': len(goals), 'programmes': len(programmes), 'added_evidence': len(updates)},
    'new_evidence_read_depths': dict(Counter(x['read_depth'] for x in updates)),
    'unresolved_source_ids': sorted(refs-known), 'broken_local_links': bad_links,
    'note': 'Structural verification only. Does not prove novelty, scientific validity, full-text coverage, external URL reachability, or experimental superiority.'
}
(BASE/'verification.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(out, ensure_ascii=False, indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
