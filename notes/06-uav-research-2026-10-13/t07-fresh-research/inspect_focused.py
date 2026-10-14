from pathlib import Path
import sys,re
sys.stdout.reconfigure(encoding='utf-8')
r=Path(__file__).parent
jobs={
'sources/focused/F04.txt':['3 Method','3.1','3.2','3.3','fixed-','Limitations','gain','utility'],
'sources/focused/F02.txt':['3.1','threshold','Table 4','limitation'],
'sources/focused/S07.txt':['3.1','Ground','4.2','Limitations'],
'sources/focused/F03.txt':['4.1','4.2','5. Conclusion','Limitations']}
for f,needles in jobs.items():
 t=(r/f).read_text(encoding='utf-8')
 print('\nSOURCE',f)
 for n in needles:
  hits=list(re.finditer(re.escape(n),t,re.I))
  # use first substantive matches (not bibliography)
  print('\nTERM',n,'MATCHES',len(hits))
  for m in hits[:2]:print(t[max(0,m.start()-120):m.start()+1300])
