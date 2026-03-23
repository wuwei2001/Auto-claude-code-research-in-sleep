# ARIS 演示 — Cursor 版本（完整记录）

> **本文件夹包含在 Cursor IDE 中使用 ARIS Skills 的完整演示案例。**
> 
> 本文档记录了 2026-03-15 在 Cursor 中通过 Codex MCP 实际运行 ARIS Skills 的完整过程。
> 演示了 3 个核心 Skill：`/research-review`、`/arxiv`、`/research-lit`。
> 目的：验证 ARIS 双模型协作功能，并详细展示每一步发生了什么。

## 本文件夹包含

| 文件 | 说明 |
|------|------|
| `README.md` | 本文件 — 完整演示记录（含操作流程、审稿结果、文献分析） |
| `DEMO_REPORT.md` | 同内容备份 |
| **可运行的 Python 演示** | |
| `arxiv_search_demo.py` | `/arxiv` — arXiv 搜索 + PDF 下载（真实 API 调用） |
| `research_lit_demo.py` | `/research-lit` — 多源文献综述（arXiv + WebSearch 模拟 + 分类） |
| `research_review_demo.py` | `/research-review` — GPT-5.4 审稿（预录制 + 实际调用模式） |
| `novelty_check_demo.py` | `/novelty-check` — 新颖性验证（预录制结果） |
| `idea_creator_demo.py` | `/idea-creator` — 创意生成（预录制的 5 个创意） |
| `workflow_demos.py` | 所有 Workflow 模拟（9 个: idea-discovery, auto-review, paper-writing, pipeline, paper-plan, paper-compile, analyze-results, run-experiment, feishu-notify） |
| `run_all_demos.py` | **统一运行器** — 交互式菜单 / 按等级 / 快速演示 / 指定 ID |

## 快速使用

```powershell
# 方法 1: 交互式菜单（推荐）
python run_all_demos.py

# 方法 2: 快速演示（每级各一个）
python run_all_demos.py --quick

# 方法 3: 运行特定脚本
python arxiv_search_demo.py "drug toxicity prediction"
python arxiv_search_demo.py "virtual cell modeling" --max 10 --download-all
python research_lit_demo.py "single cell drug toxicity" --save
python research_review_demo.py --demo
python novelty_check_demo.py --demo
python idea_creator_demo.py
python workflow_demos.py all

# 方法 4: 在 Cursor AI 对话中使用
#    输入："请用 Codex MCP 调用 GPT-5.4 审查我的研究项目..."
#    输入："请按照 research-lit skill 帮我做关于 XX 的文献综述"
```

---

## 一、演示背景

### 1.1 什么是这次演示

这次演示模拟了 ARIS 的 **`/research-review` Skill**（单轮深度审稿）的完整执行过程：

```
Claude（在 Cursor 中运行）
  ↓ 准备审稿材料
  ↓ 通过 Codex MCP 发送给 GPT-5.4
  ↓
GPT-5.4 xhigh（OpenAI 的最强推理模型）
  ↓ 以 NeurIPS/ICML 顶会审稿人身份审查
  ↓ 返回评分 + 弱点分析 + 修改建议
  ↓
Claude 接收并记录审稿结果
  → 保存到 AUTO_REVIEW_DEMO.md（本文件）
```

### 1.2 被审查的项目

| 项目信息 | 内容 |
|---------|------|
| **项目名** | VirtualCellPlatform（多尺度虚拟细胞建模与药物/毒物筛选平台） |
| **核心思路** | 用机器学习把单细胞组学数据（scRNA-seq 等）映射到生物物理参数，建立虚拟细胞数字孪生体，模拟药物/毒物暴露下的细胞行为 |
| **已有结果** | 合成数据 R²=0.47，真实数据 R²=0.36，TDCIPP 毒性仿真有性别差异 |
| **目标会议** | NeurIPS / ICML（机器学习顶会） |

### 1.3 涉及的技术栈

| 组件 | 作用 | 本次使用情况 |
|------|------|------------|
| **Claude Code / Cursor** | 执行者——准备材料、解析结果、实施修改 | ✅ 在 Cursor 中执行 |
| **Codex MCP** | 桥梁——把审稿请求转发给 GPT-5.4 | ✅ 通过 `mcp__codex__codex` 调用 |
| **GPT-5.4 xhigh** | 审查者——以顶会审稿人身份审查 | ✅ 返回了完整审稿意见 |
| **SKILL.md** | 指令文件——告诉 Claude 按什么步骤执行 | ✅ 按照 research-review 流程 |

---

## 二、执行过程详解

### Step 1: Claude 准备审稿材料

**这一步做了什么：** Claude（我）读取项目的 README.md、代码结构、已有结果，整理成结构化的审稿材料。

**具体准备的内容：**

```
发送给 GPT-5.4 的审稿材料包括：

1. 项目标题和核心思路
   → "VirtualCellPlatform: Multi-scale Virtual Cell Modeling and Drug/Toxin Screening"

2. 关键技术组件（4个）
   → OmicsToParams: ML 模型（组学 → 生物物理参数）
   → 多过程仿真引擎（电生理、钙动力学、代谢、信号通路、细胞周期、膜动力学）
   → 5种细胞类型（神经元、心肌细胞、肝细胞、β细胞、上皮细胞）
   → 药物筛选流水线（剂量-反应、灵敏度分析、异质性分析）

3. 当前实验结果
   → 合成数据训练 R² = 0.47
   → 真实数据（Allen Brain Atlas Patch-seq, 2333 细胞）R² = 0.36
   → TDCIPP 神经毒性仿真：DA 神经元 ♂ AP 幅度 -19.7% vs ♀ -5.5%

4. 数学框架
   → Hodgkin-Huxley 方程
   → 钙动力学双池模型
   → Hill 方程（药物效应）

5. 审稿指令
   → "请以 NeurIPS/ICML 资深审稿人身份审查"
   → "打分 1-10，列出弱点，给出最小修复方案"
   → "要求残酷诚实"
```

### Step 2: 通过 Codex MCP 发送给 GPT-5.4

