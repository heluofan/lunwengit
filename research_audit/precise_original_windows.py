from pathlib import Path
import re
p=Path(r'C:\lunwen\research_audit\new_direction_20261122\feasibility_recheck');t=(p/'original_full_clean.txt').read_text('utf-8')
for term in ['sliding','window','Figure 7:','Dataset C: WG—Classification','Dataset C: WG—classification','meta-classification','0–5']:
 ids=[m.start() for m in re.finditer(re.escape(term),t,re.I)];print('\n',term,len(ids))
 for i in ids[:2]:print(t[max(0,i-120):i+1600])
