# ARIS 完整使用手册（中文版）

> Auto-Research-In-Sleep (ARIS) — 让 AI 在你睡觉时做科研
> 版本：2026-03-15 | 适用环境：Windows 10/11 + Claude Code CLI + Cursor

---

## 目录

1. [30 秒极速上手](#一30-秒极速上手)
2. [ARIS 到底是什么](#二aris-到底是什么)
3. [核心概念详解](#三核心概念详解)
4. [你的安装状态](#四你的安装状态)
5. [Claude Code CLI 使用方法](#五claude-code-cli-使用方法详解)
6. [Cursor 使用方法](#六cursor-使用方法详解)
7. [三大 Workflow 详解](#七三大-workflow-详解)
8. [所有 Skills 用法手册](#八所有-skills-用法手册)
9. [实战案例：手把手教程](#九实战案例手把手教程)
10. [高级配置](#十高级配置)
11. [故障排除](#十一故障排除)
12. [常见误解 FAQ](#十二常见误解-faq)

---

## 一、30 秒极速上手

**如果你只想快速试一下，照着做就行：**

```powershell
# 1. 打开终端，进入你的研究项目目录
cd E:\Git-hub_project\你的项目

# 2. 启动 Claude Code
claude

# 3. 在 Claude Code 中输入命令（选一个试）：
> /arxiv "你的研究关键词"                    # 搜 arXiv 论文
> /research-lit "你的研究方向"                # 做文献综述
> /idea-discovery "你的研究方向"              # 全自动找创意（需 Codex MCP）
> /auto-review-loop "你的论文主题"            # 全自动审稿修改（需 Codex MCP）
> /research-pipeline "你的研究方向"           # 从找idea到审稿完毕全流程
```

**就这么简单。** 输入命令后，Claude 会自动执行所有步骤，你可以去睡觉了。

---

## 二、ARIS 到底是什么

### 2.1 一句话解释

ARIS 是**一组 Markdown 格式的指令文件**（叫 Skill），告诉 Claude Code "按照这些步骤做科研"。

### 2.2 它不是什么

| 常见误解 | 实际情况 |
|---------|---------|
| ❌ 一个需要安装的软件 | ✅ 只是一些 .md 文件，放在 `~/.claude/skills/` 目录下 |
| ❌ 一个 Python 包 | ✅ 不需要 `pip install`，Claude Code 直接读取 Skill 文件 |
| ❌ 一个 GUI 工具 | ✅ 在终端里用，输入 `/命令` 就行 |
| ❌ 只能用 Claude | ✅ 核心创新是 Claude + GPT-5.4 双模型协作 |
| ❌ 会替代你写论文 | ✅ 帮你做重复性工作，你做创造性决策 |

### 2.3 工作原理（图解）

```
┌──────────────────────────────────────────────────────────────────────┐
│                    你的电脑上发生了什么                                │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  你 ──→ 输入 "/idea-discovery 某某方向"                              │
│           │                                                          │
│           ▼                                                          │
│  ┌─────────────────────────┐                                         │
│  │   Claude Code CLI       │  ← 在你的终端里运行                     │
│  │   (Anthropic Claude)    │                                         │
│  │                         │                                         │
│  │  1. 读取 SKILL.md 文件   │  ← ~/.claude/skills/idea-discovery/    │
│  │  2. 按步骤执行：          │                                        │
│  │     ├─ 搜索 arXiv        │  ← 调用 arXiv API                     │
│  │     ├─ 搜索 Google       │  ← 调用 WebSearch                     │
│  │     ├─ 读写文件           │  ← 在项目目录操作                     │
│  │     ├─ 运行 Python       │  ← 执行代码                           │
│  │     └─ 调用 GPT-5.4 ─────┼──→ Codex MCP ──→ OpenAI API          │
│  │         (审查/评分)       │                                        │
│  │                         │                                         │
│  │  3. 输出结果文件          │  ← IDEA_REPORT.md, AUTO_REVIEW.md 等  │
│  └─────────────────────────┘                                         │
│                                                                      │
│  输出文件就在你的项目目录里，打开看就行                                │
└──────────────────────────────────────────────────────────────────────┘
```

### 2.4 为什么要双模型？

这是 ARIS 的核心创新。想象一个场景：

```
传统方式（单模型自我审查）：
  Claude 写论文 → Claude 自己审 → "写得不错！" → 实际上有很多盲点

ARIS 方式（双模型对抗审查）：
  Claude 写论文 → GPT-5.4 审稿 → "你的方法在 X 上有缺陷" → Claude 改进
                → GPT-5.4 再审 → "好多了，但 Y 需要更多实验" → Claude 再改
                → GPT-5.4 终审 → "7/10，可以投稿了" → 结束
```

就像博士答辩找外审一样，自己导师觉得好不算，得外面的专家说好才行。

---

## 三、核心概念详解

### 3.1 什么是 Skill？

**Skill = 一个 Markdown 文件 + 固定的步骤指令**

```
~/.claude/skills/
├── arxiv/
│   └── SKILL.md          ← 告诉 Claude 怎么搜 arXiv
├── idea-discovery/
│   └── SKILL.md          ← 告诉 Claude 怎么发现研究创意
├── auto-review-loop/
│   └── SKILL.md          ← 告诉 Claude 怎么自动审稿
└── paper-writing/
    └── SKILL.md          ← 告诉 Claude 怎么写论文
```

当你输入 `/arxiv "attention mechanism"` 时，Claude Code 会：
1. 找到 `~/.claude/skills/arxiv/SKILL.md`
2. 读取里面的指令
3. 按照指令一步步执行（搜索、下载、总结...）

**你可以打开任何 SKILL.md 文件查看和修改它的行为。**

### 3.2 什么是 Codex MCP？

**MCP = Model Context Protocol**，是让 Claude Code 调用外部工具的标准协议。

**Codex MCP** 具体做的事情：
```
Claude Code ──(MCP协议)──→ Codex CLI ──(API)──→ OpenAI GPT-5.4
                                                     │
                                                     ↓
                                              审稿意见/评分
                                                     │
Claude Code ←─(MCP协议)──← Codex CLI ←─(API)──←─────┘
```

简单说：Codex MCP 是一个"翻译器"，让 Claude 能跟 GPT-5.4 对话。

**配置已完成：**
- Codex CLI 安装在 `E:\software\codex`
- 配置文件在 `C:\Users\17372\.codex\config.toml`（已设定 model = "gpt-5.4"）
- MCP 连接在 `C:\Users\17372\.claude\settings.json`（已配置）

### 3.3 什么是 Auto-Allow？

正常使用 Claude Code 时，每次它想执行命令（比如运行 Python、写文件），都会问你"允许吗？"。

**Auto-Allow 让它不用问，直接执行**——这样它才能在你睡觉时自动工作。

你的配置中已经开启了全部权限：
```json
"permissions": {
  "allow": ["Bash(*)", "Edit(*)", "Write(*)", "Read(*)", ...]
}
```

### 3.4 输入和输出

**ARIS 的输入输出都是文件：**

| 你给的输入 | ARIS 产出的输出 |
|-----------|---------------|
| 一句话描述研究方向 | `IDEA_REPORT.md` — 创意报告 |
| 论文主题/草稿 | `AUTO_REVIEW.md` — 审稿记录 |
| `NARRATIVE_REPORT.md` 研究叙事 | `paper/main.pdf` — 完整论文 |
| `PAPER_PLAN.md` 论文大纲 | `paper/` 目录（LaTeX + PDF） |

**所有输出文件都在你的项目目录里**，不是在某个隐藏的地方。

---

## 四、你的安装状态

### 4.1 已安装组件检查清单

| 组件 | 路径/命令 | 状态 | 验证方法 |
|------|----------|------|---------|
| Claude Code CLI | `claude` | v2.1.76 ✅ | `claude --version` |
| ARIS Skills (77个) | `C:\Users\17372\.claude\skills\` | 已安装 ✅ | `ls ~/.claude/skills/` |
| Codex CLI | `E:\software\codex` | v0.114.0 ✅ | `codex --version` |
| Codex 模型配置 | `C:\Users\17372\.codex\config.toml` | gpt-5.4 + xhigh ✅ | 查看文件 |
| Claude Code MCP | `C:\Users\17372\.claude\settings.json` | codex 已配置 ✅ | 查看文件 |
| Auto-Allow | `C:\Users\17372\.claude\settings.json` | 已开启 ✅ | 查看文件 |
| LaTeX (pdflatex) | Scoop安装的MiKTeX | v25.12 ✅ | `pdflatex --version` |
| latexmk | MiKTeX自带 | v4.87 ✅ | `latexmk --version` |
| pdfinfo | Scoop安装的Poppler | v24.04.0 ✅ | `pdfinfo -v` |
| pdftotext | Scoop安装的Poppler | v24.04.0 ✅ | `pdftotext -v` |

### 4.2 ARIS 核心 Skills 速查表（22个科研相关）

| # | Skill名 | 一句话说明 | 需要 Codex? | 命令 |
|---|---------|----------|------------|------|
| 1 | `arxiv` | 搜索/下载 arXiv 论文 | 否 | `/arxiv "关键词"` |
| 2 | `research-lit` | 多源文献综述 | 否 | `/research-lit "主题"` |
| 3 | `idea-creator` | 生成 8-12 个研究创意 | 是 | `/idea-creator "方向"` |
| 4 | `novelty-check` | 验证创意是否新颖 | 是 | `/novelty-check "创意描述"` |
| 5 | `research-review` | 单轮深度审稿 | 是 | `/research-review "摘要"` |
| 6 | `idea-discovery` | **Workflow 1** 全流程 | 是 | `/idea-discovery "方向"` |
| 7 | `auto-review-loop` | **Workflow 2** 自动审稿 | 是 | `/auto-review-loop "主题"` |
| 8 | `paper-plan` | 论文大纲 + 矩阵 | 是 | `/paper-plan "报告.md"` |
| 9 | `paper-figure` | 生成论文图表 | 可选 | `/paper-figure "data/"` |
| 10 | `paper-write` | 逐节写 LaTeX | 是 | `/paper-write "大纲.md"` |
| 11 | `paper-compile` | 编译 LaTeX→PDF | 否 | `/paper-compile "paper/"` |
| 12 | `auto-paper-improvement-loop` | 2轮论文改进 | 是 | 自动调用 |
| 13 | `paper-writing` | **Workflow 3** 全流程 | 是 | `/paper-writing "报告.md"` |
| 14 | `research-pipeline` | **一键全流程** | 是 | `/research-pipeline "方向"` |
| 15 | `run-experiment` | 部署实验到 GPU | 否 | `/run-experiment` |
| 16 | `analyze-results` | 分析实验结果 | 否 | `/analyze-results` |
| 17 | `monitor-experiment` | 监控实验进度 | 否 | `/monitor-experiment` |
| 18 | `pixel-art` | 生成像素风 SVG | 否 | `/pixel-art "描述"` |
| 19 | `feishu-notify` | 飞书通知（可选） | 否 | 自动调用 |
| 20 | `dse-loop` | 设计空间探索 | 否 | `/dse-loop` |
| 21 | `idea-discovery-robot` | 机器人领域创意 | 是 | 替代版 |
| 22 | `auto-review-loop-minimax` | MiniMax 模型审稿 | 否(需MiniMax) | 替代版 |

### 4.3 Skill 分级（按难度/依赖排序）

```
🟢 零门槛（不需要 Codex MCP，不需要 GPU，立即可用）：
   /arxiv, /research-lit, /paper-compile, /analyze-results, /pixel-art

🟡 需要 Codex MCP（需要 OpenAI API 能通）：
   /idea-creator, /novelty-check, /research-review,
   /idea-discovery, /auto-review-loop, /paper-writing, /research-pipeline

🔴 需要 GPU 服务器（需要 SSH 到远程 GPU 机器）：
   /run-experiment, /monitor-experiment, /dse-loop
```

**建议先试 🟢 级别的命令，确认环境没问题，再试 🟡 级别的。**

---

## 五、Claude Code CLI 使用方法详解

### 5.1 Claude Code 是什么

Claude Code CLI 是 Anthropic 官方的命令行 AI 编程工具。把它想象成一个"住在终端里的 AI 研究助理"：
- 能读写你电脑上的文件
- 能运行命令（Python、git、LaTeX...）
- 能上网搜索
- 能调用 MCP 工具（Codex/GPT-5.4）
- 能读取 Skill 文件并按步骤执行

### 5.2 启动 Claude Code（详细步骤）

```powershell
# 第一步：打开 PowerShell 或 Windows Terminal

# 第二步：进入你的项目目录（很重要！Claude Code 在哪个目录启动，就在哪个目录工作）
cd E:\Git-hub_project\Auto-claude-code-research-in-sleep

# 第三步：启动 Claude Code
claude

# 你会看到类似这样的界面：
# ╭──────────────────────────────────────────╮
# │ ✻ Welcome to Claude Code!               │
# │                                          │
# │   /help for available commands           │
# │                                          │
# │ cwd: E:\Git-hub_project\Auto-...        │
# ╰──────────────────────────────────────────╯
#
# > █                    ← 这里输入你的命令
```

### 5.3 在 Claude Code 中输入命令

**两种方式：**

**方式 1：自然语言（像聊天一样）**
```
> 帮我搜索 TDCIPP 相关的 arXiv 论文
> 做一个关于有机磷阻燃剂的文献综述
> 审查一下我的论文，看看有什么问题
```

**方式 2：/命令（调用 Skill，推荐）**
```
> /arxiv "TDCIPP neurotoxicity"
> /research-lit "organophosphate flame retardant neurodevelopment"
> /idea-discovery "TDCIPP 孕期暴露致神经发育毒性"
```

**`/命令` 方式更好**，因为它会严格按照 SKILL.md 里的步骤执行，不会遗漏。

### 5.4 Claude Code 的基本操作

| 操作 | 怎么做 |
|------|--------|
| 启动 | `claude` |
| 退出 | 输入 `/quit` 或按 `Ctrl+C` 两次 |
| 查看帮助 | `/help` |
| 查看可用 Skill | `/skills` 或 `ls ~/.claude/skills/` |
| 清除上下文 | `/clear` |
| 切换模型 | `/model` |
| 查看历史 | `/history` |

### 5.5 Claude Code vs Cursor 的区别

| 特性 | Claude Code CLI | Cursor |
|------|----------------|--------|
| 界面 | 终端文本 | IDE 图形界面 |
| Skill `/命令` | 原生支持 ✅ | 不支持（用自然语言代替） |
| Codex MCP | 直接可用 ✅ | 需重启后可用 |
| 夜间自动运行 | 终端后台运行 ✅ | 需要 GUI 打开 |
| 代码编辑 | 命令行编辑 | IDE 编辑器（更好） |
| 代码补全 | 无 | Tab 补全 ✅ |

**推荐用法：**
- **写代码、看代码** → 用 Cursor
- **跑 ARIS 自动流程** → 用 Claude Code CLI
- 两者可以**同时使用**同一个项目目录，不冲突

### 5.6 让 Claude Code 后台运行（睡觉模式）

```powershell
# 方法 1：直接在终端启动，不关终端
claude
> /auto-review-loop "你的论文主题"
# 然后锁屏去睡觉（不要关终端！）

# 方法 2：用 Windows Terminal 的多标签页
# 打开一个新标签页 → 启动 claude → 输入命令 → 切到别的标签页
# Claude 在后台继续工作

# 方法 3：用 tmux/screen（如果安装了的话）
# tmux new -s aris
# claude
# > /research-pipeline "研究方向"
# Ctrl+B, D  (detach)
# 第二天回来：tmux attach -t aris
```

**注意事项：**
- 电脑不能休眠/睡眠（在电源设置中关闭自动睡眠）
- 网络不能断（代理要保持连接）
- 终端窗口不能关闭

---

## 六、Cursor 使用方法详解

### 6.1 在 Cursor 中使用 ARIS

Cursor 不支持 `/命令` 语法，但你可以用自然语言告诉 AI 去调用 Skill：

```
# ❌ 不要这样（Cursor 不认）：
/arxiv "TDCIPP"

# ✅ 要这样说：
"请按照 ARIS 的 arxiv skill 帮我搜索 TDCIPP 相关论文"

"读取 ~/.claude/skills/research-lit/SKILL.md，按照里面的步骤帮我做文献综述"

"帮我用 research-review skill 审查我的 PAPER_PLAN.md"
```

### 6.2 在 Cursor 中使用 Codex MCP

1. **确认 MCP 已配置**：查看 Cursor 设置 → MCP Servers → 应该看到 "codex"
2. **如果看不到**：重启 Cursor
3. **使用方法**：直接告诉 AI "用 Codex MCP 调用 GPT-5.4 来审查..."

### 6.3 何时用 Cursor，何时用 Claude Code

```
┌─────────────────────────────────┐
│         你的日常工作流            │
├─────────────────────────────────┤
│                                 │
│  白天：Cursor                    │
│  ├─ 写代码                      │
│  ├─ 调试                        │
│  ├─ 看文件                      │
│  └─ 简单的文献搜索               │
│                                 │
│  晚上/长时间任务：Claude Code CLI │
│  ├─ /idea-discovery（30min-2h） │
│  ├─ /auto-review-loop（2-8h）   │
│  ├─ /paper-writing（1-3h）      │
│  └─ /research-pipeline（一整晚）│
│                                 │
└─────────────────────────────────┘
```

---

## 七、三大 Workflow 详解

### 7.1 Workflow 1: 创意发现 (`/idea-discovery`)

**目的：从一个模糊的研究方向，找到具体可行的研究创意**

**你需要提供：** 一句话描述你的研究方向

**AI 最终产出：** `IDEA_REPORT.md`（排名创意报告）

**完整流程：**

```
Phase 1: 文献综述 (/research-lit)                    ⏱ 5-15 min
┌──────────────────────────────────────────────────────────┐
│ ① 搜索 arXiv API 获取相关论文（标题、摘要、作者）         │
│ ② 搜索 Google Scholar / Semantic Scholar                 │
│ ③ 扫描本地 papers/ 目录中的 PDF                          │
│ ④ 整理成研究图景：已有方法、开放问题、研究空白             │
│                                                          │
│ 🚦 检查点：展示图景，问你是否需要调整方向                  │
│    → AUTO_PROCEED=true 时自动继续                        │
│    → AUTO_PROCEED=false 时等你确认                       │
└──────────────────────────────────────────────────────────┘
                              ↓
Phase 2: 创意生成 (/idea-creator)                    ⏱ 10-30 min
┌──────────────────────────────────────────────────────────┐
│ ① Claude 根据文献图景，准备创意生成的上下文               │
│ ② 调用 Codex MCP → GPT-5.4 xhigh 生成 8-12 个创意       │
│ ③ Claude 初步筛选：可行性、新颖性、影响力                 │
│ ④ 对 top 2-3 个创意运行 pilot 实验（如有 GPU）           │
│                                                          │
│ 🚦 检查点：展示筛选后的创意排名                           │
└──────────────────────────────────────────────────────────┘
                              ↓
Phase 3: 新颖性验证 (/novelty-check)                 ⏱ 5-15 min
┌──────────────────────────────────────────────────────────┐
│ ① 对 top 3 创意做深度文献搜索                            │
│ ② 检查最近 3-6 个月是否有相同/相似的工作发表              │
│ ③ 调用 GPT-5.4 交叉验证新颖性                           │
│ ④ 淘汰已被发表的创意，记录原因                           │
└──────────────────────────────────────────────────────────┘
                              ↓
Phase 4: 专家审查 (/research-review)                 ⏱ 5-10 min
┌──────────────────────────────────────────────────────────┐
│ ① GPT-5.4 xhigh 以 NeurIPS/ICML 审稿人角色审查          │
│ ② 打分（1-10）、列出弱点、建议最小改进方案               │
│ ③ 更新创意排名                                          │
└──────────────────────────────────────────────────────────┘
                              ↓
Phase 5: 输出报告                                    ⏱ 2-5 min
┌──────────────────────────────────────────────────────────┐
│ 生成 IDEA_REPORT.md：                                    │
│  ├─ 文献图景总结                                         │
│  ├─ 🏆 排名创意（含 pilot 结果）                         │
│  ├─ 被淘汰的创意及原因                                   │
│  └─ 建议执行顺序和下一步行动                              │
└──────────────────────────────────────────────────────────┘
```

**使用示例：**
```
# 自动模式（默认，适合睡觉时运行）
> /idea-discovery "TDCIPP 孕期暴露致神经发育毒性的计算建模"

# 手动模式（每个阶段等你确认）
> /idea-discovery "TDCIPP neurotoxicology" — AUTO_PROCEED: false
```

### 7.2 Workflow 2: 自动审稿循环 (`/auto-review-loop`)

**目的：通过多轮 GPT 审稿 + Claude 修改，把论文改到能投稿的质量**

**你需要提供：** 论文主题/摘要/已有草稿

**AI 最终产出：** `AUTO_REVIEW.md`（完整审稿记录） + 改进后的论文文件

**完整流程：**

```
初始化
┌──────────────────────────────────────────────────────────┐
│ ① 检查 REVIEW_STATE.json（是否有之前中断的进度）         │
│ ② 读取项目文档、实验结果、已知问题                        │
│ ③ 创建 AUTO_REVIEW.md                                   │
└──────────────────────────────────────────────────────────┘
                              ↓
          ┌──────── 循环（最多 4 轮）────────┐
          │                                   │
          ▼                                   │
Round N: Phase A — GPT-5.4 审稿               │
┌──────────────────────────────────────────┐  │
│ 发送完整上下文给 GPT-5.4 xhigh：         │  │
│ ├─ 当前论文/研究内容                     │  │
│ ├─ 上一轮的修改（如果有）                │  │
│ └─ 已知弱点                              │  │
│                                          │  │
│ GPT-5.4 返回：                           │  │
│ ├─ 评分（1-10 分）                       │  │
│ ├─ 判定（ready/almost/not ready）        │  │
│ ├─ 弱点列表（按严重程度排序）            │  │
│ └─ 每个弱点的最小修复方案                │  │
└──────────────────────────────────────────┘  │
          │                                   │
          ▼                                   │
Phase B — 解析评审结果                         │
┌──────────────────────────────────────────┐  │
│ 提取：分数、判定、待办事项                │  │
│                                          │  │
│ 如果 分数 ≥ 6 且 判定 = ready/almost：   │  │
│   → 停止循环 ✅                          │  │
│ 否则：                                   │  │
│   → 继续修改                             │  │
└──────────────────────────────────────────┘  │
          │                                   │
          ▼                                   │
Phase C — Claude 修改                          │
┌──────────────────────────────────────────┐  │
│ 按优先级逐个修复审稿意见：               │  │
│ ├─ 修改代码                              │  │
│ ├─ 补充实验                              │  │
│ ├─ 更新分析和图表                        │  │
│ └─ 更新文档                              │  │
│                                          │  │
│ 优先策略：                               │  │
│ ├─ 跳过需要大量算力的实验                │  │
│ ├─ 优先"重新表述"而非"加实验"           │  │
│ └─ 指标类修改优先（成本低、效果好）      │  │
└──────────────────────────────────────────┘  │
          │                                   │
          ▼                                   │
Phase D — 等待实验结果（如果有实验在跑）       │
          │                                   │
          ▼                                   │
Phase E — 记录本轮结果                         │
┌──────────────────────────────────────────┐  │
│ 写入 AUTO_REVIEW.md：                    │  │
│ ├─ 本轮评分和判定                        │  │
│ ├─ GPT 原始审稿意见（完整保留）          │  │
│ ├─ 采取的修改措施                        │  │
│ └─ 实验结果                              │  │
│                                          │  │
│ 保存 REVIEW_STATE.json（断点续传）       │  │
└──────────────────────────────────────────┘  │
          │                                   │
          └──────── 回到 Phase A ─────────────┘

终止条件：
  ✅ 分数 ≥ 6/10 且判定为 ready/almost
  ⛔ 达到 MAX_ROUNDS = 4 轮
```

**断点续传功能：** 如果 Claude Code 的上下文窗口满了（长时间运行会发生），它会把当前状态保存到 `REVIEW_STATE.json`。下次重新运行 `/auto-review-loop` 时，会自动从断点恢复。

**典型结果示例：**
```
Round 1: 4/10 — "实验设计有重大缺陷，缺少基线对比"
Round 2: 5.5/10 — "基线已加，但统计分析不够严谨"
Round 3: 6.5/10 — "大部分问题已解决，建议加消融实验"
Round 4: 7/10 — "Almost ready，可以考虑投稿"
```

### 7.3 Workflow 3: 论文写作 (`/paper-writing`)

**目的：从研究叙事/报告自动生成完整的投稿级 PDF 论文**

**你需要提供：** `NARRATIVE_REPORT.md`（研究叙事） 或 `PAPER_PLAN.md`（论文大纲）

**AI 最终产出：** `paper/main.pdf`（完整论文）

**完整流程：**

```
Step 1: /paper-plan — 制定论文大纲                   ⏱ 5-10 min
┌──────────────────────────────────────────────────────────┐
│ ① 解析 NARRATIVE_REPORT.md 提取核心论点和证据           │
│ ② 构建 Claims-Evidence 矩阵（每个论点对应证据）         │
│ ③ 设计分节结构（5-8 节）                                │
│ ④ 规划图表放置位置                                      │
│ ⑤ GPT-5.4 审查大纲完整性                                │
│ → 输出：PAPER_PLAN.md                                   │
└──────────────────────────────────────────────────────────┘
                              ↓
Step 2: /paper-figure — 生成论文图表                  ⏱ 5-15 min
┌──────────────────────────────────────────────────────────┐
│ ① 读取 PAPER_PLAN.md 中的图表计划                       │
│ ② 从 JSON/CSV 数据生成 matplotlib/seaborn 图表          │
│ ③ 生成 LaTeX 对比表格                                   │
│ ④ 创建 figures/latex_includes.tex                       │
│ → 输出：figures/ 目录（PDF图表 + LaTeX代码片段）         │
│ ⚠️ 架构图等需要手动创建                                  │
└──────────────────────────────────────────────────────────┘
                              ↓
Step 3: /paper-write — 逐节写 LaTeX                   ⏱ 15-30 min
┌──────────────────────────────────────────────────────────┐
│ ① 按照大纲逐节生成 LaTeX 内容                           │
│ ② 插入图表引用                                          │
│ ③ 构建 references.bib                                   │
│ ④ 去 AI 化处理（删除 delve、pivotal 等 AI 常用词）      │
│ ⑤ GPT-5.4 逐节审查质量                                  │
│ → 输出：paper/ 目录（main.tex + sections/ + .bib）      │
└──────────────────────────────────────────────────────────┘
                              ↓
Step 4: /paper-compile — 编译 PDF                     ⏱ 2-5 min
┌──────────────────────────────────────────────────────────┐
│ ① latexmk 多遍编译                                      │
│ ② 自动修复编译错误（缺宏包、未定义引用等）              │
│ ③ 最多尝试 3 次                                         │
│ ④ pdftotext 验证页数                                    │
│ → 输出：paper/main.pdf                                  │
└──────────────────────────────────────────────────────────┘
                              ↓
Step 5: /auto-paper-improvement-loop — 润色           ⏱ 15-30 min
┌──────────────────────────────────────────────────────────┐
│ Round 1:                                                 │
│   GPT-5.4 审全文 → 标记 CRITICAL/MAJOR/MINOR 问题       │
│   → Claude 修复 → 重新编译 → 保存 main_round1.pdf       │
│                                                          │
│ Round 2:                                                 │
│   GPT-5.4 再审 → 标记剩余问题                           │
│   → Claude 修复 → 重新编译 → 保存 main_round2.pdf       │
│                                                          │
│ 典型改进：                                               │
│   ├─ 修正假设-模型不匹配                                │
│   ├─ 软化过度声称（使论点与证据匹配）                    │
│   ├─ 加强 Limitations 部分                               │
│   └─ 修复排版溢出                                        │
│                                                          │
│ → 输出：3 个 PDF（round0原始、round1、round2）           │
│         + PAPER_IMPROVEMENT_LOG.md                       │
└──────────────────────────────────────────────────────────┘
```

### 7.4 全流程一键：`/research-pipeline`

**这是终极命令**——把 Workflow 1、代码实现、Workflow 2 全部串起来：

```
/research-pipeline "你的研究方向"

执行顺序：
├─ Stage 1: /idea-discovery     ← Workflow 1（30-60 min）
│     ├─ /research-lit
│     ├─ /idea-creator
│     ├─ /novelty-check
│     └─ /research-review
│
├─ 🚦 Gate 1: 展示创意排名
│     └─ AUTO_PROCEED=true → 自动选排名第一的
│     └─ AUTO_PROCEED=false → 等你确认选哪个
│
├─ Stage 2: 代码实现             ← 自动写实验代码（15-60 min）
│
├─ Stage 3: /run-experiment      ← 部署实验（5 min + 实验时间）
│
├─ Stage 4: /auto-review-loop    ← Workflow 2（1-4 h）
│     └─ 4 轮 GPT审稿 + Claude修改
│
└─ Stage 5: 最终报告              ← 生成 Pipeline Report

💡 最佳实践：晚上启动，早上看结果
```

---

## 八、所有 Skills 用法手册

### 8.1 `/arxiv` — arXiv 论文搜索 🟢

**最简单的入门命令，不需要任何外部依赖。**

```
# 基本搜索
> /arxiv "attention mechanism"

# 搜索并指定结果数量
> /arxiv "TDCIPP neurotoxicity" — max: 20

# 下载特定论文
> /arxiv "2301.07041" — download

# 搜索并下载所有结果的 PDF
> /arxiv "organophosphate flame retardant" — download: all

# 保存到自定义目录
> /arxiv "query" — dir: literature/
```

**输出示例：**
```
| # | arXiv ID   | Title                              | Authors        | Date       |
|---|------------|------------------------------------| --------------|------------|
| 1 | 2501.12345 | TDCIPP exposure and brain...       | Zhang et al.   | 2025-01-15 |
| 2 | 2412.67890 | Organophosphate neurotoxicity...   | Li et al.      | 2024-12-20 |
```

### 8.2 `/research-lit` — 文献综述 🟢

**多源文献搜索和综合分析。**

```
# 默认搜索所有来源（本地 PDF + arXiv + Scholar + Web）
> /research-lit "TDCIPP prenatal exposure neurodevelopment"

# 只搜索网络
> /research-lit "topic" — sources: web

# 搜索并下载 arXiv PDF
> /research-lit "topic" — arxiv download: true

# 指定本地论文目录
> /research-lit "topic" — paper library: ~/my_papers/
```

**数据来源优先级：**
1. Zotero（如果配了 MCP）
2. Obsidian（如果配了 MCP）
3. 本地 PDF（papers/ 或 literature/ 目录）
4. 网络搜索（arXiv API + WebSearch）

### 8.3 `/research-review` — 单轮深度审稿 🟡

```
# 审查一段研究描述
> /research-review "我们提出了 OmicsToHH 框架..."

# 审查一个文件
> /research-review "PAPER_PLAN.md"
```

**GPT-5.4 会返回：**
- 总体评分（1-10）
- 优势列表
- 弱点列表（按严重程度排序）
- 具体改进建议
- 最小可行改进方案

### 8.4 `/idea-creator` — 创意生成 🟡

```
> /idea-creator "TDCIPP prenatal exposure mechanisms"
```

**流程：搜索文献 → GPT-5.4 生成 8-12 个创意 → 筛选 → pilot 实验 → 输出 IDEA_REPORT.md**

### 8.5 `/novelty-check` — 新颖性验证 🟡

```
> /novelty-check "OmicsToHH: mapping gene expression to HH parameters"
```

**流程：多源文献搜索 → GPT-5.4 交叉验证 → 找最相似已有工作 → 判定新颖/非新颖**

### 8.6 `/paper-plan` — 论文大纲 🟡

```
> /paper-plan "NARRATIVE_REPORT.md"
```

**输出：PAPER_PLAN.md，包含 Claims-Evidence 矩阵、分节计划、图表计划、引文框架**

### 8.7 `/paper-figure` — 生成图表 🟢

```
> /paper-figure "PAPER_PLAN.md"
```

**从 JSON/CSV 数据自动生成 matplotlib/seaborn 图表 + LaTeX 表格**

### 8.8 `/paper-write` — 写 LaTeX 🟡

```
> /paper-write "PAPER_PLAN.md"
```

**按大纲逐节生成 LaTeX，支持 ICLR/NeurIPS/ICML 模板**

### 8.9 `/paper-compile` — 编译 PDF 🟢

```
> /paper-compile "paper/"
```

**latexmk 编译 + 自动修复错误 + 验证页数**

---

## 九、实战案例：手把手教程

### 9.1 新手第一次体验（5 分钟）

**目标：用最简单的命令验证环境可用**

```powershell
# 打开终端
cd E:\Git-hub_project\Auto-claude-code-research-in-sleep
claude

# 在 Claude Code 中输入：
> /arxiv "deep learning drug screening"
```

**预期结果：** Claude 会搜索 arXiv，显示一个论文列表。如果你看到了表格，说明环境没问题。

### 9.2 案例：TDCIPP 神经毒理学研究（完整流程）

**Day 1: 文献综述**
```powershell
cd K:\shi_hao_nan_shuoshi_ke_ti\Topic_Pregnancy_Exposure_Neurodevelopment
claude

> /research-lit "TDCIPP prenatal exposure neurodevelopmental toxicity mechanisms 2024 2025"

# 等待 5-15 分钟
# 输出：文献综述表格 + 研究图景分析
```

**Day 2: 创意发现**
```
> /idea-discovery "TDCIPP孕期暴露经甲状腺轴干扰和线粒体代谢重编程致胶质细胞Crosstalk中断的神经发育毒性机制"

# 等待 30-120 分钟
# 输出：IDEA_REPORT.md
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

> /auto-review-loop "VirtualNeuronTox: a three-target biophysical simulation framework for TDCIPP neurotoxicology"

# 然后去睡觉 💤
# 第二天早上看 AUTO_REVIEW.md
```

**Day 5: 写论文**
```
> /paper-writing "NARRATIVE_REPORT.md"

# 等待 1-3 小时
# 输出在 paper/ 目录：main.pdf
```

### 9.3 推荐的项目目录结构

```
你的研究项目/
├── CLAUDE.md             # ⭐ 项目说明（Claude Code 启动时会读这个文件）
├── NARRATIVE_REPORT.md   # 研究叙事（/paper-writing 的输入）
├── PAPER_PLAN.md         # 论文大纲（/paper-plan 输出）
├── IDEA_REPORT.md        # 创意报告（/idea-discovery 输出）
├── REVIEW_STATE.json     # 审稿状态（断点续传用）
├── AUTO_REVIEW.md        # 审稿记录（/auto-review-loop 输出）
├── papers/               # 本地论文库（PDF）
├── src/                  # 你的代码
├── data/                 # 数据
├── experiments/          # 实验结果
├── figures/              # 图表（/paper-figure 输出）
└── paper/                # 生成的论文（/paper-writing 输出）
    ├── main.tex
    ├── sections/
    ├── references.bib
    └── main.pdf
```

**CLAUDE.md 的作用：** 这是项目的"自我介绍"文件。Claude Code 启动时会自动读取它，了解你的项目背景。内容越详细，AI 工作越精准。

**CLAUDE.md 示例：**
```markdown
# VirtualNeuronTox

## 项目概述
- 研究方向：TDCIPP 孕期暴露致神经发育障碍的计算毒理学
- 三个核心模块：OmicsToHH, VirtualNeuronTox, NeuroCellHet

## 环境
- Python 3.12, PyTorch 2.x
- 数据：Allen Brain Atlas Patch-seq (2333 cells)

## 前期结果
- 合成数据训练 R²=0.47
- 真实数据训练 R²=0.36
- TDCIPP 仿真：DA 神经元 ♂ AP -19.7% vs ♀ -5.5%

## 当前问题
- 真实数据 R² 较低，需要改进特征工程
- 需要更多细胞类型的验证
```

---

## 十、高级配置

### 10.1 修改 Codex 审稿模型

```powershell
notepad C:\Users\17372\.codex\config.toml
```

可选模型：
```toml
model = "gpt-5.4"         # 最佳（推荐，当前配置）
model = "gpt-5.3-codex"   # 次选
model = "o3"              # 推理型
```

### 10.2 修改 Skill 参数

所有参数都在对应的 SKILL.md 文件开头定义，可以直接修改：

```powershell
# 修改审稿循环参数
notepad C:\Users\17372\.claude\skills\auto-review-loop\SKILL.md

# 可修改的关键参数：
# MAX_ROUNDS = 4            ← 最多审稿轮数
# POSITIVE_THRESHOLD = 6/10 ← 达到此分数停止
# REVIEWER_MODEL = gpt-5.4  ← 审稿用的模型
```

```powershell
# 修改创意发现参数
notepad C:\Users\17372\.claude\skills\idea-discovery\SKILL.md

# 可修改的关键参数：
# PILOT_MAX_HOURS = 2       ← 单个 pilot 实验最长时间
# MAX_PILOT_IDEAS = 3       ← 最多跑几个 pilot
# AUTO_PROCEED = true       ← 检查点是否自动继续
# ARXIV_DOWNLOAD = false    ← 是否下载 arXiv PDF
```

### 10.3 添加飞书通知（可选）

配置后，审稿完成、实验结束等关键节点会推送飞书消息：

```powershell
# 创建飞书配置
notepad C:\Users\17372\.claude\feishu.json
```

```json
{
  "mode": "push",
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/你的WEBHOOK_ID"
}
```

### 10.4 配置 GPU 服务器（可选）

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

## 十一、故障排除

### 11.1 常见问题速查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| `claude` 命令不存在 | 未安装 Claude Code | `npm install -g @anthropic-ai/claude-code` |
| `/idea-discovery` 在 Cursor 中不识别 | Cursor 不支持 `/` 语法 | 改用 Claude Code CLI，或用自然语言 |
| Codex MCP 报错 | 网络/代理问题 | 确认 `HTTP_PROXY=http://127.0.0.1:7897` |
| Codex MCP 超时 | Codex CLI 版本旧或网络慢 | 更新 Codex CLI，检查代理 |
| LaTeX 编译失败 | 缺少宏包 | MiKTeX 会自动下载，或 `miktex packages install xxx` |
| 审稿循环中断 | 上下文窗口满了 | 自动从 `REVIEW_STATE.json` 恢复，重新运行即可 |
| GPT-5.4 评分一直很低 | 研究确实有问题 | 认真看审稿意见，先手动改进再重跑 |
| Claude Code 卡住不动 | 等待用户输入 | 检查是否到了检查点，需要你回复 |
| `arXiv API` 返回空 | 关键词不对或API限流 | 换英文关键词，等几分钟重试 |

### 11.2 验证环境的命令

```powershell
# 验证 Claude Code
claude --version

# 验证 Codex
E:\software\codex --version

# 验证 LaTeX
pdflatex --version
latexmk --version

# 验证 PDF 工具
pdfinfo -v
pdftotext -v

# 验证 Python
python --version

# 验证代理（如果需要）
curl -x http://127.0.0.1:7897 https://api.openai.com
```

### 11.3 重要文件位置

```
配置文件：
  C:\Users\17372\.claude\settings.json        # Claude Code 全局配置
  C:\Users\17372\.claude\settings.local.json   # Auto-Allow 配置
  C:\Users\17372\.codex\config.toml            # Codex 模型配置
  C:\Users\17372\.cursor\mcp.json              # Cursor MCP 配置

Skill 文件：
  C:\Users\17372\.claude\skills\               # 所有 ARIS Skills

项目：
  E:\Git-hub_project\Auto-claude-code-research-in-sleep\  # ARIS 源码
```

---

## 十二、常见误解 FAQ

### Q1：ARIS 能完全替代我做科研吗？

**不能。** ARIS 擅长自动化重复性工作（搜文献、格式化、编译、审稿改稿），但：
- 研究方向的选择需要你的专业判断
- 实验设计的关键决策需要你确认
- 最终论文质量需要你审核
- AI 不能替代领域专家的洞察力

### Q2：跑一次全流程要花多少钱？

- arXiv 搜索：免费
- 文献综述：仅 Claude API 费用
- 创意发现（含 GPT 审查）：约 $1-3
- 自动审稿 4 轮：约 $5-15
- 论文写作：约 $3-8
- 全流程：约 $10-25

### Q3：我没有 GPU 服务器，能用吗？

**能用大部分功能。** 只有 `/run-experiment`、`/monitor-experiment`、`/dse-loop` 需要 GPU。其他所有 Skill 都在本地运行。

### Q4：为什么有些命令需要 Codex MCP？

标记为"需要 Codex"的命令会调用 GPT-5.4 做审查/评分。如果 Codex MCP 不可用，这些命令会报错。你可以只使用不需要 Codex 的命令（标记为 🟢 的）。

### Q5：我可以修改 Skill 的行为吗？

**可以！** Skill 就是普通的 Markdown 文件。打开 `C:\Users\17372\.claude\skills\<skill名>\SKILL.md`，修改里面的步骤或参数即可。修改后立即生效，不需要重启。

### Q6：ARIS 生成的论文能直接投稿吗？

**建议不要直接投。** ARIS 生成的论文是很好的初稿，但你应该：
1. 仔细阅读并修改内容
2. 确认所有数据和结论的准确性
3. 检查引用的论文是否真实存在（AI 可能幻觉）
4. 根据目标期刊的要求调整格式
5. 请导师和合作者审阅

---

## 附录

### A. 你的环境信息

```
OS: Windows 10 (build 26200)
Claude Code: v2.1.76
Codex: v0.114.0 (E:\software\codex)
Codex Model: gpt-5.4, reasoning_effort: xhigh
Python: 3.12
Proxy: http://127.0.0.1:7897
LaTeX: MiKTeX 25.12 (Portable, via Scoop)
Poppler: 24.04.0 (via Scoop)
Skills Count: 77 (22 ARIS核心 + 55 通用)
```

### B. 完整 Skill 列表

运行以下命令查看所有已安装的 Skill：
```powershell
Get-ChildItem "C:\Users\17372\.claude\skills" -Directory | ForEach-Object { $_.Name }
```

### C. 快速命令参考卡

```
┌──────────────────────────── ARIS 快速参考 ─────────────────────────────┐
│                                                                        │
│  🟢 不需要 Codex（立即可用）                                           │
│     /arxiv "关键词"              搜索 arXiv 论文                       │
│     /research-lit "主题"         多源文献综述                          │
│     /paper-compile "paper/"      编译 LaTeX → PDF                     │
│     /analyze-results data/       分析实验结果                         │
│     /pixel-art "描述"            生成像素风 SVG                       │
│                                                                        │
│  🟡 需要 Codex MCP                                                    │
│     /idea-discovery "方向"       Workflow 1：从方向到创意              │
│     /auto-review-loop "主题"     Workflow 2：自动审稿循环             │
│     /paper-writing "报告.md"     Workflow 3：从报告到论文             │
│     /research-pipeline "方向"    全流程一键                           │
│     /research-review "摘要"      单轮审稿                             │
│     /idea-creator "方向"         创意生成                             │
│     /novelty-check "创意"        新颖性验证                           │
│                                                                        │
│  🔴 需要 GPU 服务器                                                   │
│     /run-experiment              部署实验                              │
│     /monitor-experiment          监控实验                              │
│     /dse-loop                    设计空间探索                         │
│                                                                        │
│  参数覆盖示例：                                                        │
│     /idea-discovery "x" — AUTO_PROCEED: false                         │
│     /auto-review-loop "x" — MAX_ROUNDS: 6                            │
│     /paper-writing "x" — venue: NeurIPS                               │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```