**这一步做了什么：** 调用 `mcp__codex__codex` 工具，设置 `model_reasoning_effort: "xhigh"`（最高推理深度），把审稿材料发送给 GPT-5.4。

**技术细节：**
```
工具调用：mcp__codex__codex
参数：
  model: gpt-5.4
  config: { "model_reasoning_effort": "xhigh" }
  prompt: [上面准备的完整审稿材料]

xhigh 的含义：GPT-5.4 会花更多"思考时间"，类似于 o3 的深度推理模式。
这个参数让审稿更深入、更严格，但也更慢、更贵。
```

**等待时间：** 约 20-30 秒（xhigh 模式比标准模式慢 3-5 倍）

### Step 3: GPT-5.4 返回审稿结果

**GPT-5.4 返回了完整的结构化审稿意见。以下是逐项详细分析：**

---

## 三、GPT-5.4 审稿结果详解

### 3.1 总体评分

| 指标 | 结果 |
|------|------|
| **评分** | **3/10** |
| **判定** | **Not Ready（未准备好）** |
| **目标水准** | NeurIPS / ICML 顶会 |

**3/10 意味着什么？**
- 1-3 分：基本不具备投稿条件，需要根本性重构
- 4-5 分：有潜力但重大问题多，需要大量修改
- 6-7 分：Almost ready，修改后可投
- 8-10 分：强论文，可直接投稿

当前 3 分说明项目虽然方向好，但在方法论、实验验证、论文聚焦方面有根本性问题。

### 3.2 优势（Strengths）— GPT-5.4 认可的部分

GPT-5.4 给出了 5 个优势：

| # | 优势 | 解读 |
|---|------|------|
| 1 | **问题重要**：把单细胞状态与扰动下的功能响应联系起来，科学上有意义且高影响力 | 研究方向选得好，有实际价值 |
| 2 | **机制角度正确**：纯黑箱预测在这个领域效果差，生物物理仿真结构能带来真正的优势 | 方法论方向对，不是简单的深度学习 |
| 3 | **Patch-seq 起点合理**：Patch-seq 数据同时包含转录组和电生理，是做这种映射的理想数据 | 数据选择好 |
| 4 | **异质性感知的筛选**是比均值细胞预测更好的框架，可以成为强的 biology/ML 贡献 | 异质性分析是亮点 |
| 5 | **平台愿景有吸引力**，作为长期愿景是好的（但目前反而伤害了论文） | 想法很好，但执行太散 |

### 3.3 弱点（Weaknesses）— 详细分析每一条

#### 弱点 1: [致命] 核心映射不可识别

```
问题：从转录组数据无法唯一恢复 HH 电导参数和酶动力学常数。
       多种参数组合可以产生相似的表型，而且 mRNA 水平与实际电导/动力学常数
       只有弱相关性。

通俗解释：
  你试图从"基因表达量"推断"离子通道的电导值"，
  但同样的基因表达可以对应很多不同的电导值（一对多映射），
  而且 mRNA 数量 ≠ 蛋白质数量 ≠ 功能活性。
  这是一个"不适定问题"（ill-posed problem）。

最小修复方案：
  ① 不再声称"直接从组学恢复隐藏参数"
  ② 改为：
     - 预测可观测表型（如 AP 幅度、放电频率）
     - 或者推断参数的后验分布（贝叶斯方法），
       并展示可识别性分析

严重程度：致命（FATAL）— 不修复这个，论文不可能接受
```

#### 弱点 2: [致命] 监督目标不清晰且可能循环

```
问题：如果 Patch-seq 的"真实参数"是通过拟合电生理模型获得的，
       那你其实是在"用模型拟合结果训练另一个模型"——
       训练标签本身就是有噪声的推断值，不是真实值。

通俗解释：
  你用 HH 模型拟合电生理记录得到一组参数（比如 gNa=120），
  然后用这组参数作为"标签"训练 ML 模型。
  但 gNa=120 本身就不一定准确——它只是拟合结果。
  这相当于"循环论证"：用模型的输出训练另一个模型预测同一个输出。

最小修复方案：
  ① 明确标注监督目标是什么（拟合参数 vs 直接测量值）
  ② 优先用直接可测量的指标做基准测试：
     AP 幅度、放电频率、尖峰宽度、适应性等
  ③ 把"隐藏参数推断"降级为次要的潜变量分析

严重程度：致命（FATAL）
```

#### 弱点 3: [致命] 评估不可信

```
问题：只报告了训练 R²（合成 0.47，真实 0.36），
       没有测试集、交叉验证、基线对比。
       训练 R² 这么低本身就是红旗——
       说明要么任务不适定，要么模型没学到有用信号。

通俗解释：
  你告诉审稿人"我的模型训练准确率 47%"，
  但没说测试准确率是多少、跟简单方法比怎么样。
  审稿人会想：如果连训练集都只有 47%，测试集可能更差。
  而且没有基线对比，47% 到底是好是坏都无法判断。

最小修复方案：
  ① 报告留出测试集的表现（不是训练集！）
  ② 按捐赠者/标本分割数据（防止数据泄漏）
  ③ 报告不确定性区间和校准曲线
  ④ 与强基线对比：
     - 线性模型
     - 树模型（XGBoost/LightGBM）
     - MLP
     - 多模态基线
     - 纯机制模型基线

严重程度：致命（FATAL）
```

#### 弱点 4: [致命] 仿真声称缺乏验证

```
问题：TDCIPP 性别差异仿真结果（♂ -19.7% vs ♀ -5.5%）
       没有与真实实验数据对比。
       仿真说了不算——必须与实验数据匹配才有意义。

通俗解释：
  你的仿真器输出"男性神经元受影响更大"，
  但这是仿真器说的，不是实验证明的。
  如果不与真实的 TDCIPP 暴露实验数据对比，
  这个结果没有说服力——可能只是仿真器的 artifact。

最小修复方案：
  ① 找到一个有真实剂量-反应数据的扰动实验
  ② 端到端验证：组学输入 → 参数预测 → 仿真输出 → 与实验对比
  ③ 一个扎实的案例研究 > 十个推测性仿真

严重程度：致命（FATAL）
```

