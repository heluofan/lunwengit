from pathlib import Path
import json
p=Path(r'C:\lunwen\output\医学多模态论文阅读_2026-11-22');d=json.loads((p/'逐篇提取_结构化数据.json').read_text('utf-8'));print(type(d).__name__);print(str(d[0] if isinstance(d,list) else list(d.items())[:1])[:2500])
s=(p/'01_逐篇提取_94篇.md').read_text('utf-8')
for n in ['036','040','043','046','047','050','053','056','078']:
 start=s.find('<a id="p'+n+'"');
 if start<0:start=s.find('## '+n)
 if start>=0:
  end=s.find('\n## ',start+5); print(s[start:end if end>=0 else start+2200][:2100])
