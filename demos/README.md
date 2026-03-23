# ARIS 演示案例

> 本目录包含两个版本的 ARIS 使用演示，分别展示如何在 Cursor 和 Claude Code CLI 中使用 ARIS Skills。
> 所有演示结果均为 2026-03-15 实际运行获得，包含真实的 GPT-5.4 审稿意见和 arXiv 搜索结果。

## 目录结构

```
demos/
├── README.md                                  ← 本文件（总览）
│
├── cursor-version/                            ← Cursor IDE 版本
│   ├── README.md                              ← 完整演示记录（含操作流程、审稿结果、文献分析）
│   ├── DEMO_REPORT.md                         ← 同内容备份
│   │
│   ├── arxiv_search_demo.py                   ← 可运行: arXiv 搜索 + PDF 下载
│   ├── research_lit_demo.py                   ← 可运行: 多源文献综述（arXiv + WebSearch 模拟）
│   ├── research_review_demo.py                ← 可运行: 审稿演示（含预录制结果）
│   ├── novelty_check_demo.py                  ← 可运行: 新颖性验证演示
│   ├── idea_creator_demo.py                   ← 可运行: 创意生成演示
│   ├── workflow_demos.py                      ← 可运行: 所有 Workflow 模拟（9 个演示）
│   └── run_all_demos.py                       ← 统一运行器: 交互式菜单，一键运行全部
│
└── claude-code-version/                       ← Claude Code CLI 版本
    ├── README.md                              ← 完整教程（12 章节一步一步指南）
    │
    ├── quick_start.ps1                        ← 快速启动（检查环境 + 显示命令 + 启动 Claude）
    ├── health_check.ps1                       ← 深度诊断（17 项检查 + 生成报告）
    │
    ├── overnight_review.ps1                   ← 过夜审稿脚本（/auto-review-loop）
    ├── overnight_idea_discovery.ps1            ← 过夜创意发现脚本（/idea-discovery）
    ├── overnight_pipeline.ps1                 ← 过夜全流程脚本（/research-pipeline）
    │
    ├── run_all_demos.ps1                      ← 所有 Skill 演示命令列表
    ├── demo_results_reference.md              ← 预期结果参考（与 Cursor 版本对照）
    │
    ├── CLAUDE.md.template                     ← 项目说明模板（含示例和最佳实践）
    └── NARRATIVE_REPORT.md.template           ← 研究叙事模板（/paper-writing 的输入）
```

## 演示了哪些 ARIS Skill？

| Skill | Cursor 版本 | Claude Code 版本 | 结果概要 |
|-------|------------|-----------------|---------|
| `/arxiv` | ✅ Python 脚本（真实 API） | ✅ 命令参考 | 搜索 9 篇论文 + 下载 3 个 PDF |
| `/research-lit` | ✅ Python 脚本 + GPT-5.4 分析 | ✅ 结果参考 | 4 大方向 + 5 个空白 |
| `/research-review` | ✅ GPT-5.4 实际审稿 | ✅ 结果参考 | 评分 3/10, 8 个弱点 |
| `/novelty-check` | ✅ GPT-5.4 新颖性验证 | ✅ 结果参考 | PARTIALLY NOVEL, 8 个已有工作 |
| `/idea-creator` | ✅ GPT-5.4 创意生成 | ✅ 结果参考 | 5 个创意, 推荐 #1 和 #5 |
| `/analyze-results` | ✅ Workflow 模拟 | ✅ 命令参考 | 统计对比 + 图表生成 |
| `/run-experiment` | ✅ Workflow 模拟 | ✅ 命令参考 | GPU 部署 + screen 会话 |
| `/monitor-experiment` | ✅ Workflow 模拟 | ✅ 命令参考 | 进度查看 + ETA |
| `/feishu-notify` | ✅ Workflow 模拟 | ✅ 命令参考 | 飞书推送实验结果 |
| `/idea-discovery` | ✅ Workflow 模拟 | ✅ 详细教程 + 脚本 | Workflow 1 全流程 |
| `/auto-review-loop` | ✅ Workflow 模拟 | ✅ 详细教程 + 脚本 | Workflow 2 全流程 |
| `/paper-writing` | ✅ Workflow 模拟 | ✅ 详细教程 | Workflow 3 全流程 |
| `/research-pipeline` | ✅ Workflow 模拟 | ✅ 详细教程 + 脚本 | 全流程一键 |
| `/paper-plan` | ✅ Workflow 模拟 | ✅ 命令参考 | Claims-Evidence 矩阵 |
| `/paper-compile` | ✅ Workflow 模拟 | ✅ 命令参考 | LaTeX 编译 + 自动修复 |
| `/pixel-art` | ✅ Workflow 模拟 | ✅ 命令参考 | 像素风 SVG |

