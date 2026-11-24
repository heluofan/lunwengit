from pathlib import Path
import re
p=Path(r'C:\lunwen\research_audit\topic_selection_nov23');t=(p/'hyper_paper_clean.txt').read_text('utf-8')
for term in ['labeled videos','Labeled videos','374 videos','Data Records']:
 ids=[m.start() for m in re.finditer(re.escape(term),t,re.I)];print('\n',term,len(ids))
 for i in ids[:3]:print(t[max(0,i-250):i+2200])