#### 弱点 5: [重大] 论文范围过大

```
问题：5 个细胞类型 + 6 个动力学模块 + 筛选平台 = 太多了。
       结果就是每个部分都浅尝辄止，没有深入验证。

通俗解释：
  顶会论文的标准是"一个问题做深做透"，
  不是"展示一个大平台"。
  你现在有 5 种细胞类型，但每种都只有初步结果。
  审稿人宁愿看一种细胞类型的深入验证，
  也不想看 5 种的浅层展示。

最小修复方案：
  ① 砍到 1 种细胞类型
  ② 砍到 1 个功能子系统
  ③ 砍到 1 个扰动用例
  ④ 其他全部放到 Future Work

严重程度：重大（MAJOR）
```

#### 弱点 6: [重大] ML 贡献不清晰

```
问题："平台 + 仿真器 + 预测器"不足以构成一个 ML 贡献。
       目前看起来像是"已知组件的集成"，不是方法创新。

最小修复方案：
  ① 定义一个清晰的技术贡献，例如：
     - 仿真器约束的潜变量推断
     - 可微分机制正则化
     - 不确定性感知的参数后验估计
  ② 对这个贡献做消融实验（ablation study）

严重程度：重大（MAJOR）
```

#### 弱点 7: [重大] 性别差异结果不够严谨

```
问题：♂ AP -19.7% vs ♀ -5.5% 没有样本量、置信区间、
       统计检验、训练数据的性别平衡信息。

最小修复方案：
  ① 报告样本量
  ② 报告置信区间
  ③ 做统计检验（t-test, Mann-Whitney 等）
  ④ 检查训练数据中男女比例是否平衡
  ⑤ 提供外部生物学依据

严重程度：重大（MAJOR）
```

#### 弱点 8: [重大] 缺乏不确定性量化

```
问题：在这种设置下，点估计是危险的。
       参数推断的误差会通过非线性仿真器放大。

通俗解释：
  如果参数估计有 10% 的误差，
  通过非线性 HH 方程仿真后，
  AP 波形的误差可能是 50% 或更大。
  不报告不确定性，就无法知道结果到底可不可信。

最小修复方案：
  ① 预测参数分布而非点估计
  ② 通过仿真传播不确定性
  ③ 报告药物响应输出的不确定性

严重程度：重大（MAJOR）
```

### 3.4 GPT-5.4 给出的最小可行改进方案

GPT-5.4 最后给出了一个非常直接的建议：

> **"最小可发表路径不是'完成平台'，而是'删掉 70-80% 的范围，令人信服地证明一个窄论点。'"**

具体来说：

```
最小改进方案（5 步）：

Step 1: 缩窄范围
  → 只做一个可行的论点，例如：
    "Patch-seq 神经元状态 → 电生理表型 / 扰动响应预测"
  → 删掉心肌细胞、肝细胞、β细胞、上皮细胞

Step 2: 修正核心方法
  → 不再说"组学直接预测隐藏生物物理参数"
  → 改为：
    选项 A: 预测可观测表型（AP 幅度等）
    选项 B: 推断参数后验分布 + 可识别性分析

Step 3: 建立可信评估
  → 留出测试集（按捐赠者/标本分割）
  → 与强基线对比
  → 做消融实验
  → 做校准分析

Step 4: 端到端验证
  → 找一个有真实数据的药物/毒物
  → 验证：组学 → 预测 → 仿真 → 与实验对比

Step 5: 重新定位贡献
  → 从"展示平台"变成"提出一个方法"
  → 平台作为实现载体，不是贡献本身
```

---

## 四、这在完整的 `/auto-review-loop` 中会怎样

如果运行完整的 `/auto-review-loop`（而不是单轮 `/research-review`），Claude 会按以下流程自动迭代：

```
Round 1 (刚才演示的)
┌─────────────────────────────────────────────────────────────────────┐
│ GPT-5.4 审稿 → 3/10, NOT READY                                    │
│                                                                     │
│ 8 个弱点，4 个致命                                                  │
│                                                                     │
│ Claude 自动采取的修改措施（预计）：                                   │
│ ├─ [弱点5] 砍掉 4 种细胞类型，只保留神经元                          │
│ ├─ [弱点3] 实现留出测试集 + 基线对比（线性/XGBoost/MLP）            │
│ ├─ [弱点6] 重写 Contribution 部分，聚焦一个技术点                   │
│ ├─ [弱点7] 补充样本量、置信区间、统计检验                           │
│ ├─ [弱点8] 添加蒙特卡洛不确定性传播                                 │
│ ├─ [弱点1] 改为预测可观测表型而非隐藏参数                           │
│ └─ [弱点2] 明确标注监督目标                                         │
│                                                                     │
│ 预计弱点 4（端到端验证）因为需要外部实验数据而被跳过                  │
│ → 标记为 "needs manual follow-up"                                   │
│                                                                     │
│ 保存 REVIEW_STATE.json:                                             │
│ { "round": 1, "score": 3, "status": "in_progress" }                │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
Round 2 (预计)
┌─────────────────────────────────────────────────────────────────────┐
│ Claude 把修改后的内容重新提交给 GPT-5.4                              │
│                                                                     │
│ GPT-5.4 re-审稿 → 预计 4.5-5.5/10                                  │
│                                                                     │
│ 预计剩余问题：                                                       │
│ ├─ 仍需端到端验证                                                   │
│ ├─ 基线对比还不够强                                                 │
│ └─ 消融实验还没做                                                   │
│                                                                     │
│ Claude 继续修改...                                                   │
│ 保存 REVIEW_STATE.json:                                             │
│ { "round": 2, "score": 5, "status": "in_progress" }                │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
Round 3 (预计)
┌─────────────────────────────────────────────────────────────────────┐
│ GPT-5.4 re-审稿 → 预计 5.5-6.5/10                                  │
│                                                                     │
│ 如果 ≥ 6 且判定 almost/ready → 停止循环 ✅                          │
│ 如果 < 6 → 继续 Round 4                                             │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
Round 4 (最终轮，预计)
┌─────────────────────────────────────────────────────────────────────┐
│ GPT-5.4 终审 → 预计 6-7.5/10                                       │
│                                                                     │
│ 最终判定：Almost Ready 或 Ready                                     │
│ 列出剩余的可选改进（not blocking submission）                        │
│                                                                     │
│ 保存 REVIEW_STATE.json:                                             │
│ { "round": 4, "score": 7, "status": "completed" }                  │
│                                                                     │
│ 生成最终 AUTO_REVIEW.md 总结                                        │
└─────────────────────────────────────────────────────────────────────┘

典型分数进展：3/10 → 5/10 → 6.5/10 → 7/10
典型耗时：2-8 小时（取决于修改复杂度和是否有实验要跑）
```