## 快速开始

### Cursor 版本

```powershell
cd demos\cursor-version

# 方法 1: 交互式菜单（推荐）
python run_all_demos.py

# 方法 2: 快速演示（每级各一个）
python run_all_demos.py --quick

# 方法 3: 运行特定演示
python arxiv_search_demo.py "drug toxicity prediction"
python research_lit_demo.py --demo
python research_review_demo.py --demo
python novelty_check_demo.py --demo
python idea_creator_demo.py
python workflow_demos.py all

# 方法 4: 按等级运行
python run_all_demos.py --level 1    # 基础 Skill（不需要 Codex）
python run_all_demos.py --level 2    # 进阶 Skill（预录制结果）
python run_all_demos.py --level 3    # Workflow 模拟
```

### Claude Code 版本

```powershell
cd demos\claude-code-version

# 方法 1: 深度环境诊断
.\health_check.ps1

# 方法 2: 快速启动（推荐新手）
.\quick_start.ps1

# 方法 3: 查看所有命令
.\run_all_demos.ps1

# 方法 4: 过夜创意发现
.\overnight_idea_discovery.ps1 "your research direction"

# 方法 5: 过夜审稿
.\overnight_review.ps1 "your paper topic"

# 方法 6: 过夜全流程
.\overnight_pipeline.ps1 "your research direction"

# 方法 7: 直接启动
claude
> /arxiv "drug toxicity prediction"
```

## 该用哪个版本？

| 场景 | 推荐 |
|------|------|
| 第一次尝试 ARIS | Claude Code CLI (`quick_start.ps1`) |
| 了解 ARIS 功能（不安装） | Cursor 版本 (`python run_all_demos.py --quick`) |
| 环境排错 | Claude Code CLI (`health_check.ps1`) |
| 写代码 + 简单搜索 | Cursor |
| 过夜创意发现 | Claude Code CLI (`overnight_idea_discovery.ps1`) |
| 过夜审稿改稿 | Claude Code CLI (`overnight_review.ps1`) |
| 周末全自动科研 | Claude Code CLI (`overnight_pipeline.ps1`) |
| 查看演示结果 | 两个都看 |

## 新增文件说明 (2026-03-16)

### Claude Code 版本新增

| 文件 | 说明 |
|------|------|
| `health_check.ps1` | 17 项深度环境诊断，检查组件/Skills/MCP/网络/磁盘等，生成诊断报告 |
| `overnight_idea_discovery.ps1` | 过夜创意发现专用脚本，含环境检查/电源提醒/时间预估 |
| `overnight_pipeline.ps1` | 过夜全流程脚本(idea→code→experiment→review)，含详细时间线 |
| `NARRATIVE_REPORT.md.template` | `/paper-writing` 输入模板，含示例和字段说明 |
| `CLAUDE.md.template` | 大幅扩充：增加技术栈/数据/ARIS偏好/目录结构等节 |

### Cursor 版本新增

| 文件 | 说明 |
|------|------|
| `research_lit_demo.py` | `/research-lit` 完整演示：arXiv + WebSearch模拟 + 分类 + GPT分析 |
| `run_all_demos.py` | 统一运行器：交互式菜单 / 按等级 / 快速演示 / 指定ID |
| `workflow_demos.py` 新增3个演示 | `analyze-results` / `run-experiment` + `monitor` / `feishu-notify` |
