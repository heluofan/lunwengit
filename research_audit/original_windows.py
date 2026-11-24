from pathlib import Path
import re
p=Path(r'C:\lunwen\research_audit\new_direction_20261122\feasibility_recheck');t=(p/'original_full_clean.txt').read_text('utf-8')
for w in ['Classification','Dataset C: WG—classification','Figure 7','0–5','window','available','Data Records']:
 ids=[m.start() for m in re.finditer(re.escape(w),t,re.I)];print('\nTERM',w)
 for i in ids[:4]:print(t[max(0,i-150):i+1600])
