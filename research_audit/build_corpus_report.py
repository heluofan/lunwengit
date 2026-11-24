from pathlib import Path
import json,re,unicodedata,html
ROOT=Path(r'C:\lunwen\research_audit\corpus_2025_2026')
OUT=Path(r'C:\lunwen\output\医学多模态论文阅读_2026-11-22')
OUT.mkdir(parents=True,exist_ok=True)
keys=['id','journal','year','task','clinical_problem','modalities','data_source_and_size','method_innovation','metrics','main_conclusions','limitations','multimodal_necessity','packaging_logic']
records=[]
for filename in ['records_original_1.txt','records_original_2.txt','records_context.txt']:
 for line in (ROOT/filename).read_text('utf-8').splitlines():
  if not line.strip():continue
  cols=line.split('|')
  assert len(cols)==len(keys),(cols[0],len(cols),len(keys))
  item=dict(zip(keys,cols));item['category']='背景/综述/理论/教学' if filename=='records_context.txt' else '方法/临床/系统研究'
  records.append(item)
records.sort(key=lambda r:r['id'])
manifest=json.loads((ROOT/'manifest.json').read_text('utf-8'))
meta={x['id']:x for x in manifest}
for r in records:
 r['title']=Path(meta[r['id']]['file']).stem.rsplit('_',1)[0].replace(' (1)','')
 r['source_pdf']=meta[r['id']]['file'];r['extracted_text']=meta[r['id']]['text'];r['pdf_pages']=meta[r['id']]['pages']
 # Final corrections after checking complete experiment/discussion sections.
 if r['id']=='082':
  r['data_source_and_size']='两院配对CT/DWI：第一院228人、7778片（6222训1556测）；第二院635人、8167片（6533训1634测），均按片数描述8:2'
  r['main_conclusions']='作者报告第二院MSE0.0059、PSNR28.12dB、SSIM0.844；两院均有生成比较；不是独立跨院测试的同义词'
 if r['id']=='100':r['main_conclusions']='LPBA40 Dice70.1%、OASIS79.9%；报告负雅可比比例0.01%；模型可解释性主要来自展开结构'
 if r['id']=='055':
  r['data_source_and_size']='BraTS2019 335人（259高级别/76低级别）；CHAOS文内描述40个T1/T2序列（20训练/20测试）；两张2080Ti；五折交叉验证'
  r['metrics']='Dice、HD、Acc；五折交叉验证及单边双样本t检验（统计单元和检验适配仍需审查）'
 if r['id']=='078':r['main_conclusions']+='；分类最佳模型报告Acc约87%、敏感度约96%、特异度约66%'
 if r['id']=='050':r['main_conclusions']+='；注意0.600为临床模型特异度，不能误读为临床AUC'
expected=set(meta)-{'020','069','071','085','095','096'}
assert {r['id'] for r in records}==expected,('Missing',expected-{r['id'] for r in records})
assert len(records)==94
(OUT/'逐篇提取_结构化数据.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')

def link(label,path):return f'[{label}](<{Path(path).as_posix()}>)'
intro='''# 医学多模态论文逐篇提取：94篇正文记录

日期：2026-11-22。目的：审计旧选题SOP，反推论文呈现出的立题与论证结构。这里的“包装逻辑”是读者根据论文内容作的解释，不是作者真实选题、实验或投稿过程的还原。

## 范围与证据口径

- 输入100个PDF，共1204页。按Unicode/空白规范化后的正文去重，94篇不同文章；61篇方法/临床/系统研究，33篇综述、述评、理论、教学等背景文章。分类用于本次审计，不声称等同数据库文献类型。
- 逐篇提取全文，并阅读摘要及与任务、方法、数据/实验、结果、结论有关的段落；研究论文重点回查数据与对照；综述按综述记录，不把引用工作的样本和结果算成其自己的实验。没有逐条验证全部参考文献，也没有逐式复算全部公式/原始统计。
- 对关键争议表格进行PDF页面视觉复核：025第5页、053第8页、078第4页、081第5页、039第6页等；093中文编码乱码，结合可见PDF页面、英文摘要及可读表格处理。其余可疑字段保留边界，不补写不存在的信息。
- “作者报告”不等于本次复现实验。本文没有训练模型、下载数据集或验证作者代码完整性；“公开数据”只表示论文所述来源，不能据此认定当前可以直接下载、可合法复用或代码可跑。
- 患者、病灶、扫描、切片、图像对、裁块与增强样本分别记录；不得将这些数量混用。“未确认/未明确”是信息缺口，不是已证实论文没有交代。精确缺口须继续回原文/附件，禁止猜补。
- 期刊与年份按PDF卷期/页眉记录；未逐刊核验北大核心目录届次。052为增刊；005有年份标识冲突；040卷期为2026年12月，晚于本次阅读日期，作为用户提供版本记录，不推定已正式刊出。
- 局限栏显式区分作者自述与本次核查者判断；没有将所有论文的统计/评价做法视作推荐实践。

## 重复文件处理

同正文重复：020→019；069→068；071→070；085→084；095/096→094。PDF哈希不同（可能为下载包装/水印差异），没有按文件名或哈希单独判断文献重复；没有删除或修改原文件。

## 如何阅读

先看单篇“模态组合、数据来源与规模、多模态必要性、局限”，再看方法。真正用于新SOP的例证与反例在第二份报告中逐条给出。本表完整保留非多模态/非医学文章，防止只挑支持旧规则的论文。

## 文章索引

|ID|标题|期刊/年份|任务|类别|
|---|---|---|---|---|
'''
lines=[intro]
for r in records:
 lines.append(f"|{r['id']}|[{r['title']}](#p{r['id']})|{r['journal']}，{r['year']}|{r['task']}|{r['category']}|\n")
