from pathlib import Path
import json,re
OUT=Path(r'C:\lunwen\output\医学多模态论文阅读_2026-11-22')
rows=json.loads((OUT/'逐篇提取_结构化数据.json').read_text('utf-8'))
required=['title','journal','year','clinical_problem','modalities','data_source_and_size','task','method_innovation','metrics','main_conclusions','limitations','multimodal_necessity','packaging_logic','source_pdf','extracted_text']
assert len(rows)==94 and len({r['id'] for r in rows})==94
for r in rows:
 for field in required:assert r.get(field),(r['id'],field)
 for field in ['source_pdf','extracted_text']:assert Path(r[field]).exists(),(r['id'],field)
sop=(OUT/'02_医学多模态选题SOP_v4_带论文例证.md').read_text('utf-8')
rules=re.split(r'### R\d+ · ',sop)[1:]
for i,rule in enumerate(rules,1):
 examples=re.findall(r'\*\*\[(\d{3})\]',rule)
 assert len(set(examples))>=2,(i,examples)
 for ex in examples:assert ex in {r['id'] for r in rows}
full=(OUT/'01_逐篇提取_94篇.md').read_text('utf-8')
assert len(re.findall(r'<a id="p\d+"',full))==94
reader=(OUT/'逐篇阅读_可搜索.html').read_text('utf-8')
assert reader.count('<article id=')==94
report={'entries':94,'required_fields':len(required),'rules':10,'every_rule_has_at_least_two_examples':True,'source_links_exist':True,'unique_article_anchors':94,'html_cards':94,'unresolved_scope':['未实测数据集下载/代码运行','未逐刊核对北大核心届次','未逐式复算统计','部分原文未明确规模/协议，已标注','093部分中文编码乱码，采用页面/英文和表格补核']}
(OUT/'阅读覆盖与验收.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