### 断点续传机制

```
如果在 Round 2 时 Claude Code 的上下文窗口满了（长时间运行会发生）：

① Claude 自动保存 REVIEW_STATE.json:
   { "round": 2, "threadId": "019cd392-...", "score": 5, "status": "in_progress" }

② 上下文被压缩，Claude 失去之前的记忆

③ 你重新运行 /auto-review-loop 时：
   Claude 检测到 REVIEW_STATE.json
   → 读取 round=2, threadId, score
   → 读取 AUTO_REVIEW.md 恢复历史上下文
   → 从 Round 3 继续
   → 使用 mcp__codex__codex-reply（带 threadId）保持 GPT 的对话上下文

这就是"断点续传"——即使崩溃/中断，也不会从头开始。
```

---

## 五、如何在你的电脑上运行完整流程

### 5.1 运行单轮审稿（快速，5-10 分钟）

```powershell
# 1. 打开终端
cd E:\Git-hub_project\Auto-claude-code-research-in-sleep

# 2. 启动 Claude Code
claude

# 3. 输入命令
> /research-review "VirtualCellPlatform: a multi-scale virtual cell modeling framework that maps single-cell multi-omics data to biophysical parameters for drug toxicity screening. Current results: R²=0.47 synthetic, R²=0.36 real data."

# 4. 等待 GPT-5.4 返回审稿意见（约 30 秒到 2 分钟）
# 5. 查看评分和修改建议
```

### 5.2 运行自动审稿循环（长时间，2-8 小时）

```powershell
# 1. 打开终端
cd E:\Git-hub_project\Auto-claude-code-research-in-sleep

# 2. 启动 Claude Code
claude

# 3. 输入命令
> /auto-review-loop "VirtualCellPlatform: multi-scale virtual cell modeling for drug toxicity screening"

# 4. 去睡觉 💤
# 5. 第二天早上查看：
#    - AUTO_REVIEW.md（完整审稿记录）
#    - REVIEW_STATE.json（最终状态）

# ⚠️ 重要：不要关闭终端窗口！不要让电脑休眠！
```

### 5.3 运行创意发现（中等时间，30-120 分钟）

```powershell
cd E:\Git-hub_project\Auto-claude-code-research-in-sleep
claude

> /idea-discovery "virtual cell digital twin for multi-organ drug toxicity prediction using single-cell omics"

# Claude 会自动执行：
# Phase 1: 文献综述（搜索 arXiv + Scholar + 本地论文）
# Phase 2: 创意生成（GPT-5.4 生成 8-12 个创意）
# Phase 3: 新颖性验证（检查是否已有人做过）
# Phase 4: 专家审查（GPT-5.4 审查）
# Phase 5: 输出 IDEA_REPORT.md
```

### 5.4 运行全流程一键（最长，一整晚）

```powershell
cd E:\Git-hub_project\Auto-claude-code-research-in-sleep
claude

> /research-pipeline "virtual cell digital twin for drug toxicity screening"

# 这会依次执行：
# Stage 1: /idea-discovery（30-60 min）
# Stage 2: 代码实现（15-60 min）
# Stage 3: /run-experiment（需要 GPU，没有则跳过）
# Stage 4: /auto-review-loop（1-4 h）
# Stage 5: 最终报告
```

---

## 六、关键产出文件说明

| 文件 | 由谁产生 | 内容 |
|------|---------|------|
| `IDEA_REPORT.md` | `/idea-discovery` | 排名创意报告（含 pilot 结果） |
| `AUTO_REVIEW.md` | `/auto-review-loop` | 完整审稿记录（每轮的评分、意见、修改） |
| `REVIEW_STATE.json` | `/auto-review-loop` | 断点续传状态（轮次、分数、threadId） |
| `PAPER_PLAN.md` | `/paper-plan` | 论文大纲（Claims-Evidence 矩阵） |
| `NARRATIVE_REPORT.md` | 你手写或 Claude 辅助 | 研究叙事（论文写作的输入） |
| `paper/main.pdf` | `/paper-writing` | 最终编译的论文 PDF |
| `PAPER_IMPROVEMENT_LOG.md` | `/auto-paper-improvement-loop` | 论文改进日志 |
| `LITERATURE_SUMMARY.md` | `/research-lit` | 文献综述总结 |

---

## 七、本次演示的环境信息

```
运行时间：2026-03-15 15:05-15:20
运行环境：Cursor IDE（Windows 10, build 26200）
执行模型：Claude (claude-4.6-opus) via Cursor
审稿模型：GPT-5.4 xhigh via Codex MCP
Codex CLI：v0.114.0 (E:\software\codex)
代理：http://127.0.0.1:7897
项目目录：E:\Git-hub_project\Auto-claude-code-research-in-sleep
```

---

## 八、总结

**ARIS 的双模型审稿确实有效。** 在这次演示中：

1. GPT-5.4 给出了 **3/10** 的严格评分——这不是"打击"，而是有建设性的
2. 8 个弱点中有 4 个是"致命"级别——说明项目确实需要根本性调整
3. 每个弱点都给出了**最小修复方案**——不是空洞的批评，而是可执行的建议
4. 最终的建议非常务实：**"删掉 70-80% 的范围，证明一个窄论点"**

如果用单模型（Claude 自己审自己），很可能不会这么尖锐。这就是双模型对抗审查的价值。

在完整的 `/auto-review-loop` 中，Claude 会自动实施修改、重新提交审稿、重复 4 轮，每轮分数逐步提升，直到达到可投稿水准。

