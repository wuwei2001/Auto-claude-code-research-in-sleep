# ARIS 演示 — Claude Code CLI 版本（完整教程）

> **本文件夹包含在 Claude Code CLI 中一步一步使用 ARIS Skills 的完整教程。**
> 
> **这是 ARIS 的推荐使用方式** — Claude Code 原生支持 `/命令` 语法，功能最完整，
> 支持后台运行和断点续传，适合长时间自动化科研任务。

## 本文件夹包含

| 文件 | 说明 |
|------|------|
| `README.md` | 本文件 — 完整的 Claude Code 版本教程 |
| **环境与启动** | |
| `quick_start.ps1` | 快速启动脚本（自动检查环境 + 显示命令列表 + 启动 Claude Code） |
| `health_check.ps1` | 深度环境诊断（17 项检查 + 网络测试 + 生成诊断报告） |
| **过夜自动化脚本** | |
| `overnight_review.ps1` | 过夜审稿脚本（一键启动自动审稿循环） |
| `overnight_idea_discovery.ps1` | 过夜创意发现脚本（文献→创意→新颖性→审查） |
| `overnight_pipeline.ps1` | 过夜全流程脚本（idea→code→experiment→review） |
| **参考与模板** | |
| `run_all_demos.ps1` | 所有 Skill 演示命令列表（按难度分级） |
| `demo_results_reference.md` | 预期结果参考（与 Cursor 版本对照） |
| `CLAUDE.md.template` | 项目说明模板（含示例、技术栈、ARIS 偏好） |
| `NARRATIVE_REPORT.md.template` | 研究叙事模板（`/paper-writing` 的输入格式） |

## 快速使用

```powershell
# 方法 1: 深度环境诊断（推荐先运行）
.\health_check.ps1

# 方法 2: 用启动脚本（推荐新手）
.\quick_start.ps1

# 方法 3: 直接启动
claude
> /arxiv "drug toxicity prediction"

# 方法 4: 过夜创意发现
.\overnight_idea_discovery.ps1 "your research direction"

# 方法 5: 过夜审稿
.\overnight_review.ps1 "你的论文主题"

# 方法 6: 过夜全流程（idea→code→experiment→review）
.\overnight_pipeline.ps1 "your research direction" -Venue "NeurIPS"
```

---

## 目录