labels=[('clinical_problem','临床问题'),('modalities','模态组合与部署含义'),('data_source_and_size','数据来源与规模'),('task','任务类型'),('method_innovation','方法创新（论文声称）'),('metrics','评价指标'),('main_conclusions','主要结论（作者报告/已核数值）'),('limitations','局限与核查意见'),('multimodal_necessity','作者如何论证多模态必要性'),('packaging_logic','选题包装逻辑（本次反推）')]
for r in records:
 lines.append(f"\n<a id=\"p{r['id']}\"></a>\n\n## {r['id']} · {r['title']}\n\n**{r['journal']}｜{r['year']}｜{r['category']}｜PDF {r['pdf_pages']}页**\n\n")
 lines.append(link('原PDF',r['source_pdf'])+' · '+link('带页号全文提取',r['extracted_text'])+'\n\n')
 for k,label in labels:lines.append(f'- **{label}**：{r[k]}。\n')
(OUT/'01_逐篇提取_94篇.md').write_text(''.join(lines),encoding='utf-8')

# Preserve exact excerpts with PDF page numbers rather than generating unverifiable quotes.
ev=['# 原文定位摘录（辅助核查，不代替全文）\n\n每条均直接摘自本地PDF提取文本；自动关键词命中可能含引言中的相关工作。正文总数与原文页面可由逐篇报告链接继续核对。\n']
for r in records:
 text=unicodedata.normalize('NFKC',Path(r['extracted_text']).read_text('utf-8'))
 pages=re.split(r'=== PDF_PAGE \d+ ===',text)[1:]
 ev.append(f"\n## {r['id']} {r['title']}\n\n")
 for j,p in enumerate(pages,1):
  if j==1:
   ev.append(f'### PDF第{j}页：篇首\n\n'+p[:1800]+'\n\n')
   continue
  pats=[r'(?:数据集|研究对象|资料与方法|数据准备|数据收集|实验设置)',r'(?:单模态|单一模态|仅临床|仅形态|消融实验|局限性|本研究的局限|结束语|结\s*论)']
  for pat in pats:
   m=re.search(pat,p)
   if m:
    ev.append(f'### PDF第{j}页：相关段落\n\n'+p[max(0,m.start()-80):m.start()+1000]+'\n\n')
(OUT/'04_原文定位摘录.md').write_text(''.join(ev),encoding='utf-8')

# Searchable local reader: same records as the markdown, no external services or assets.
cards=[]
for r in records:
 body=''.join(f'<dt>{html.escape(label)}</dt><dd>{html.escape(r[k])}</dd>' for k,label in labels)
 src='file:///'+Path(r['source_pdf']).as_posix()
 cards.append(f'<article id="p{r["id"]}" data-search="{html.escape(" ".join(map(str,r.values())),quote=True)}"><h2>{r["id"]} {html.escape(r["title"])}</h2><p class="meta">{html.escape(r["journal"])} · {r["year"]} · {html.escape(r["category"])}</p><p><a href="{html.escape(src,quote=True)}">查看本地PDF</a></p><dl>{body}</dl></article>')
reader='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>医学多模态论文逐篇阅读</title><style>body{font-family:"Microsoft YaHei",sans-serif;margin:0;background:#f3f5f7;color:#172333;line-height:1.7}header{position:sticky;top:0;background:#142638;color:white;padding:16px 5vw}header h1{font-size:21px;margin:0 0 8px}input{box-sizing:border-box;width:min(100%,760px);padding:11px;border:0;border-radius:5px}main{max-width:1020px;margin:25px auto;padding:0 18px}article{background:white;border:1px solid #dce2e8;border-radius:8px;padding:22px;margin:20px 0}h2{font-size:20px;line-height:1.6;margin:0 0 8px}.meta{color:#5d6d7b}dt{font-weight:bold;margin-top:15px}dd{margin:4px 0}a{color:#08646c}.note{background:#fff5db;padding:16px;border-left:4px solid #aa7400}@media print{header{position:static;background:white;color:black}input{display:none}article{break-inside:avoid}}</style><header><h1>94篇医学多模态相关论文 · 逐篇结构化阅读</h1><input id="q" placeholder="搜索题名、任务、模态、数据集、私有、局限等"><span id="count"></span></header><main><p class="note">基于论文呈现反推论证结构，不还原作者真实选题过程。公开数据未实测下载；文献结果未复现。样本量、模态定义、测试协议及资源限制优先于模块名称。详见配套Markdown的范围说明。</p>'''+''.join(cards)+'''</main><script>const q=document.querySelector('#q'),cards=[...document.querySelectorAll('article')],count=document.querySelector('#count');q.addEventListener('input',()=>{let n=0;const terms=q.value.toLowerCase().trim().split(/\\s+/).filter(Boolean);for(const c of cards){const ok=terms.every(t=>c.dataset.search.toLowerCase().includes(t));c.hidden=!ok;if(ok)n++}count.textContent=' '+n+' / 94'});q.dispatchEvent(new Event('input'));</script></html>'''
(OUT/'逐篇阅读_可搜索.html').write_text(reader,encoding='utf-8')
print(json.dumps({'papers':len(records),'original':sum(r['category']=='方法/临床/系统研究' for r in records),'context':sum(r['category']!='方法/临床/系统研究' for r in records),'out':str(OUT),'files':[p.name for p in OUT.iterdir()]},ensure_ascii=False))
