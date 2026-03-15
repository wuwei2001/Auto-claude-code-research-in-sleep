# ARIS 完整使用手册（中文版）

> Auto-Research-In-Sleep (ARIS) — 让 AI 在你睡觉时做科研
> 版本：2026-03-15 | 适用环境：Windows 10/11 + Claude Code CLI + Cursor

---

## 目录

1. [ARIS 是什么](#一aris-是什么)
2. [你的安装状态](#二你的安装状态)
3. [Claude Code CLI 使用方法](#三claude-code-cli-使用方法详解)
4. [Cursor 使用方法](#四cursor-使用方法详解)
5. [三大 Workflow 详解](#五三大-workflow-详解)
6. [所有 Skills 用法手册](#六所有-skills-用法手册)
7. [实战案例](#七实战案例)
8. [高级配置](#八高级配置)
9. [故障排除](#九故障排除)

---

## 一、ARIS 是什么

### 1.1 核心理念

ARIS 是一组 Skill 文件（Markdown 格式的指令），安装在 `~/.claude/skills/` 目录下。当 Claude Code 读到这些文件时，它会按照文件中的步骤自动执行科研任务。

**关键创新**：跨模型协作
```
你 → 给出研究方向 → Claude Code（执行者）→ 写代码、跑实验、改论文
                              ↕ Codex MCP
                    GPT-5.4 xhigh（审查者）→ 审稿、打分、找弱点
```

为什么需要两个模型？
- 单模型自我审查会陷入"局部最优"——自己审自己总是觉得不错
- GPT-5.4 的审查风格与 Claude 不同，能发现 Claude 的盲点
- 类似于博弈论中的"对抗博弈" vs "自我博弈"

### 1.2 三大 Workflow

| Workflow | 命令 | 做什么 | 耗时 |
|----------|------|--------|------|
| **1. 创意发现** | `/idea-discovery` | 文献→创意→验证→排名 | 30min-2h |
| **2. 自动审稿** | `/auto-review-loop` | 审稿→修改→再审→重复4轮 | 2-8h |
| **3. 论文写作** | `/paper-writing` | 大纲→图表→LaTeX→PDF | 1-3h |

全流程一键：`/research-pipeline` = Workflow 1 → 代码实现 → Workflow 2 → Workflow 3

---

## 二、你的安装状态

### 2.1 已安装组件检查清单

| 组件 | 路径/命令 | 状态 | 验证方法 |
|------|----------|------|---------|
| ARIS Skills (22个) | `C:\Users\17372\.claude\skills\` | 已安装 | `ls ~/.claude/skills/` |
| Codex CLI | `E:\software\codex` | v0.114.0 | `codex --version` |
| Codex 模型配置 | `C:\Users\17372\.codex\config.toml` | gpt-5.4 + xhigh | 查看文件 |
| Cursor MCP | `C:\Users\17372\.cursor\mcp.json` | codex 已配置 | 查看文件 |
| Claude Code MCP | `C:\Users\17372\.claude\settings.json` | codex 已配置 | 查看文件 |
| Auto-Allow | `C:\Users\17372\.claude\settings.local.json` | 已开启 | 查看文件 |
| LaTeX (pdflatex) | Scoop安装的MiKTeX | v25.12 | `pdflatex --version` |
| latexmk | MiKTeX自带 | v4.87 | `latexmk --version` |
| pdfinfo | Scoop安装的Poppler | v24.04.0 | `pdfinfo -v` |
| pdftotext | Scoop安装的Poppler | v24.04.0 | `pdftotext -v` |

### 2.2 22个 Skill 功能速查表

| # | Skill名 | 功能 | 需要Codex MCP? | 命令示例 |
|---|---------|------|---------------|---------|
| 1 | `arxiv` | 搜索/下载 arXiv 论文 | 否 | `/arxiv "TDCIPP neurotoxicity"` |
| 2 | `research-lit` | 多源文献综述 (Zotero+Obsidian+本地+Web) | 否 | `/research-lit "organophosphate flame retardants"` |
| 3 | `idea-creator` | 生成8-12个研究创意 + GPT审查 + pilot | 是 | `/idea-creator "virtual cell toxicology"` |
| 4 | `novelty-check` | 深度新颖性验证 | 是 | `/novelty-check "OmicsToHH framework"` |
| 5 | `research-review` | 单轮深度审稿 (GPT-5.4) | 是 | `/research-review "你的论文摘要"` |
| 6 | `idea-discovery` | Workflow 1 全流程 | 是 | `/idea-discovery "研究方向"` |
| 7 | `auto-review-loop` | Workflow 2 自动审稿循环 | 是 | `/auto-review-loop "论文主题"` |
| 8 | `paper-plan` | 论文大纲 + Claims-Evidence矩阵 | 是 | `/paper-plan "NARRATIVE_REPORT.md"` |
| 9 | `paper-figure` | 生成论文图表 (matplotlib/seaborn) | 可选 | `/paper-figure "data/*.json"` |
| 10 | `paper-write` | 逐节写 LaTeX | 是 | `/paper-write "PAPER_PLAN.md"` |
| 11 | `paper-compile` | 编译 LaTeX→PDF | 否 | `/paper-compile "paper/"` |
| 12 | `auto-paper-improvement-loop` | 2轮论文改进 | 是 | 自动调用 |
| 13 | `paper-writing` | Workflow 3 全流程 | 是 | `/paper-writing "NARRATIVE_REPORT.md"` |
| 14 | `research-pipeline` | 全流程一键 | 是 | `/research-pipeline "研究方向"` |
| 15 | `run-experiment` | 部署实验到GPU | 否 | `/run-experiment train.py --lr 1e-4` |
| 16 | `analyze-results` | 分析实验结果 | 否 | `/analyze-results figures/*.json` |
| 17 | `monitor-experiment` | 监控实验进度 | 否 | `/monitor-experiment server5` |
| 18 | `pixel-art` | 生成像素风SVG | 否 | `/pixel-art "两个科学家讨论"` |
| 19 | `feishu-notify` | 飞书/Lark 通知 | 否 | 自动调用 |
| 20 | `dse-loop` | 设计空间探索(EDA/架构) | 否 | `/dse-loop "parameter sweep"` |
| 21 | `idea-discovery-robot` | 机器人领域创意 | 是 | `/idea-discovery-robot "manipulation"` |
| 22 | `auto-review-loop-minimax` | MiniMax模型审稿 | 否(需MiniMax) | 替代方案 |

---

## 三、Claude Code CLI 使用方法详解

### 3.1 什么是 Claude Code CLI

Claude Code CLI 是 Anthropic 官方的命令行 AI 编程工具。它在终端中运行，能够：
- 读写文件
- 运行命令
- 调用 MCP 工具（如 Codex/GPT-5.4）
- 执行 Skills（`/命令` 语法）

### 3.2 安装确认

```powershell
# 检查是否已安装
claude --version

# 如果没有安装
npm install -g @anthropic-ai/claude-code
```

### 3.3 启动和使用

```powershell
# 第一步：进入你的项目目录
cd E:\Git-hub_project\VirtualNeuronTox

# 第二步：启动 Claude Code
claude

# 你会看到类似这样的界面：
# ╭──────────────────────────────────────────╮
# │ Claude Code                              │
# │                                          │
# │ Type a message to start...               │
# ╰──────────────────────────────────────────╯
```

### 3.4 基本交互

在 Claude Code 中，你可以像聊天一样输入：

```
> 帮我搜索 TDCIPP 相关的 arXiv 论文
```

或者使用 `/命令` 调用 Skill：

```
> /arxiv "TDCIPP neurotoxicity"
```

### 3.5 Claude Code vs Cursor 的区别

| 特性 | Claude Code CLI | Cursor |
|------|----------------|--------|
| 界面 | 终端文本 | IDE图形界面 |
| Skill 调用 | `/命令` 原生支持 | 需要自然语言描述 |
| Codex MCP | 直接可用 | 需重启后可用 |
| 文件编辑 | 命令行编辑 | IDE内置编辑器 |
| 夜间运行 | 终端后台运行 | 需要GUI打开 |
| 代码补全 | 无 | 有 (Tab补全) |
| 多文件编辑 | 逐个文件 | 可同时打开多个 |

**建议**：
- **写代码**用 Cursor（IDE 体验好）
- **跑 ARIS Workflow**用 Claude Code CLI（功能完整，可后台运行）
- 两者可以同时使用，操作同一个项目目录

### 3.6 实际操作示例

**示例1：搜索 arXiv 论文**
```
> /arxiv "TDCIPP neurodevelopmental toxicity"

# Claude 会运行 Python 脚本查询 arXiv API
# 输出类似：
# | # | arXiv ID   | Title                        | Date       |
# |---|------------|------------------------------|------------|
# | 1 | 2501.12345 | TDCIPP exposure and brain... | 2025-01-15 |
```

**示例2：文献综述**
```
> /research-lit "organophosphate flame retardant neurodevelopment"

# Claude 会依次检查：
# 1. 本地 papers/ 目录中的 PDF
# 2. arXiv API 搜索
# 3. WebSearch 搜索
# 4. 整理成文献综述报告
```

**示例3：创意生成（需要 Codex MCP）**
```
> /idea-creator "TDCIPP prenatal exposure mechanisms"

# Claude 会：
# 1. 搜索文献建立图景
# 2. 调用 Codex MCP 让 GPT-5.4 生成 8-12 个创意
# 3. 逐个评估可行性和新颖性
# 4. 输出 IDEA_REPORT.md
```

**示例4：夜间自动审稿**
```
> /auto-review-loop "VirtualNeuronTox: biophysical modeling for neurotoxicology"

# Claude 会：
# 轮次1: GPT-5.4 审稿 → 打分 5/10 → Claude 修改
# 轮次2: GPT-5.4 再审 → 打分 6/10 → Claude 再改
# 轮次3: GPT-5.4 再审 → 打分 6.5/10 → Claude 再改
# 轮次4: GPT-5.4 再审 → 打分 7.5/10 → 达到阈值，停止
# 
# 全程自动，不需要人工干预
# 状态保存在 REVIEW_STATE.json（断点续传）
```

---

## 四、Cursor 使用方法详解

### 4.1 在 Cursor 中使用 ARIS

虽然 ARIS 原生为 Claude Code CLI 设计，但在 Cursor 中也可以使用大部分功能：

**方法：用自然语言告诉 AI 你想做什么**

```
# 不要用 /命令 语法（Cursor 不支持）
# 而是这样说：

"请按照 ARIS 的 research-lit skill 帮我做关于 TDCIPP 的文献综述"

"读取 ~/.claude/skills/idea-creator/SKILL.md，然后按照里面的步骤帮我生成研究创意"

"帮我用 arxiv skill 搜索 discrete diffusion language models"
```

### 4.2 Cursor 中使用 Codex MCP

**第一步**：重启 Cursor（使新的 MCP 配置生效）

**第二步**：验证 Codex MCP 是否可用
- 在 Cursor 设置中查看 MCP Servers
- 应该能看到 "codex" 服务器
- 状态应该是 "Running" 或 "Connected"

**第三步**：AI 可以调用 Codex
```
# 在 Cursor 中告诉 AI：
"请用 Codex MCP 调用 GPT-5.4 来审查我的 PAPER_PLAN.md"
```

### 4.3 直接运行 VirtualNeuronTox

VirtualNeuronTox 的 Python 代码在 Cursor 中完全可用：

```
# 在 Cursor 终端中：
cd E:\Git-hub_project\VirtualNeuronTox

python run_demo.py                    # 完整 demo
python run_tdcipp_simulation.py       # TDCIPP 仿真
python train_real_data.py             # 真实数据训练
python generate_figures.py            # 生成图表
python src/data/download_allen_data.py  # 下载数据
```

---

## 五、三大 Workflow 详解

### 5.1 Workflow 1: 创意发现 (`/idea-discovery`)

```
输入: 研究方向（一句话）
输出: IDEA_REPORT.md（排名创意报告）

流程:
Phase 1: 文献综述 (/research-lit)
  → 搜索 arXiv + Scholar + 本地论文
  → 建立研究图景：方向、方法、空白
  → 🚦 检查点：向你展示图景，问是否需要调整

Phase 2: 创意生成 (/idea-creator)
  → GPT-5.4 生成 8-12 个创意
  → Claude 初步筛选（可行性、新颖性、影响力）
  → 🚦 检查点：展示筛选后的创意排名

Phase 3: 新颖性验证 (/novelty-check)
  → 对 top 3 创意做深度文献搜索
  → GPT-5.4 交叉验证
  → 淘汰已发表的创意

Phase 4: 批判性审查 (/research-review)
  → GPT-5.4 以高水平审稿人角色审查
  → 指出弱点、建议改进
  → 更新排名

Phase 5: 输出
  → IDEA_REPORT.md 包含：
    - 文献图景
    - 排名创意（含 pilot 实验结果，如有 GPU）
    - 淘汰创意及原因
    - 建议执行顺序
```

**AUTO_PROCEED 参数**：
- `true`（默认）：每个检查点自动继续
- `false`：每个检查点等你确认

```
# 自动模式
> /idea-discovery "TDCIPP neurotoxicology"

# 手动确认模式
> /idea-discovery "TDCIPP neurotoxicology" — AUTO_PROCEED: false
```

### 5.2 Workflow 2: 自动审稿循环 (`/auto-review-loop`)

```
输入: 论文主题/摘要/已有草稿
输出: 改进后的论文 + AUTO_REVIEW.md 审稿记录

流程:
Round 1:
  → GPT-5.4 xhigh 审稿（10 分制打分）
  → 列出 5-8 个弱点
  → Claude 逐一修改/补充
  → 如果需要实验验证 → /run-experiment
  → 重新提交

Round 2-4: 重复上述过程

停止条件:
  → Score ≥ 6/10 (POSITIVE_THRESHOLD)
  → 或达到 MAX_ROUNDS = 4

安全特性:
  → 不会隐藏弱点来骗高分
  → > 4 GPU-hour 的实验会被跳过
  → 优先"重新表述"而非"加实验"
  → 状态保存在 REVIEW_STATE.json（断电可恢复）
```

### 5.3 Workflow 3: 论文写作 (`/paper-writing`)

```
输入: NARRATIVE_REPORT.md 或 PAPER_PLAN.md
输出: paper/ 目录（LaTeX + PDF）

流程:
Step 1: /paper-plan
  → Claims-Evidence 矩阵
  → 分节计划（5-8节）
  → 引文框架

Step 2: /paper-figure
  → 从实验数据自动生成图表
  → matplotlib/seaborn 风格
  → LaTeX \includegraphics 代码片段

Step 3: /paper-write
  → 逐节生成 LaTeX
  → ICLR/NeurIPS/ICML 模板
  → 自动去 AI 写作风格（delve, pivotal...）

Step 4: /paper-compile
  → latexmk 编译
  → 自动修复编译错误
  → pdftotext 验证页数

Step 5: /auto-paper-improvement-loop
  → 2 轮 GPT-5.4 审稿 + 修改
  → 格式合规检查
  → 最终 PDF
```

---

## 六、所有 Skills 用法手册

### 6.1 `/arxiv` — arXiv 论文搜索

```
# 基本搜索
> /arxiv "attention mechanism"

# 下载特定论文
> /arxiv "2301.07041" — download

# 搜索并下载所有结果
> /arxiv "TDCIPP neurotoxicity" — download: all

# 指定结果数量
> /arxiv "organophosphate" — max: 20

# 保存到自定义目录
> /arxiv "query" — dir: literature/
```

### 6.2 `/research-lit` — 文献综述

```
# 默认：搜索所有来源
> /research-lit "TDCIPP prenatal exposure"

# 只搜索特定来源
> /research-lit "topic" — sources: web
> /research-lit "topic" — sources: zotero, local
> /research-lit "topic" — sources: obsidian, web

# 同时下载 arXiv PDF
> /research-lit "topic" — arxiv download: true

# 指定本地论文目录
> /research-lit "topic" — paper library: ~/my_papers/
```

### 6.3 `/research-review` — 深度审稿

```
# 审查一段描述
> /research-review "我们提出了 OmicsToHH 框架，将离子通道基因表达映射到 HH 参数..."

# 审查一个文件
> /research-review "PAPER_PLAN.md"

# GPT-5.4 会给出：
# - 总体评分（1-10）
# - 优势列表
# - 弱点列表（按严重程度排序）
# - 具体改进建议
# - 最小可行改进方案
```

---

## 七、实战案例

### 7.1 案例：TDCIPP 神经毒理学研究

**Day 1: 文献综述**
```powershell
cd K:\shi_hao_nan_shuoshi_ke_ti\Topic_Pregnancy_Exposure_Neurodevelopment
claude

> /research-lit "TDCIPP prenatal exposure neurodevelopmental toxicity mechanisms 2024 2025"
```

**Day 2: 创意发现**
```
> /idea-discovery "TDCIPP孕期暴露经甲状腺轴干扰和线粒体代谢重编程致胶质细胞Crosstalk中断的神经发育毒性机制"
```

**Day 3: 开始写代码（切换到 Cursor）**
```
在 Cursor 中打开 E:\Git-hub_project\VirtualNeuronTox
正常写 Python 代码
运行 python run_tdcipp_simulation.py
```

**Day 4: 夜间审稿（切换回 Claude Code）**
```powershell
cd E:\Git-hub_project\VirtualNeuronTox
claude

> /auto-review-loop "VirtualNeuronTox: a three-target biophysical simulation framework for TDCIPP neurotoxicology, integrating OmicsToHH translator, virtual neuron digital twins, and NeuroCellHet sex-differential susceptibility analysis"

# 然后去睡觉
```

**Day 5: 写论文**
```
> /paper-writing "PAPER_PLAN.md"

# 等待 1-3 小时
# 输出在 paper/ 目录
```

### 7.2 推荐的项目目录结构

```
你的研究项目/
├── CLAUDE.md           # 项目说明（Claude Code 会读这个文件了解项目）
├── NARRATIVE_REPORT.md # 研究叙事（/paper-writing 的输入）
├── PAPER_PLAN.md       # 论文大纲
├── IDEA_REPORT.md      # 创意报告（/idea-discovery 输出）
├── REVIEW_STATE.json   # 审稿状态（断点续传）
├── AUTO_REVIEW.md      # 审稿记录
├── papers/             # 本地论文库（/research-lit 会扫描）
├── src/                # 代码
├── data/               # 数据
├── experiments/        # 实验结果
├── figures/            # 图表
└── paper/              # 生成的 LaTeX（/paper-writing 输出）
    ├── main.tex
    ├── references.bib
    └── main.pdf
```

**CLAUDE.md 示例**（让 Claude Code 了解你的项目）：
```markdown
# VirtualNeuronTox

## 项目概述
- 研究方向：TDCIPP 孕期暴露致神经发育障碍的计算毒理学
- 三个核心创意：OmicsToHH, VirtualNeuronTox, NeuroCellHet

## 环境
- Python 3.12, PyTorch 2.x
- 数据：Allen Brain Atlas Patch-seq (2333 cells)

## 前期结果
- 合成数据训练 R²=0.47
- 真实数据训练 R²=0.36
- TDCIPP 仿真：DA 神经元 ♂ AP -19.7% vs ♀ -5.5%
```

---

## 八、高级配置

### 8.1 修改 Codex 模型

```powershell
# 编辑 Codex 配置
notepad C:\Users\17372\.codex\config.toml

# 可选模型：
# model = "gpt-5.4"         ← 最佳（推荐）
# model = "gpt-5.3-codex"   ← 次选
# model = "o3"              ← 推理型
```

### 8.2 修改 Skill 参数

所有 Skill 的参数都在对应的 `SKILL.md` 文件开头定义：

```powershell
# 编辑审稿循环参数
notepad C:\Users\17372\.claude\skills\auto-review-loop\SKILL.md

# 可修改的参数：
# MAX_ROUNDS = 4            ← 最多审稿轮数
# POSITIVE_THRESHOLD = 6/10 ← 达到此分数停止
# > 4 GPU-hour skip = 4h    ← 跳过超时实验
```

### 8.3 添加飞书通知（以后配置）

```powershell
# 创建飞书配置文件
# 编辑 C:\Users\17372\.claude\feishu.json

{
  "mode": "push",
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/你的WEBHOOK_ID"
}
```

配置后，审稿循环完成、实验结束、论文编译完成时，飞书会推送通知卡片。

### 8.4 配置 GPU 服务器（以后配置）

在项目的 `CLAUDE.md` 中添加：

```markdown
## Remote Server
- SSH: `ssh user@gpu-server` (key-based auth)
- GPU: 4x A100
- Conda env: `research`
- Code directory: `/home/user/experiments/`
- Use `screen` for background jobs
```

---

## 九、故障排除

### 9.1 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| `claude` 命令不存在 | 未安装 Claude Code CLI | `npm install -g @anthropic-ai/claude-code` |
| `/idea-discovery` 不识别 | 在 Cursor 中（不支持 `/`） | 改用 Claude Code CLI，或用自然语言 |
| Codex MCP 报错 | Cursor 未重启 | 重启 Cursor |
| Codex 超时 | 网络/代理问题 | 检查 `HTTP_PROXY=http://127.0.0.1:7897` |
| LaTeX 编译失败 | 缺少宏包 | MiKTeX 会自动下载，或手动 `miktex packages install xxx` |
| 审稿循环中断 | 上下文窗口满了 | 自动从 `REVIEW_STATE.json` 恢复 |
| GPT-5.4 评分太低 | 论文确实有问题 | 认真看审稿意见，先手动改进再重跑 |
| Allen 数据下载失败 | API 限流 | 等几分钟重试 |
| HH 仿真太慢 | 纯 Python 循环 | 减少 `duration` 或增大 `dt` |

### 9.2 重要文件位置

```
C:\Users\17372\.claude\skills\          # ARIS Skills
C:\Users\17372\.claude\settings.json    # Claude Code 全局配置
C:\Users\17372\.claude\settings.local.json  # Auto-Allow 配置
C:\Users\17372\.cursor\mcp.json         # Cursor MCP 配置
C:\Users\17372\.codex\config.toml       # Codex 模型配置
E:\Git-hub_project\Auto-claude-code-research-in-sleep\  # ARIS 源码
E:\Git-hub_project\VirtualNeuronTox\    # VirtualNeuronTox 项目
```

---

## 附录：你的环境信息

```
OS: Windows 10 (build 26200)
Python: 3.12
Node.js: (需要确认版本)
Proxy: http://127.0.0.1:7897
Codex: E:\software\codex (v0.114.0)
LaTeX: MiKTeX 25.12 (Portable, via Scoop)
Poppler: 24.04.0 (via Scoop)
Scoop: 已安装
```