1. [前置条件](#一前置条件)
2. [第一步：首次体验](#二第一步首次体验5-分钟)
3. [第二步：文献综述](#三第二步文献综述10-15-分钟)
4. [第三步：单轮审稿](#四第三步单轮审稿5-10-分钟)
5. [第四步：创意发现](#五第四步创意发现30-120-分钟)
6. [第五步：自动审稿循环](#六第五步自动审稿循环2-8-小时过夜运行)
7. [第六步：论文写作](#七第六步论文写作1-3-小时)
8. [全流程一键命令](#八全流程一键命令)
9. [所有命令参考](#九所有命令参考)
10. [常用组合技](#十常用组合技)
11. [故障排除](#十一故障排除)
12. [与 Cursor 版本的对比](#十二与-cursor-版本的对比)

---

## 一、前置条件

### 1.1 环境检查

在开始之前，确认以下组件已安装（你的环境已全部就绪 ✅）：

```powershell
# 验证 Claude Code（必须）
claude --version
# 期望输出：2.1.76 (Claude Code) 或更高

# 验证 Codex CLI（审稿功能需要）
E:\software\codex --version
# 期望输出：v0.114.0 或更高

# 验证 LaTeX（论文编译需要）
pdflatex --version
# 期望输出：MiKTeX 25.12

# 验证 Python（arXiv 搜索等需要）
python --version
# 期望输出：Python 3.12.x
```

### 1.2 你的环境现状

| 组件 | 状态 | 路径 |
|------|------|------|
| Claude Code CLI | v2.1.76 ✅ | 全局安装 |
| Codex CLI | v0.114.0 ✅ | `E:\software\codex` |
| Codex 模型 | gpt-5.4 + xhigh ✅ | `C:\Users\17372\.codex\config.toml` |
| MCP 配置 | codex 已连接 ✅ | `C:\Users\17372\.claude\settings.json` |
| Auto-Allow | 全部权限 ✅ | 同上 |
| ARIS Skills | 77 个 ✅ | `C:\Users\17372\.claude\skills\` |
| LaTeX | MiKTeX 25.12 ✅ | Scoop 安装 |
| Python | 3.12 ✅ | — |
| 代理 | 127.0.0.1:7897 ✅ | — |

### 1.3 自动检查脚本

运行 `quick_start.ps1` 会自动检查所有组件：

```powershell
cd E:\Git-hub_project\Auto-claude-code-research-in-sleep\demos\claude-code-version
.\quick_start.ps1
```

---

## 二、第一步：首次体验（5 分钟）

### 2.1 启动 Claude Code

```powershell
# 打开 PowerShell 或 Windows Terminal
# 进入 ARIS 项目目录（重要！Claude Code 在哪个目录启动就在哪工作）
cd E:\Git-hub_project\Auto-claude-code-research-in-sleep

# 启动 Claude Code
claude
```

你会看到类似这样的界面：

```
╭──────────────────────────────────────────╮
│ ✻ Welcome to Claude Code!               │
│                                          │
│   /help for available commands           │
│                                          │
│ cwd: E:\Git-hub_project\Auto-...        │
╰──────────────────────────────────────────╯

> █                    ← 在这里输入命令
```

### 2.2 运行最简单的命令

在 `>` 提示符后输入：

```
> /arxiv "drug toxicity neural network"
```

**Claude 会自动执行：**
1. 读取 `~/.claude/skills/arxiv/SKILL.md`
2. 解析你的查询
3. 调用 arXiv API 搜索论文
4. 展示结构化结果表格

**预期输出：**

```
| # | arXiv ID   | Title                                    | Authors        | Date       |
|---|------------|------------------------------------------|----------------|------------|
| 1 | 2403.18997 | Quantum to Classical Neural Network...   | Smaldone et al | 2024-03-27 |
| 2 | 1902.04996 | Structured penalized regression for...   | Zhao, Zucknick | 2019-02-13 |
```

**如果你看到了表格** → 环境没问题！继续下一步。

**如果报错了** → 查看[故障排除](#十一故障排除)。

### 2.3 基本操作

| 操作 | 命令 |
|------|------|
| 退出 | `/quit` 或 `Ctrl+C` 两次 |
| 查看帮助 | `/help` |
| 清除上下文 | `/clear` |
| 查看可用 Skill | 输入 `/` 后按 Tab |

---

## 三、第二步：文献综述（10-15 分钟）

### 3.1 为什么先做文献综述

文献综述是所有后续步骤的基础：
- 创意发现需要知道"别人做了什么"
- 审稿时需要引用相关工作
- 写论文需要 Related Work 部分

### 3.2 运行文献综述

```
> /research-lit "virtual cell digital twin single cell omics drug toxicity"
```

**Claude 会自动执行 5 个步骤：**

```
Step 0c: 扫描本地论文库
┌──────────────────────────────────────────┐
│ 检查 papers/ 和 literature/ 目录        │
│ 如果有 PDF，读取前 3 页提取信息          │
│ → 建立"你已有的论文"列表                │
└──────────────────────────────────────────┘
                    ↓
Step 1: 外部搜索
┌──────────────────────────────────────────┐
│ arXiv API 搜索（结构化结果）             │
│ WebSearch 搜索（Google Scholar 等）      │
│ → 去重合并所有来源                       │
└──────────────────────────────────────────┘
                    ↓
Step 2: 分析每篇论文
┌──────────────────────────────────────────┐
│ 提取：问题、方法、结果、与我们的相关性   │
└──────────────────────────────────────────┘
                    ↓
Step 3: 综合分析
┌──────────────────────────────────────────┐
│ 按主题分组                               │
│ 找共识和分歧                             │
│ 识别研究空白                             │
└──────────────────────────────────────────┘
                    ↓
Step 4: 输出
┌──────────────────────────────────────────┐
│ 结构化文献表格                           │
│ 叙述性总结（3-5 段）                     │
│ 可选：保存到 LITERATURE_SUMMARY.md       │
└──────────────────────────────────────────┘
```

### 3.3 参数变体

```
# 只搜索网络（跳过本地 PDF）
> /research-lit "方向" — sources: web

# 搜索并下载 arXiv PDF
> /research-lit "方向" — arxiv download: true

# 指定本地论文目录
> /research-lit "方向" — paper library: D:\my_papers\

# 只搜索 arXiv（快速）
> /arxiv "关键词"
> /arxiv "关键词" — max: 20               # 最多 20 结果
> /arxiv "2301.07041" — download           # 下载特定论文
> /arxiv "关键词" — download: all          # 下载所有结果
```

---

## 四、第三步：单轮审稿（5-10 分钟）

### 4.1 什么是单轮审稿

`/research-review` 调用 GPT-5.4 xhigh 以顶会审稿人身份审查你的研究。
这是一次性审查（不是循环），适合快速获取反馈。

### 4.2 运行审稿

**方式 1：直接输入描述**
```
> /research-review "我们提出了 VirtualCellPlatform，一个多尺度虚拟细胞建模框架。核心思路是用机器学习把单细胞组学数据映射到生物物理参数，建立虚拟细胞数字孪生体。当前结果：合成数据 R²=0.47，真实数据 R²=0.36。"
```

**方式 2：审查文件**
```
> /research-review "PAPER_PLAN.md"
```

### 4.3 预期输出

GPT-5.4 xhigh 会返回：

```
Score: 3/10 (Not Ready)

Strengths:
1. [优势 1]
2. [优势 2]

Weaknesses (ranked by severity):
1. [FATAL] 核心映射不可识别...
   Minimum fix: [具体修复方案]
2. [FATAL] 评估不可信...
   Minimum fix: [具体修复方案]
3. [MAJOR] 论文范围过大...
   Minimum fix: [具体修复方案]

Verdict: Not ready for submission.

Minimum viable improvement plan:
1. [改进步骤 1]
2. [改进步骤 2]
```

### 4.4 真实案例

在 Cursor 版本的 `DEMO_REPORT.md` 中记录了一次完整的审稿过程：
- GPT-5.4 给出 3/10 评分
- 识别出 4 个致命问题 + 4 个重大问题
- 每个问题都给出了"通俗解释"和"最小修复方案"
- 最终建议："删掉 70-80% 的范围，证明一个窄论点"

---

## 五、第四步：创意发现（30-120 分钟）

### 5.1 什么是创意发现

`/idea-discovery` 是 **Workflow 1** 的入口——从一个模糊的研究方向，找到具体可行的研究创意。

### 5.2 启动创意发现

```
> /idea-discovery "virtual cell digital twin for multi-organ drug toxicity prediction"
```

### 5.3 执行过程（你会看到什么）

```
======================================
Phase 1: Literature Survey            ⏱ 5-15 min
======================================

Searching arXiv... found 15 papers
Searching Scholar... found 8 papers
Scanning local papers/... found 3 PDFs
Building landscape map...

📚 Literature survey complete. Here's what I found:
  - Key themes: virtual cell modeling, single-cell omics, drug screening
  - Open problems: no executable causal cell model, weak temporal inference
  - Gaps: no joint drug-cell model, missing uncertainty quantification

Does this match your understanding? Should I adjust the scope?
(AUTO_PROCEED=true, continuing with top direction...)

======================================
Phase 2: Idea Generation               ⏱ 10-30 min
======================================

Preparing context for GPT-5.4 xhigh...
[Codex MCP] Sending to GPT-5.4...
[Codex MCP] Response received.

Generated 10 ideas, filtering by feasibility...
  - Idea 1: Perturbation-native virtual cell twin (feasible, novel)
  - Idea 2: Hybrid mechanistic-neural twin (feasible, possibly done)
  - Idea 3: Spatial multicellular toxicity twin (high compute)
  - ...

Running pilot experiments for top 3 ideas...
  - Idea 1 pilot: training... R²=0.52 (+12% over baseline) ✅
  - Idea 2 pilot: training... R²=0.48 (+3% over baseline) ⚠️
  - Idea 3 pilot: skipped (requires GPU cluster)

💡 Generated 10 ideas, filtered to 5, piloted 3. Top results:
  1. [Idea 1] — Pilot: POSITIVE (+12%)
  2. [Idea 2] — Pilot: WEAK POSITIVE (+3%)
  3. [Idea 3] — Not piloted

======================================
Phase 3: Novelty Verification          ⏱ 5-15 min
======================================

Checking Idea 1 against literature...
  - arXiv: no exact match found ✅
  - Scholar: 2 somewhat similar papers, but different approach ✅
  - GPT-5.4 cross-check: NOVEL CONFIRMED ✅

Checking Idea 2 against literature...
  - arXiv: found very similar work (2025.12345) ❌
  - Verdict: NOT NOVEL → eliminated

======================================
Phase 4: Critical Review               ⏱ 5-10 min
======================================

Sending Idea 1 to GPT-5.4 xhigh for review...
[Codex MCP] Sending to GPT-5.4...
[Codex MCP] Response received.

  Score: 7/10
  Strengths: [...]
  Weaknesses: [...]
  Verdict: Worth pursuing

======================================
Phase 5: Final Report                  ⏱ 2-5 min
======================================

Writing IDEA_REPORT.md...

📋 Idea Discovery complete!
  🏆 Top idea: [Idea 1 title]
  Pilot: POSITIVE (+12%)
  Novelty: CONFIRMED
  Reviewer score: 7/10
  
  See IDEA_REPORT.md for full details.
```

### 5.4 参数选项

```
# 自动模式（默认，适合睡觉时跑）
> /idea-discovery "研究方向"

# 手动模式（每个阶段等你确认）
> /idea-discovery "研究方向" — AUTO_PROCEED: false

# 下载文献 PDF
> /idea-discovery "研究方向" — arxiv download: true

# 调整 pilot 实验预算
> /idea-discovery "研究方向" — pilot budget: 4h per idea, 20h total
```

---

## 六、第五步：自动审稿循环（2-8 小时，过夜运行）

### 6.1 这是 ARIS 的核心功能

`/auto-review-loop` 是 **Workflow 2** — 通过多轮 GPT 审稿 + Claude 修改，把研究改到能投稿的质量。

**这就是"睡觉时做科研"的关键部分。**

### 6.2 启动前检查

```
☐ 电脑不会自动休眠
   → 设置 → 系统 → 电源 → 屏幕/睡眠 → 从不
   
☐ 网络代理保持连接
   → 代理软件不要关闭

☐ 终端窗口不要关闭
   → 可以最小化，但不能关

☐ 项目目录有足够的内容让 Claude 修改
   → 代码、文档、实验结果等
```

### 6.3 启动审稿循环

**方法 1：手动启动**
```powershell
cd E:\Git-hub_project\Auto-claude-code-research-in-sleep
claude

> /auto-review-loop "VirtualCellPlatform: multi-scale virtual cell modeling and drug toxicity screening"
```

**方法 2：用脚本启动（更方便）**
```powershell
cd E:\Git-hub_project\Auto-claude-code-research-in-sleep\demos\claude-code-version

.\overnight_review.ps1 "VirtualCellPlatform: multi-scale virtual cell modeling"
```

### 6.4 执行过程（后台自动运行）

```
初始化
├── 检查 REVIEW_STATE.json（是否有上次未完成的进度）
├── 读取项目文档和实验结果
└── 创建 AUTO_REVIEW.md

Round 1                                 ⏱ 30-90 min
├── Phase A: 发送完整上下文给 GPT-5.4 xhigh
│   └── GPT-5.4 返回：3/10, NOT READY
│       ├── 4 个致命弱点
│       └── 4 个重大弱点
├── Phase B: 解析评审结果
│   └── 3/10 < 6/10 → 继续循环
├── Phase C: Claude 实施修改
│   ├── 缩窄论文范围（砍掉 4 种细胞类型）
│   ├── 添加测试集评估和基线对比
│   ├── 重写贡献部分
│   └── 补充统计检验
├── Phase D: 等待实验结果（如果有实验在跑）
└── Phase E: 记录到 AUTO_REVIEW.md + 保存 REVIEW_STATE.json

Round 2                                 ⏱ 30-90 min
├── Phase A: 发送修改后的内容给 GPT-5.4
│   └── GPT-5.4 返回：5/10, NOT READY
│       └── 剩余 3 个问题
├── Phase C: Claude 继续修改
│   ├── 改进评估方法
│   ├── 添加消融实验
│   └── 补充不确定性分析
└── Phase E: 更新记录

Round 3                                 ⏱ 30-60 min
├── Phase A: GPT-5.4 审稿
│   └── 返回：6.5/10, ALMOST READY ✅
├── Phase B: 6.5 ≥ 6 → 停止条件满足
└── 写入最终总结

终止
├── REVIEW_STATE.json → status: "completed"
├── AUTO_REVIEW.md → 完整 3 轮审稿记录
└── 项目文件已被修改和改进
```

### 6.5 第二天早上查看结果

```powershell
# 查看审稿记录
type AUTO_REVIEW.md

# 查看最终状态
type REVIEW_STATE.json
# 期望看到: { "round": 3, "score": 6.5, "status": "completed" }

# 查看被修改的文件
git diff
```

### 6.6 如果中断了怎么办

```powershell
# 情况 1: 上下文窗口满了（Claude 自动处理）
#   → REVIEW_STATE.json 已保存
#   → 重新运行会自动从断点恢复

claude
> /auto-review-loop "同样的主题"
# Claude 会说：Recovered from context compaction. Resuming at Round N.

# 情况 2: 电脑休眠/断网
#   → 重新启动代理和终端
#   → 重新运行（同上）

# 情况 3: 想手动停止
#   → 按 Ctrl+C
#   → REVIEW_STATE.json 可能不完整
#   → 手动设置 status: "completed" 或删除文件重新开始
```

---

## 七、第六步：论文写作（1-3 小时）

### 7.1 准备输入

论文写作需要一个 `NARRATIVE_REPORT.md`（研究叙事），包含：

```markdown
# 研究叙事

## 研究背景
[你的研究领域背景，1-2 段]

## 核心问题
[你要解决什么问题]

## 方法
[你的方法详细描述]

## 实验设置
[数据集、基线、评估指标]

## 结果
[主要实验结果，包含数值]

## 关键发现
[3-5 个主要结论]

## 局限性
[已知限制]
```

**提示：** 你可以用 `CLAUDE.md.template` 作为起点，复制到项目中改写。

### 7.2 启动论文写作

```
> /paper-writing "NARRATIVE_REPORT.md"
```

或指定目标会议：
```
> /paper-writing "NARRATIVE_REPORT.md" — venue: NeurIPS
```

### 7.3 执行过程

```
Step 1: /paper-plan → PAPER_PLAN.md          ⏱ 5-10 min
Step 2: /paper-figure → figures/             ⏱ 5-15 min
Step 3: /paper-write → paper/main.tex        ⏱ 15-30 min
Step 4: /paper-compile → paper/main.pdf      ⏱ 2-5 min
Step 5: /auto-paper-improvement-loop          ⏱ 15-30 min
        → paper/main_round0_original.pdf
        → paper/main_round1.pdf
        → paper/main_round2.pdf（最终版）
```

---

## 八、全流程一键命令

### 8.1 `/research-pipeline` — 终极命令

```
> /research-pipeline "你的研究方向"
```

这一个命令包含了 Step 2 到 Step 5 的所有内容：

```
Stage 1: /idea-discovery          ← Workflow 1 (30-60 min)
  └── /research-lit → /idea-creator → /novelty-check → /research-review

🚦 Gate 1: 展示创意排名
  └── AUTO_PROCEED=true → 自动选排名第一的
  └── AUTO_PROCEED=false → 等你确认

Stage 2: 代码实现                  ← 自动写实验代码 (15-60 min)

Stage 3: /run-experiment           ← 部署实验 (5 min + 实验时间)

Stage 4: /auto-review-loop         ← Workflow 2 (1-4 h)
  └── 4 轮 GPT审稿 + Claude修改

Stage 5: 最终报告
```

### 8.2 参数选项

```
# 自动全流程（推荐睡前启动）
> /research-pipeline "方向"

# 手动确认模式（每个关键节点暂停）
> /research-pipeline "方向" — AUTO_PROCEED: false

# 同时下载文献 PDF
> /research-pipeline "方向" — arxiv download: true
```

### 8.3 典型时间线

```
19:00 — 启动 /research-pipeline
19:30 — Stage 1 完成（IDEA_REPORT.md）
20:00 — Stage 2 完成（代码已写好）
20:05 — Stage 3 完成（实验已部署）
20:10 — Stage 4 开始（auto-review-loop）
  ...  — Round 1: 4/10
  ...  — Round 2: 5.5/10
  ...  — Round 3: 6.5/10（停止）
~23:00 — 完成

你在 19:05 就可以去睡觉了 💤
```

---

## 九、所有命令参考

### 9.1 绿色命令（不需要 Codex，立即可用）

```
/arxiv "关键词"                 搜索 arXiv 论文
/arxiv "ID" — download          下载特定论文 PDF
/arxiv "关键词" — max: 20       指定结果数量
/arxiv "关键词" — download: all 下载所有结果

/research-lit "主题"            多源文献综述
/research-lit "主题" — sources: web    只搜网络
/research-lit "主题" — arxiv download: true  下载 PDF

/paper-compile "paper/"         编译 LaTeX → PDF
/analyze-results data/          分析实验结果
/pixel-art "描述"               生成像素风 SVG
```

### 9.2 黄色命令（需要 Codex MCP）

```
/research-review "摘要"         单轮深度审稿
/idea-creator "方向"            生成研究创意
/novelty-check "创意描述"       新颖性验证

/idea-discovery "方向"          Workflow 1: 创意发现全流程
/auto-review-loop "主题"        Workflow 2: 自动审稿循环
/paper-writing "报告.md"        Workflow 3: 论文写作全流程
/research-pipeline "方向"       全流程一键（1+2+3）

/paper-plan "报告.md"           论文大纲
/paper-write "大纲.md"          逐节写 LaTeX
```

### 9.3 参数覆盖语法

所有命令都支持 `— 参数名: 值` 语法覆盖默认参数：

```
/idea-discovery "x" — AUTO_PROCEED: false          手动确认
/auto-review-loop "x" — MAX_ROUNDS: 6              增加轮数
/paper-writing "x" — venue: NeurIPS                 指定会议
/research-lit "x" — sources: web                    只搜网络
/arxiv "x" — max: 20                               更多结果
```

---

## 十、常用组合技

```
组合 1: 快速文献调研 (15 min)
  /arxiv "关键词" → /research-lit "方向" → 手动阅读

组合 2: 过夜创意发现 (1-2 h)
  /idea-discovery "方向" → 睡觉 → 早上看 IDEA_REPORT.md

组合 3: 过夜审稿改稿 (2-8 h)
  /auto-review-loop "主题" → 睡觉 → 早上看 AUTO_REVIEW.md

组合 4: 周末全自动 (4-12 h)
  /research-pipeline "方向" → 周五晚上启动 → 周一看结果

组合 5: 论文冲刺 (1-3 h)
  手写 NARRATIVE_REPORT.md → /paper-writing "NARRATIVE_REPORT.md"
  → 得到 paper/main.pdf

组合 6: 日常最佳实践
  白天：Cursor 写代码、看结果
  晚上：Claude Code 跑 ARIS 自动化任务
```

---

## 十一、故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| `claude` 命令不存在 | 未安装 Claude Code | `npm install -g @anthropic-ai/claude-code` |
| `/idea-discovery` 不识别 | 可能在 Cursor 中 | 改用 Claude Code CLI |
| Codex MCP 报错 | 网络/代理问题 | 检查代理 `http://127.0.0.1:7897` |
| Codex 超时 | 网络慢 | 重试，或检查 Codex CLI 版本 |
| LaTeX 编译失败 | 缺宏包 | `miktex packages install xxx` |
| 审稿循环中断 | 上下文窗口满 | 重新运行，自动从断点恢复 |
| GPT 评分一直很低 | 研究确实需要改进 | 认真看审稿意见，先手动改进 |
| arXiv 返回空 | 关键词问题 | 换英文关键词，等几分钟重试 |
| Claude Code 卡住 | 等待用户输入 | 检查是否到了检查点 |

---

## 十二、与 Cursor 版本的对比

| 功能 | Claude Code CLI | Cursor IDE |
|------|----------------|------------|
| `/命令` 语法 | ✅ 原生支持 | ❌ 需自然语言 |
| Codex MCP | ✅ 直接可用 | ✅ 需重启后可用 |
| 后台运行 | ✅ 终端后台 | ❌ 需 GUI 打开 |
| 断点续传 | ✅ REVIEW_STATE.json | ❌ |
| 代码编辑 | ⚠️ 命令行 | ✅ IDE 编辑器 |
| 代码补全 | ❌ | ✅ Tab 补全 |
| 多文件编辑 | ⚠️ 逐个 | ✅ 同时多个 |

**结论：**
- **写代码** → Cursor
- **跑 ARIS 自动化** → Claude Code CLI
- **两者可以同时用同一个项目目录**

---

## 附：Cursor 版本详细演示

完整的 Cursor 版本演示记录（包含 GPT-5.4 审稿的原始结果、arXiv 搜索的完整论文列表、文献综合分析等）请查看：

```
demos/cursor-version/README.md     (746 行完整记录)
demos/cursor-version/DEMO_REPORT.md (同内容备份)
```