---

## 九、`/arxiv` Skill 演示：多关键词论文搜索

### 9.1 执行过程

**这一步做了什么：** 模拟 ARIS `/arxiv` Skill 的功能，用 3 组关键词搜索 arXiv API。

**使用的搜索关键词：**
1. `"virtual cell digital twin drug screening"` — 虚拟细胞数字孪生
2. `"single cell omics biophysical modeling"` — 单细胞组学生物物理建模
3. `"Hodgkin-Huxley parameter inference transcriptomics"` — HH 参数推断

**技术实现：**
```python
# 1. 构建 arXiv API 查询 URL
url = "http://export.arxiv.org/api/query?search_query=..."

# 2. 通过代理（http://127.0.0.1:7897）发送请求
proxy = urllib.request.ProxyHandler({"http": "http://127.0.0.1:7897"})
opener = urllib.request.build_opener(proxy)

# 3. 解析 XML 响应，提取论文信息
root = ET.fromstring(response)
for entry in root.findall(f"{{{NS}}}entry"):
    # 提取 ID、标题、作者、日期、分类、摘要
```

### 9.2 搜索结果（9 篇论文）

| # | arXiv ID | 标题 | 日期 | 分类 | 搜索词 |
|---|----------|------|------|------|--------|
| 1 | 2305.07244 | Digital Twin as a Service (DTaaS): A Platform for DT Developers and Users | 2023-05-12 | cs.SE | virtual cell digital twin |
| 2 | 1311.3723 | Fragment Descriptors in Virtual Screening | 2013-11-15 | physics.chem-ph | virtual cell digital twin |
| 3 | 2107.14109 | Digital Twin As A Cost Reduction Method | 2021-07-10 | cs.OH | virtual cell digital twin |
| 4 | 1307.1009 | Systems Biophysics of Gene Expression | 2013-07-03 | q-bio.MN | single cell omics |
| 5 | 2311.04567 | CellPhoneDB v5: inferring cell-cell communication from single-cell multiomics | 2023-11-08 | q-bio.CB | single cell omics |
| 6 | 2506.20697 | scMamba: A Scalable Foundation Model for Single-Cell Multi-Omics Integration | 2025-06-25 | q-bio.CB, cs.LG | single cell omics |
| 7 | 1811.00173 | Structure-preserving numerical integrators for HH systems | 2018-11-01 | math.NA | HH parameter inference |
| 8 | 2601.14579 | The Lie Group Basis of Neuronal Membrane Architecture | 2026-01-21 | physics.bio-ph | HH parameter inference |
| 9 | 1106.4317 | Self-organizing state-space model for HH parameter estimation | 2011-06-21 | q-bio.QM | HH parameter inference |

### 9.3 这在真实的 `/arxiv` Skill 中是怎样的

```
在 Claude Code CLI 中：

> /arxiv "virtual cell digital twin drug screening"

Claude 会：
  ① 读取 ~/.claude/skills/arxiv/SKILL.md
  ② 找到 tools/arxiv_fetch.py 脚本（或用内联 Python 回退）
  ③ 调用 arXiv API 搜索
  ④ 展示结构化结果表格
  ⑤ 如果加了 "— download" 参数，还会下载 PDF 到 papers/ 目录
  ⑥ 建议后续 Skill：/research-lit、/novelty-check
```

---

## 十、`/research-lit` Skill 演示：文献综合分析

### 10.1 执行过程

**这一步做了什么：** 模拟 ARIS `/research-lit` Skill 的功能。先用 arXiv API 搜索（上面已完成），再用 WebSearch 补充网络文献，最后通过 Codex MCP 调用 GPT-5.4 做综合分析。

**搜索来源：**
```
来源 1: arXiv API 搜索 → 找到 9 篇论文
来源 2: WebSearch 网络搜索 → 找到 4 篇重要论文/平台

真实的 /research-lit 还会额外搜索：
来源 3: 本地 papers/ 目录中的 PDF
来源 4: Zotero（如果配了 MCP）
来源 5: Obsidian（如果配了 MCP）
```

### 10.2 WebSearch 补充的重要发现

通过 WebSearch 发现了 4 个非常重要的最新工作（arXiv 搜索没覆盖到的）：

| # | 名称 | 来源 | 日期 | 核心内容 |
|---|------|------|------|---------|
| 1 | **TwinCell** | bioRxiv | 2026-01 | 大规模因果细胞模型，整合单细胞基础模型嵌入与多组学互作组数据，用于治疗靶点优先排序 |
| 2 | **VCWorld** | OpenReview | 2025/2026 | 白盒细胞仿真器，结合结构化生物知识与 LLM，提供可解释的药物扰动预测 |
| 3 | **GENEVA** | Nature Cancer | 2026 | 可扩展的单细胞平台，汇集多个患者来源的细胞系研究药物反应 |
| 4 | **AI-driven Virtual Cell Models** | npj Digital Medicine | 2025 | AI虚拟细胞模型综述：整合多模态组学 + 深度生成模型 + 图神经网络 + 物理信息神经网络 |

**这些发现说明：** 你的 VirtualCellPlatform 方向是对的，但竞争很激烈——TwinCell 和 VCWorld 都在做类似的事情。

### 10.3 GPT-5.4 的文献综合分析

将搜索结果送给 GPT-5.4 xhigh 做综合分析后，GPT-5.4 识别出 **4 个主要研究方向** 和 **5 个未被覆盖的空白**：

#### 四大研究方向

```
方向 1: 数字孪生基础设施/经济学
  [DTaaS, DT Cost Reduction]
  → 关注部署、复用、监控，不解决生物学建模

方向 2: 单细胞表示与微环境推断
  [scMamba, CellPhoneDB v5]
  → 最接近目标问题
  → scMamba: 大规模多组学整合，不依赖高变异基因筛选
  → CellPhoneDB v5: 配体-受体推断、空间先验
  → 但都是描述性/推断性的，不是可执行的数字孪生

方向 3: 机制动力学建模
  [Systems Biophysics, HH Parameter Estimation, Structure-preserving Integrators, Lie Group]
  → 方向正确（可解释、可执行）
  → 但都是神经元或基因调控特异的，不是基于现代单细胞扰动数据

方向 4: 化合物中心的筛选
  [Fragment Descriptors]
  → 解决分子表示问题
  → 但不建模细胞状态或毒性机制
```

