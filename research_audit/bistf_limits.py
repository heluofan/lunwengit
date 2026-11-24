from pathlib import Path
import re
p=Path(r'C:\lunwen\research_audit\new_direction_20261122');t=(p/'bistf_clean.txt').read_text('utf-8')
for term in ['limitation','cross-subject','within-subject','delay','Parameters','parameters','Data Preprocessing','10 s','13 s']:
 ids=[m.start() for m in re.finditer(re.escape(term),t,re.I)];print(term,[t[max(0,i-150):i+1000] for i in (ids[-2:] if term=='limitation' else ids[:2])])
t=(p/'mgf_full_clean.txt').read_text('utf-8')
for term in ['cross-subject','Data Availability','github','code','limitation']:
 ids=[m.start() for m in re.finditer(re.escape(term),t,re.I)];print('MGF',term,[t[max(0,i-120):i+800] for i in (ids[-2:] if term=='limitation' else ids[:2])])
