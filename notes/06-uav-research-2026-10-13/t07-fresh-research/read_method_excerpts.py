from pathlib import Path
import sys,re
sys.stdout.reconfigure(encoding='utf-8')
r=Path(__file__).parent
jobs=[
('R02','resolution','3.1',6500),
('R04','resolution','SLICING AIDED',5000),
('R09','resolution','3.2',5000),
('G11','geometry','3.3',4500),
('G12','geometry','Angle Distribution',3500),
('S05','representation','3.2',5000),
('S12','representation','3.2',4000)]
for id,f,n,lim in jobs:
 t=(r/'sources'/f/(id+'.txt')).read_text(encoding='utf-8')
 hits=list(re.finditer(re.escape(n),t,re.I))
 h=next((h for h in hits if h.start()>4500),hits[0] if hits else None)
 print('\nSOURCE',id,'needle',n,'offset',h.start() if h else None)
 if h:print(t[max(0,h.start()-120):h.start()+lim])
