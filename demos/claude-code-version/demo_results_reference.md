# ARIS Claude Code 版本 — 预期结果参考

> 本文件记录了在 Cursor 版本中实际运行各 Skill 的结果，
> 供你在 Claude Code 中运行时对照参考。

---

## 1. `/arxiv` — arXiv 搜索结果参考

### 搜索词: "drug toxicity neural network prediction"

| # | arXiv ID | 标题 | 日期 | 分类 |
|---|----------|------|------|------|
| 1 | 1609.04846 | A Tutorial about Random Neural Networks in Supervised Learning | 2016-09-15 | cs.NE |
| 2 | 2502.01654 | Predicting concentration levels of air pollutants... | 2025-01-30 | cs.LG |
| 3 | 2212.06370 | Dual Accuracy-Quality-Driven Neural Network... | 2022-12-13 | cs.LG |
| 4 | **2403.18997** | **Quantum to Classical Neural Network Transfer Learning Applied to Drug Toxicity Prediction** | 2024-03-27 | quant-ph |
| 5 | 1902.04996 | Structured penalized regression for drug sensitivity prediction | 2019-02-13 | stat.ME |

**第 4 篇是最相关的** — 直接讨论药物毒性预测的深度学习方法。

### 搜索词: "Hodgkin-Huxley parameter estimation single cell"

| # | arXiv ID | 标题 | 日期 | PDF 大小 |
|---|----------|------|------|---------|
| 1 | 1106.4317 | Self-organizing state-space model for HH parameter estimation | 2011-06-21 | 8,479 KB |
| 2 | 1811.00173 | Structure-preserving integrators for HH systems | 2018-11-01 | 1,205 KB |
| 3 | 2601.14579 | Lie Group Basis of Neuronal Membrane Architecture | 2026-01-21 | 488 KB |

---

## 2. `/research-review` — GPT-5.4 审稿结果参考

### 被审查的项目: VirtualCellPlatform

**评分: 3/10 (Not Ready)**

**8 个弱点摘要:**

| # | 严重程度 | 弱点 | 最小修复方案 |
|---|---------|------|------------|
| 1 | FATAL | 核心映射不可识别（mRNA≠蛋白质≠功能活性） | 改为预测可观测表型或参数后验 |
| 2 | FATAL | 监督目标循环（用模型输出训练模型） | 用直接可测量的指标做基准 |
| 3 | FATAL | 评估不可信（只有训练R²） | 报告测试集+基线对比 |
| 4 | FATAL | 仿真缺乏实验验证 | 端到端验证一个真实药物 |
| 5 | MAJOR | 范围过大（5种细胞太多） | 砍到1种+1个用例 |
| 6 | MAJOR | ML贡献不清晰 | 定义一个技术贡献+消融 |
| 7 | MAJOR | 性别差异不够严谨 | 补充统计检验 |
| 8 | MAJOR | 缺乏不确定性量化 | 预测分布+传播不确定性 |

**核心建议:** "删掉 70-80% 的范围，证明一个窄论点"

---

## 3. `/research-lit` — 文献综合分析参考

### GPT-5.4 识别的 4 大研究方向

1. **数字孪生基础设施** — DTaaS, DT Cost Reduction
2. **单细胞表示与微环境** — scMamba, CellPhoneDB v5
3. **机制动力学建模** — HH参数估计, 基因表达生物物理
4. **化合物中心筛选** — 片段描述符, QSAR

### WebSearch 发现的最新竞争者

| 名称 | 来源 | 核心 |
|------|------|------|
| TwinCell | bioRxiv 2026 | 大规模因果细胞模型 |
| VCWorld | OpenReview | 白盒细胞仿真器+LLM |
| GENEVA | Nature Cancer 2026 | 单细胞药物反应平台 |

### GPT-5.4 建议的 5 个新方向

1. 扰动原生虚拟细胞孪生
2. 混合机制-神经网络孪生
3. 空间多细胞毒性孪生
4. 联合药物-细胞模型
5. 闭环主动学习孪生

---

## 4. `/novelty-check` — 新颖性验证参考

### 被验证的创意: PNVCT

**判定: PARTIALLY NOVEL**

| 差异化点 | 判定 | 已有工作 |
|---------|------|---------|
| 直接在扰动数据上训练 | ❌ 不新颖 | CPA (2022) |
| 毒性终点作为损失函数 | ⚠️ 部分新颖 | — |
| 基础模型嵌入 | ❌ 不新颖 | scOTM (2025) |
| 剂量-时间分辨率 | ❌ 不新颖 | CPA (2022) |

**8 个最相似已有工作:** chemCPA, GEARS, biolord, PerturbNet, State, SIMCO, scOTM, Decoding Stress States

**更安全的声称:** "端到端毒性监督虚拟细胞模型"

---

## 5. 在 Claude Code 中运行时的预期差异

| 方面 | Cursor 版本 | Claude Code 版本 |
|------|------------|-----------------|
| 命令格式 | 自然语言 / Python 脚本 | `/skill名 "参数"` |
| Codex MCP | 通过 Cursor AI 调用 | Claude 自动调用 |
| 输出格式 | AI 对话框 + 文件 | 终端文本 + 文件 |
| 文件保存 | 自动 | 自动（IDEA_REPORT.md 等） |
| 运行时间 | 相同 | 相同 |
| 审稿结果 | 相同（同一个 GPT-5.4） | 相同 |

**核心区别：** Claude Code 中所有步骤自动串联，不需要你手动运行 Python 脚本。
