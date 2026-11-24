from pathlib import Path
p=Path(r'C:\lunwen\output\选方向_CDD-CESM_2026-11-22');p.mkdir(parents=True,exist_ok=True)
t='''# 本轮选方向记录：增强乳腺双影像良恶性分类

日期：2026-11-22。
依据：桌面《论文选题SOP_重塑版.md》，按“互补预测”路线推进。本文是方向选择和先导实验任务卡，未宣称实验涨点、机制创新或可录用。

## 方向决定

优先候选：同一乳房低能影像（LE/数据中DM）与减影影像（DES/数据中CM、CESM）的良恶性分类。
两类影像来自同次双能增强乳腺检查；减影图由低/高能曝光重组计算得到，不应写成两个独立检查。
临床动机：低能图保留形态、结构及钙化信息，减影图呈现增强信息；两者有互补的可能，但在本数据上的增益仍要由单影像/双影像实验确认。

暂定任务表述：面向乳腺良恶性鉴别的低能—减影影像互补学习。正式题名和主要改进在实验后确定。

## 已实际核查的数据

官方：TCIA CDD-CESM，326位女性，2006张JPG，1003张低能及1003张减影，官方标示1.49GB、CC BY 4.0。不是2006位独立患者。官方公开包不要求医院合作或新标注。
已经下载并解析官方annotations.xlsx（244539字节）、segmentation.csv（1015109字节）；已经下载作者代码ZIP并检查分类加载器及划分脚本。

标注表实算：2006行、326个患者ID、566个乳房侧；1001个患者-侧别-视图组，均包含两种影像。分组数与1003对名义数的区别包含重复采集，正式清单需在影像落盘后逐文件确认。
435个乳房侧同时有CC/MLO和两类影像，其余131个侧缺一个视图。50个侧的可用影像标签集合不完全相同，不能直接把每张图视为拥有一致的侧别病理标签。
按2026 Journal of Imaging论文的既有规则，在同一侧按 Malignant > Benign > Normal 聚合，得到：Normal189侧、Benign194侧、Malignant183侧。排除Normal后为377侧，涉及284位患者。这是按规则推导的任务样本数，不等于377个独立患者或377个独立病灶。聚合标签沿用数据标签，不等于对所有侧重新核实了组织病理。

下载实况：已打开官方Aspera公开包，页面列出2007个文件及“Files on server: Yes”。跳过客户端安装后显示Transfer unavailable。当前未安装客户端、未下载完整影像、未逐例打开真实配对JPG；因此“数据已验收”和“开箱即跑”均不成立。Aspera客户端是明确的下载前置条件，不是数据申请审批。

正式训练前：完成官方影像获取；核对图名、重复采集、侧别/视图/影像类型、标签；固定纳入排除标准（含术后/治疗病例处理）；打开至少若干完整病例检查；建立患者级清单。官方作者代码中的split_train_test.py按图像行拆分，不能直接沿用。

## 第一次撞车核查

已使用OpenAlex/Crossref、PubMed/EuropePMC、PMC全文及官方仓库查询。查询包括CDD-CESM、contrast enhanced mammography benign malignant multimodal fusion、cross-energy feature fusion contrast mammography；检索时间范围2024-01-01至2026-11-22，并补读2022数据论文。OpenAlex原始命中混入无关CESM缩写，不能把原始计数当论文热度。

1. Categorized contrast enhanced mammography dataset for diagnostic and artificial intelligence research；Scientific Data，2022；LE/DES与报告标注；数据及分类/分割基线。已读全文和作者代码。官方实现为旧TensorFlow单图分类等工具，不是现成现代双影像融合强基线，5090兼容性未验证。
2. Multi-modal classification of breast cancer lesions in Digital Mammography and contrast enhanced spectral mammography images；Computers in Biology and Medicine，2024；DM+CM、CC/MLO；正常异常及良恶分类，JointNet与Attention on Lesion管线。已读正式摘要，全文为订阅访问，尚未定位公开完整代码。它是直接竞争，摘要中的高分不能在不核对ROI监督、患者划分、任务单位的情况下与新实验直接比较，也不能无视。
3. Improving Benign and Malignant Classifications in Mammography with ROI-Stratified Deep Learning；Bioengineering，2025；乳腺影像/ROI存在性分层；良恶分类。已通过PMC BioC读全文。CDD-CESM没有预定义划分，作者采用10:1 train/test；本次未在全文定位公开代码或明确患者分组说明。该工作利用ROI是否存在进行分流，不能与只用影像的设置不加说明地混比。
4. Calibrated Transformer Fusion for Dual-View Low-Energy CESM Classification；Journal of Imaging，2026；只有低能CC/MLO；正常vs异常（良恶合并），五折患者分组。已读PMC全文。AUC0.9915是不同任务，不能作为良恶性分类的成绩上限。侧别聚合、缺视图、重复采集处理可作为协议参考。
5. Dual-view and dual-modality fusion in contrast-enhanced spectral mammography for breast-side classification: a patient-grouped evaluation；Clinical Radiology，2026；双视图+双影像；正常vs异常。已核对正式摘要：326患者/566侧，277患者交叉验证、49患者独立留出，Transformer融合、缺输入处理、MC dropout和校准；CV AUC0.993，留出AUC0.985。非良恶分类，但融合机制是直接竞争。全文/公开实现尚未核实。
6. Improving Normal/Abnormal and Benign/Malignant Classifications in Mammography with ROI-Stratified Deep Learning；Bioengineering，2026；多种乳腺数据、ROI存在性分层、多个强骨干；已读PMC BioC全文。需作为现代骨干和ROI输入条件的对照参考，不能把“换ConvNeXt/Swin”当本课题创新。
7. Masked complex non-decimated wavelet features for patient-level classification of contrast-enhanced mammography；arXiv 2607.02394，2026；低能/减影、患者级聚合、正常vs恶性；本轮已读摘要，未读全文。提示患者级无泄漏评价已有工作，不能主张自己首次提出患者分组。

竞争判断：这个具体任务已有多条研究路线，属于有竞争的候选，不能称冷门、空白或证明无人解决；本轮没有建立可信的全量热度统计。推荐理由是任务、标签及公开数据入口具体，2D计算规模适合单卡，已有任务对照可循；不因只有一个直接邻近方法就否决，但也不以“中文核心”降低公平对照要求。

## 首轮实验任务卡

输入：LE、DES；暂不输入诊断报告、BI-RADS、人工病灶mask。报告和BI-RADS带诊断信息，额外监督/推理条件必须单列。CC/MLO均属视图，不应靠把视图当模态来论证多模态必要性。
输出：侧别良性/恶性概率。先固定任务单位和标签规则，缺视图处理不随方法改变。
划分：所有左右侧、CC/MLO及重复图都随患者分组。先在开发训练/验证划分建立管线，测试数据不用于挑问题、调参或选择模块；最终采用预先锁定的患者级交叉验证/嵌套验证方案，报告患者聚类不确定性。

基线矩阵：
- ImageNet预训练现代骨干（例如ResNet50及ConvNeXt-Tiny），分别训练LE-only、DES-only；验证集确定训练设置，不能用训练不足制造弱基线。
- 相同骨干、输入分辨率、训练预算下的双分支特征拼接和预测后融合。
- 任务相关强融合：查清JointNet/AOL及2026Transformer融合的输入和监督，定位可用代码；无代码时只在完整方法可重建且预算可承受时独立实现，并清楚标注。不能把文献数字贴进自己的实验表冒充公平重跑。

当前没有一篇同时完成“近期任务强代码完整、5090实跑、患者协议复核”的唯一主基线验收。旧作者工具只用于数据和参考，不包装成已确定的强主基线。

主要指标：ROC-AUC、PR-AUC、灵敏度与特异度（阈值只在训练内部验证集选择）、balanced accuracy，另报参数/推理成本。评价不只依赖accuracy。先完成单/双影像与强融合对照，检查互补收益及融合后新增错误，再限定一个瓶颈。

待检验的问题：在不使用测试时人工ROI和诊断报告的条件下，双影像融合能否稳定胜过最强单影像，若不能，哪类证据冲突或信息丢失导致差距？这不是已经证实的缺陷，也不是机制创新声明。

若简单充分训练已解释所有收益，就不把它写成新算法。若具体瓶颈成立，才设计一个主要改动，并按SOP进行第二次跨器官、跨任务机制撞车核查。数据下载、标签规则或强对照若无法落实，停止此候选的正式立项，保留可复用的数据审计成果。

## 本轮决策边界

这是优先数据验收/先导实验方向，不是已满足全部条件的正式题目。尚未完成真实影像验收、近期强方法实现验收，也没有方法涨点证据。论文能否成立取决于之后在公平协议下的改进与充分比较。

## 来源

- 官方数据：https://www.cancerimagingarchive.net/collection/cdd-cesm/
- 数据论文：https://doi.org/10.1038/s41597-022-01238-0
- 官方工具：https://github.com/omar-mohamed/CDD-CESM-Dataset
- JointNet/AOL：https://doi.org/10.1016/j.compbiomed.2024.109266
- 2025 ROI分层：https://pmc.ncbi.nlm.nih.gov/articles/PMC12383514/
- 2026低能双视图：https://pmc.ncbi.nlm.nih.gov/articles/PMC12842785/
- 2026双影像双视图：https://doi.org/10.1016/j.crad.2026.107276
- 2026 ROI分层：https://pmc.ncbi.nlm.nih.gov/articles/PMC12938819/
- 2026小波患者级评价：https://arxiv.org/abs/2607.02394

原始网页、元数据、全文抽取、官方标注、代码与分组审计：C:/lunwen/research_audit/topic_selection_2026_11_22/。
补充比较候选：BRSET官方认证获取未通过“直接自助下载”要求；SHUS-CEUS未定位官方成品公开入口；Derm7pt官网本轮未取得有效下载页面；Prostate158有明确公开Zenodo及完整基线，但本轮未完成真实数据验收、近期强方法与竞争复核，不作为已合格备选。以上是本轮检查状态，不是断言数据永久不可得或整个任务不可做。
'''
(p/'方向任务卡与核查证据.md').write_text(t,encoding='utf-8')
print(p/'方向任务卡与核查证据.md')