#### 关键发现：文献中的空白

```
GPT-5.4 指出的 5 个关键空白：

空白 1: 没有论文构建了"可执行的因果细胞模型"
  → 能预测药物暴露如何改变单细胞状态轨迹

空白 2: 没有论文联合建模"化合物结构 + 剂量 + 时间 + 靶点 + 细胞状态"
  → 这些通常是分开处理的

空白 3: 时间推断很弱
  → 大多数单细胞数据是破坏性快照，不是真正的时间序列

空白 4: 组织毒性需要多尺度整合
  → 细胞内调控 + 细胞间通信 + 空间上下文 + 表型

空白 5: 验证不足
  → 缺少不确定性量化、校准、前瞻性测试
```

#### GPT-5.4 建议的 5 个新研究方向

```
方向 1: 扰动原生虚拟细胞孪生
  → 基于剂量-时间分辨的单细胞扰动数据集训练
  → 以毒性终点为目标

方向 2: 混合机制-神经网络孪生
  → 结合基础模型嵌入与显式 GRN/信号动力学
  → 带校准的不确定性

方向 3: 空间多细胞毒性孪生
  → 整合单细胞多组学 + 配体-受体推断 + 组织病理学/成像

方向 4: 联合药物-细胞模型
  → 连接化合物结构、靶点网络、细胞状态转换和脱靶毒性

方向 5: 闭环主动学习孪生
  → 自动选择下一个最能减少不确定性的扰动实验
```

### 10.4 这在真实的 `/research-lit` Skill 中是怎样的

```
在 Claude Code CLI 中：

> /research-lit "virtual cell digital twin drug toxicity screening"

Claude 会：
  ① 读取 ~/.claude/skills/research-lit/SKILL.md
  ② 扫描本地 papers/ 目录中的 PDF
  ③ 搜索 arXiv API（结构化结果）
  ④ WebSearch 搜索 Google Scholar / Semantic Scholar
  ⑤ 如果配了 Zotero MCP → 搜索 Zotero 库
  ⑥ 如果配了 Obsidian MCP → 搜索 Obsidian 笔记
  ⑦ 去重合并所有来源的结果
  ⑧ 对每篇论文提取：问题、方法、结果、与我们的相关性
  ⑨ 综合分析：按主题分组、找共识和分歧、识别空白
  ⑩ 输出结构化文献表 + 叙述性总结
```

---

## 十一、完整的 ARIS 操作流程总览

### 11.1 从零开始到投稿的完整路径

```
┌──────────────────────────────────────────────────────────────────────┐
│                    ARIS 完整操作流程总览                              │
│                                                                      │
│  准备阶段（一次性）                                                  │
│  ├── 安装 Claude Code CLI: npm install -g @anthropic-ai/claude-code  │
│  ├── 安装 Codex CLI 并配置 model=gpt-5.4                            │
│  ├── 复制 ARIS Skills 到 ~/.claude/skills/                           │
│  ├── 配置 MCP: claude mcp add codex -- codex mcp-server             │
│  └── 开启 Auto-Allow（允许自动执行命令）                             │
│        ↑                                                             │
│        └── 你的环境已全部完成 ✅                                      │
│                                                                      │
│  使用阶段（每次科研任务）                                            │
│                                                                      │
│  Step 0: 准备项目目录                                                │
│  ┌──────────────────────────────────────────────────────┐            │
│  │ mkdir 你的研究项目                                    │            │
│  │ cd 你的研究项目                                       │            │
│  │ 创建 CLAUDE.md（项目说明，让 Claude 了解背景）         │            │
│  │ 创建 papers/ 目录（放入本地论文 PDF）                  │            │
│  └──────────────────────────────────────────────────────┘            │
│                              ↓                                       │
│  Step 1: 文献综述                                     ⏱ 5-15 min    │
│  ┌──────────────────────────────────────────────────────┐            │
│  │ claude                                                │            │
│  │ > /research-lit "你的研究方向"                         │            │
│  │                                                       │            │
│  │ 或者只搜 arXiv：                                      │            │
│  │ > /arxiv "关键词"                                     │            │
│  │                                                       │            │
│  │ 输出：文献综述表格 + 研究图景分析                      │            │
│  └──────────────────────────────────────────────────────┘            │
│                              ↓                                       │
│  Step 2: 创意发现                                     ⏱ 30-120 min  │
│  ┌──────────────────────────────────────────────────────┐            │
│  │ > /idea-discovery "你的研究方向"                       │            │
│  │                                                       │            │
│  │ 内部流程：                                            │            │
│  │   /research-lit → /idea-creator → /novelty-check      │            │
│  │   → /research-review                                  │            │
│  │                                                       │            │
│  │ 输出：IDEA_REPORT.md（排名创意报告）                   │            │
│  └──────────────────────────────────────────────────────┘            │
│                              ↓                                       │
│  Step 3: 代码实现                                     ⏱ 数天       │
│  ┌──────────────────────────────────────────────────────┐            │
│  │ 在 Cursor 中正常写代码                                │            │
│  │ 运行实验、收集结果                                    │            │
│  │ 写 NARRATIVE_REPORT.md（研究叙事）                    │            │
│  └──────────────────────────────────────────────────────┘            │
│                              ↓                                       │
│  Step 4: 自动审稿循环                                 ⏱ 2-8 h      │
│  ┌──────────────────────────────────────────────────────┐            │
│  │ claude                                                │            │
│  │ > /auto-review-loop "你的论文主题"                     │            │
│  │                                                       │            │
│  │ 内部流程（最多 4 轮）：                               │            │
│  │   GPT-5.4 审稿 → Claude 修改 → 再审 → 再改           │            │
│  │                                                       │            │
│  │ 输出：AUTO_REVIEW.md + 改进后的研究内容               │            │
│  │                                                       │            │
│  │ 💤 这一步可以去睡觉                                   │            │
│  └──────────────────────────────────────────────────────┘            │
│                              ↓                                       │
│  Step 5: 论文写作                                     ⏱ 1-3 h      │
│  ┌──────────────────────────────────────────────────────┐            │
│  │ > /paper-writing "NARRATIVE_REPORT.md"                │            │
│  │                                                       │            │
│  │ 内部流程：                                            │            │
│  │   /paper-plan → /paper-figure → /paper-write          │            │
│  │   → /paper-compile → /auto-paper-improvement-loop     │            │
│  │                                                       │            │
│  │ 输出：paper/main.pdf（完整论文）                      │            │
│  │                                                       │            │
│  │ 💤 这一步也可以去睡觉                                 │            │
│  └──────────────────────────────────────────────────────┘            │
│                              ↓                                       │
│  Step 6: 人工审核和修改                               ⏱ 你决定     │
│  ┌──────────────────────────────────────────────────────┐            │
│  │ 1. 阅读 paper/main.pdf                               │            │
│  │ 2. 检查数据和结论的准确性                             │            │
│  │ 3. 验证引用的论文是否真实存在                         │            │
│  │ 4. 根据目标期刊调整格式                               │            │
│  │ 5. 请导师和合作者审阅                                 │            │
│  │ 6. 投稿！ 🎉                                         │            │
│  └──────────────────────────────────────────────────────┘            │
│                                                                      │
│  一键全流程（替代 Step 1-5）：                                       │
│  > /research-pipeline "你的研究方向"                                 │
│  └── 自动执行 Step 1→2→3→4，你只需要做 Step 6                       │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 11.2 每一步的详细命令和参数

#### 文献综述命令选项

```powershell
# 最基本用法
claude
> /research-lit "你的研究方向"

