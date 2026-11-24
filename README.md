# lunwengit

医学多模态影像方向的论文阅读、选题审计与研究资料库。

## 目录结构

```
lunwengit/
├── *.pdf                          # 论文 PDF 库（多模态融合 / 分割 / 配准 / VQA / 报告生成等）
├── output/                        # 阶段性产出
│   ├── 医学多模态论文阅读_2026-11-22/        # 94 篇逐篇提取 + 选题 SOP v4 + 证据审计
│   ├── 医学多模态选题SOP_执行版_2026-11-23/   # SOP 执行版 + 规则修订依据
│   ├── 选方向_CDD-CESM_2026-11-22/           # 方向任务卡与撞车核查证据
│   ├── 选方向_EEG-fNIRS_2026-11-22/          # 数据实测与可行性复核
│   └── 选题初筛_内镜视频文本检索_2026-11-23/
└── research_audit/                # 各选题方向的审计脚本、数据核查与证据留存
    ├── new_direction_20261122/
    ├── pancreatic_ct_cbct_sop/
    ├── resect_sop_20261124/
    ├── picai_sop_20261123/
    ├── topic_selection_nov23/
    ├── topic_selection_2026_11_22/
    ├── corpus_2025_2026/
    └── CoRe-Sleep/ SleepDG/ evid_multimodal_ehr/   # 第三方参考实现
```

## 说明

- `research_audit/` 下的脚本主要用于文献撞车核查、数据集可达性实测、方向可行性验证。
- 第三方代码 `CoRe-Sleep`、`SleepDG`、`evid_multimodal_ehr` 为公开仓库的代码副本，用于对照实验设计。
- 依赖目录（`python_deps/`、`deps/`）未纳入版本库，复现时请按各自 `requirements.txt` 重新安装。

## 研究方向

多模态医学图像融合、跨模态配准、病灶分割、医学视觉问答与报告生成，关注数据可达性与撞车风险的前置核查。
