from pathlib import Path
import json,csv,collections,re
out=Path(r'C:\lunwen\output\选题初筛_内镜视频文本检索_2026-11-23');out.mkdir(parents=True,exist_ok=True)
root=Path(r'C:\lunwen\research_audit\topic_selection_nov23')
rows=list(csv.DictReader((root/'video-labels.csv').open(encoding='utf-8-sig')))
find=collections.Counter(r['Finding 1'].strip() for r in rows); multi=sum(bool(r['Finding 2'].strip()) for r in rows); org=collections.Counter(r['Organ'] for r in rows)
repo=root/'clip4clip_src'/'CLIP4Clip-master'
files=[str(x.relative_to(repo)).replace('\\','/') for x in repo.rglob('*') if x.is_file()]
# Collect stage outputs and decisions
text=f'''# 候选方向任务卡（SOP 1—3）

日期：2026-11-23。基于《论文选题SOP_最新版.md》前3步；不提前设计创新模块，不声称已经找到可投稿贡献。

## 决定

**进入基线验证的候选：基于视频级临床标签文本的胃肠内镜视频—文本检索。**

这不是已有论文题名的复制，也不是已形成创新方案。它是SOP第1—3步筛出的可验证任务。下阶段先适配并评估公开CLIP4Clip，再据统一验证集结果判断问题是否值得做。

## 1．论文任务地图

从你提供的2025—2026期刊集中，选择“语义关联”路线。

核心依据：武星等，《基于多模态对比学习的小肠视频关键帧检索》，《生物医学工程学杂志》2025，42(2)， DOI: [10.7507/1001-5515.202304021](https://doi.org/10.7507/1001-5515.202304021)。本轮读取了用户PDF全文。

论文呈现的任务：内镜视频帧序列＋由视频标签构造的文本提示 → 视频级文本到视频检索；使用Hyper-Kvasir及视频类别标签。注意题名写“关键帧”，但正文报告的是视频级R@K/MdR检索，把多帧嵌入聚合成视频表示；数据没有逐帧病灶位置或自然语言时刻标注。因此本候选严谨表述为**视频级检索**，不声称定位病灶帧/时间段。

相邻的第二条语义路线是医学VQA。用户论文集中有2025《数据知识双增强的医学视觉问答网络》、2026《基于语境感知和多层次特征融合的医学视觉问答模型》及2026《医学视觉问答中图像与答案一致性验证方法研究》。它们覆盖相近公开基准，初查显示直接竞争更密集，暂不作为首选。此判断是候选排序，不是“VQA绝对不能做”。

任务卡：
- 输入：一段胃肠内镜视频；查询文本来自现有视频标签/器官类别。训练与推理都只看对应视频和文字标签，不使用患者报告或额外临床资料。
- 输出：按相关性排序的视频。每个视频可有两个发现标签；评估要约定主标签、多标签相关性如何处理。
- 使用边界：开放集临床文本检索、病灶定位、患者诊断或临床获益均不在当前标签证据支持范围内。

## 2．数据与资源验收

数据：HyperKvasir，官方OSF项目ID mh9sj，DOI [10.17605/OSF.IO/MH9SJ](https://doi.org/10.17605/OSF.IO/MH9SJ)；原始数据论文 Scientific Data 2020，DOI [10.1038/s41597-020-00622-y](https://doi.org/10.1038/s41597-020-00622-y)。官方说明CC BY 4.0。OSF API可直接读取公开文件树，无需注册/机构审批；Simula官方仓库也指向此OSF资源。

已经做的实测：
- 从官方OSF下载`video-labels.csv`，37,107字节；成功解析374条视频标签记录、30种Finding 1值；60条记录有第二个Finding字段（按CSV的非空字段计）。标签主类别数：{dict(collections.Counter(r['Classification 1'] for r in rows))}；上/下消化道记录数：{dict(org)}。
- 从官方OSF视频文件树选取一段标注为polyps的AVI，2,839,552字节，实际下载成功并解码：720×576、25fps、60帧；该条另有`lipoma?`标签，体现多标签歧义需要保留。
- 全部视频压缩数据约32.5GB，374段、约9.78小时、889,372帧；全HyperKvasir（含图像及其他记录）约66.4GB。只做视频任务无需先下全量图像，但全部视频仍是数十GB。单卡训练以抽帧/预提CLIP特征开展有希望，完整训练吞吐和工作盘容量尚未测，不能承诺开箱即跑。
- 数据匿名化，没有患者ID可供患者级分组。最低限度按唯一视频UUID分组，不能宣称患者级外部泛化；同一患者多段视频的潜在重合无法在当前标签文件中排除。

## 3．已有方法初查与基线选择

**任务特定工作（强相关，优先读）：** 上述KRCL 2025直接在Hyper-Kvasir做文本到视频检索。原文报告KRCL R@1 22.0、R@5 46.8、R@10 52.8；KRCL-IT为23.1/45.6/53.5。MeanPool视频帧聚合R@1 22.0；Transformer聚合22.7/47.1/53.5。该文已经覆盖“CLIP图文知识迁移＋时间聚合＋标签提示”这一类组合。本轮按题名、作者和KRCL查询GitHub未定位其官方训练仓库；只能说未定位，不能断言作者从未公开。

**可核查代码基线：** CLIP4Clip（ArrowLuo，2021），[官方GitHub](https://github.com/ArrowLuo/CLIP4Clip)，MIT许可证。仓库已下载并检查，含`main_task_retrieval.py`、完整视频-文本数据加载器、CLIP/跨模态网络、训练/评估循环、检索R@K等评价及预处理脚本；支持MeanPool、LSTM、Transformer等时间聚合。不是Hyper-Kvasir专用代码，需要新增读取video-labels与标签文本的数据适配器。

代码风险已检查：README使用PyTorch 1.7.1并示例多GPU；主程序初始化分布式进程组，单卡需要用单进程启动验证。训练循环当前有基于test_dataloader挑checkpoint的实现风险，正式比较需改为独立验证集选模型、锁定测试集。以上是适配工作，不算论文贡献。CLIP预训练权重与第三方权利条件需下载前确认；本轮没有运行训练。

**初查热度判断：** 在你给的94篇文章中有一篇完全相同数据/任务的2025论文，故不能称空白，也必须将KRCL作为强相关对照。跨领域近作还包括手术视频检索、GI内镜内容检索、Endo视频语言模型；医学视频/多模态基础模型整体活跃。不过在HyperKvasir视频级“标签文本→视频检索”这一窄设定，本轮初查到的直接工作较少，暂定为“有直接竞争、总体中等活跃”，不是低热度保证。搜索不是穷尽证明。

SOP 3的结论：数据与可用代码管线有依据，且资源投入表面可控；**候选可进入下一步基线适配/小规模训练**。但只有一个完全同任务的近期强工作且其代码未定位，CLIP4Clip需改数据适配并修评估口径。因此若必须“原作者官方方法代码开箱、零适配”，此候选不满足；若允许公开通用强基线做明确数据适配，则可继续。

## 不做的结论

- 不把“只有一篇直接论文”写成没人做。
- 不将KRCL的论文数字与自跑结果当同协议公平比较，先重建相同视频列表、标签处理和划分。
- 不把视频级检索结果称为关键帧定位或临床诊断。
- 不声称已经找到改进点或保证涨点。SOP第4步跑可信基线后，再用验证集错误与成本决定是否继续。

## 下一步（只到SOP第4步入口）

先从video-labels构造明确的单标签/多标签检索评估协议，并固定按视频UUID的70/10/20划分；检查现有Hyper-Kvasir仓库中的官方split是否适用于视频记录。适配CLIP4Clip视频读取入口和标签prompt，先抽样1—2个batch完成前向/损失/排名指标冒烟；随后跑CLIP zero-shot/冻结特征与微调基线。测试集在阈值、prompt、checkpoint选定中保持锁定。跑通并核对后才进入SOP第4/5步；此任务卡没有提出模块创新。

原始材料与实测证据：`C:/lunwen/research_audit/topic_selection_nov23/`（OSF标签CSV、OSF目录清单、AVI样本、解码记录、CLIP4Clip代码ZIP、官方仓库README、文献检索结果）。
'''
(out/'选题任务卡_SOP前3步.md').write_text(text,'utf-8')
print(out/'选题任务卡_SOP前3步.md')