# 只搜网络（跳过本地和 Zotero）
> /research-lit "方向" — sources: web

# 搜索并下载 arXiv PDF
> /research-lit "方向" — arxiv download: true

# 指定本地论文目录
> /research-lit "方向" — paper library: D:\my_papers\

# 只搜 arXiv
> /arxiv "关键词"
> /arxiv "关键词" — max: 20               # 最多 20 结果
> /arxiv "2301.07041" — download           # 下载特定论文
> /arxiv "关键词" — download: all          # 下载所有结果
```

#### 创意发现命令选项

```powershell
# 自动模式（每个阶段自动继续，适合睡觉时跑）
> /idea-discovery "研究方向"

# 手动模式（每个阶段等你确认）
> /idea-discovery "研究方向" — AUTO_PROCEED: false

# 下载文献 PDF
> /idea-discovery "研究方向" — arxiv download: true

# 调整 pilot 实验预算
> /idea-discovery "研究方向" — pilot budget: 4h per idea, 20h total
```

#### 审稿循环命令选项

```powershell
# 基本用法
> /auto-review-loop "论文主题/摘要"

# 如果之前中断了（自动恢复）
> /auto-review-loop "同样的主题"
# Claude 会检测 REVIEW_STATE.json 并从断点继续
```

#### 论文写作命令选项

```powershell
# 从研究叙事开始
> /paper-writing "NARRATIVE_REPORT.md"

# 指定目标会议
> /paper-writing "NARRATIVE_REPORT.md" — venue: NeurIPS
> /paper-writing "NARRATIVE_REPORT.md" — venue: ICML
> /paper-writing "NARRATIVE_REPORT.md" — venue: ICLR

# 手动模式
> /paper-writing "NARRATIVE_REPORT.md" — wait for my approval at each step
```

#### 全流程命令

```powershell
# 自动全流程（推荐睡前启动）
> /research-pipeline "研究方向"

# 手动确认模式
> /research-pipeline "研究方向" — AUTO_PROCEED: false
```

### 11.3 运行前检查清单

```
在启动 ARIS 长时间任务前，检查以下事项：

☐ 终端窗口保持打开（不要关闭）
☐ 电脑不会自动休眠（电源设置 → 从不休眠）
☐ 网络代理保持连接（http://127.0.0.1:7897）
☐ 足够的磁盘空间（论文 PDF + LaTeX 编译临时文件）
☐ 项目目录中有 CLAUDE.md（可选但推荐）
☐ 如果需要 Codex MCP：确认 codex --version 正常
☐ 如果需要编译 LaTeX：确认 pdflatex --version 正常
```

### 11.4 常用组合技

```
组合 1: 快速文献调研
  /arxiv "关键词" → /research-lit "方向" → 手动阅读

组合 2: 过夜创意发现
  /idea-discovery "方向"   → 睡觉 → 早上看 IDEA_REPORT.md

组合 3: 过夜审稿改稿
  /auto-review-loop "主题" → 睡觉 → 早上看 AUTO_REVIEW.md

组合 4: 周末全自动
  /research-pipeline "方向" → 周五晚上启动 → 周一看结果

组合 5: 论文冲刺
  手写 NARRATIVE_REPORT.md → /paper-writing "NARRATIVE_REPORT.md"
  → 1-3 小时后得到 paper/main.pdf
```

---

## 十二、本次演示技术参数汇总

| 参数 | 值 |
|------|-----|
| 演示日期 | 2026-03-15 |
| 运行环境 | Cursor IDE, Windows 10 (build 26200) |
| 执行模型 | Claude (claude-4.6-opus) |
| 审稿模型 | GPT-5.4 xhigh (via Codex MCP) |
| Codex CLI | v0.114.0 |
| Claude Code | v2.1.76 |
| 网络代理 | http://127.0.0.1:7897 |
| 项目目录 | E:\Git-hub_project\Auto-claude-code-research-in-sleep |
| arXiv 搜索结果 | 9 篇论文（3 组关键词 × 3 篇/组，去重后 9 篇） |
| WebSearch 结果 | 4 个重要平台/论文（TwinCell, VCWorld, GENEVA, npj综述） |
| GPT-5.4 审稿评分 | 3/10 (Not Ready) |
| GPT-5.4 识别的弱点 | 4 个致命 + 4 个重大 = 8 个 |
| 演示的 Skill | /research-review, /arxiv, /research-lit, /novelty-check |
| 总耗时 | 约 25 分钟 |

---

## 十三、`/arxiv` PDF 下载演示

### 13.1 执行命令

```powershell
python arxiv_search_demo.py "Hodgkin-Huxley parameter estimation single cell" --max 3 --download-all --dir papers
```

### 13.2 结果

成功搜索并下载了 3 篇论文的 PDF：

| # | arXiv ID | 标题 | 大小 |
|---|----------|------|------|
| 1 | 1106.4317 | Self-organizing state-space model for HH parameter estimation | 8,479 KB |
| 2 | 1811.00173 | Structure-preserving integrators for HH systems | 1,205 KB |
| 3 | 2601.14579 | Lie Group Basis of Neuronal Membrane Architecture | 488 KB |

**PDF 文件保存在** `papers/` 目录，搜索结果保存在 `papers/search_results.json`。

### 13.3 这在真实的 `/arxiv` Skill 中

```
在 Claude Code CLI 中：
> /arxiv "Hodgkin-Huxley parameter estimation" — download: all

