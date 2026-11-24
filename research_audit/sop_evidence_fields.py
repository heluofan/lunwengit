from pathlib import Path
import json
p=Path(r'C:\lunwen\output\医学多模态论文阅读_2026-11-22');ds=json.loads((p/'逐篇提取_结构化数据.json').read_text('utf-8'))
for d in ds:
 if d['id'] in ['036','040','041','043','046','047','050','053','056','078']:
  print('\n',d['id'],d['title'],d['journal'],d['year'])
  for k in ['data_source_and_size','method_innovation','metrics','main_conclusions','limitations','multimodal_necessity']:print(k,d[k])