效果完全相同——Claude 会调用 arXiv API 搜索并下载 PDF。
```

---

## 十四、`/novelty-check` Skill 演示：研究创意新颖性验证

### 14.1 被验证的创意

```
创意名称: Perturbation-Native Virtual Cell Twin (PNVCT)

核心思路: 
  直接在剂量-时间分辨的单细胞扰动数据集上训练虚拟细胞数字孪生体，
  以毒性终点作为学习目标，而不是先从静态基因表达推断生物物理参数
  再仿真。

声称的差异化:
  1. 直接在扰动数据上训练（不是 静态→仿真）
  2. 毒性终点是损失函数（不是参数准确性）
  3. 使用基础模型嵌入作为细胞状态表示
  4. 训练数据有剂量-时间分辨率
```

### 14.2 GPT-5.4 的新颖性判定

**判定结果: PARTIALLY NOVEL（部分新颖）**

GPT-5.4 找到了 **8 个高度相关的已有工作**，并逐一分析了差异：

| # | 已有工作 | 年份 | 与我们的差异 |
|---|---------|------|------------|
| 1 | **chemCPA / CPA** (NeurIPS 2022, Mol Syst Biol 2023) | 2022-23 | CPA 已经做了"直接在扰动数据上训练"和"剂量-时间感知"——我们的差异化点 1 和 4 不新颖 |
| 2 | **GEARS** (Nature Biotech 2023) | 2023 | 已经报告了"以细胞适应性为目标训练"——削弱了我们的差异化点 2 |
| 3 | **biolord** (Nature Biotech 2024) | 2024 | 反事实单细胞建模，包含药物特征和剂量属性 |
| 4 | **PerturbNet** (EMBO 2025) | 2025 | 模块化扰动表示 + 剂量和细胞类型协变量 |
| 5 | **State** (Arc Institute, bioRxiv 2025) | 2025 | **最近的竞争者** — 明确的"虚拟细胞模型"框架，以扰动数据为原生训练信号 |
| 6 | **SIMCO** (PMC 2025) | 2025 | 单细胞级数字孪生 + 结果预测目标 |
| 7 | **scOTM** (Bioengineering 2025) | 2025 | 已经使用基础模型嵌入——差异化点 3 不新颖 |
| 8 | **Decoding Cellular Stress States** (bioRxiv 2025) | 2025 | 最接近的毒理学单细胞工作 |

### 14.3 各差异化点的新颖性判定

```
差异化点 1: 直接在扰动数据上训练     → ❌ 不新颖（CPA 2022 已做）
差异化点 2: 毒性终点作为损失函数     → ⚠️ 部分新颖（最强的剩余角度）
差异化点 3: 基础模型嵌入             → ❌ 不新颖（scOTM 已做）
差异化点 4: 剂量-时间分辨率          → ❌ 不新颖（CPA 已做）
```

### 14.4 GPT-5.4 建议的更安全的新颖性声称

> **"一个端到端的毒性监督虚拟细胞模型，使用剂量和时间分辨的单细胞扰动数据
> 作为原生训练信号，而不是主要优化转录组重构。"**

### 14.5 GPT-5.4 建议的进一步差异化方法

```
1. 让毒性监督真正成为主要目标
   → 预测不良结果（存活率、凋亡、坏死、应激状态转换）
   → 不是"转录组重构 + 辅助毒性头"

2. 显式建模连续的剂量-时间轨迹
   → 不只是离散的条件标签

3. 将潜在空间与不良结果通路（AOP）绑定
   → 可解释性

4. 展示分布外泛化
   → 未见过的化合物、剂量、时间点、细胞类型

5. 前瞻性验证
   → 在留出的毒理学面板上验证
   → 证明"毒性优先训练"优于"转录组优先"基线
```

### 14.6 竞争时间线

```
2019: scGen — 建立了直接扰动响应预测
2022-23: chemCPA/CPA — 扰动原生、剂量时间感知成为主流
2023-24: GEARS/biolord — 扩展到表型/反事实预测
2025 Jun-Aug: State/PerturbNet — 大规模扰动原生虚拟细胞
2025: SIMCO — 单细胞数字孪生 + 结果预测
2025: 单细胞毒理学论文开始直接映射应激/毒性状态

GPT-5.4 的推断：
"如果一个'State/SIMCO for toxicology'论文还没有在审稿中，
 它很可能很快就会出现。"
```

### 14.7 这在真实的 `/novelty-check` Skill 中

```
在 Claude Code CLI 中：

> /novelty-check "Perturbation-Native Virtual Cell Twin: directly train virtual cell 
  digital twins on dose-time-resolved single-cell perturbation datasets with toxicity 
  endpoints as the learning objective"

Claude 会：
  ① 多源文献搜索（arXiv + Scholar + Semantic Scholar）
  ② 调用 GPT-5.4 xhigh 交叉验证新颖性
  ③ 检查最近 3-6 个月的并发工作
  ④ 识别最相似的已有工作和差异化点
  ⑤ 给出判定：NOVEL / PARTIALLY NOVEL / NOT NOVEL
  ⑥ 更新 IDEA_REPORT.md
```
