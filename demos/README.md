# ARIS 演示案例

> 本目录包含两个版本的 ARIS 使用演示，分别展示如何在 Cursor 和 Claude Code CLI 中使用 ARIS Skills。
> 所有演示结果均为 2026-03-15 实际运行获得，包含真实的 GPT-5.4 审稿意见和 arXiv 搜索结果。

## 目录结构

```
demos/
├── README.md                                  ← 本文件（总览）
│
├── cursor-version/                            ← Cursor IDE 版本
│   ├── README.md                              ← 完整演示记录（864行, 49.8KB）
│   │   ├── /research-review 演示（GPT-5.4 审稿, 3/10, 8个弱点详解）
│   │   ├── /arxiv 演示（9篇论文 + PDF 下载）
│   │   ├── /research-lit 演示（GPT-5.4 文献综合分析）
│   │   ├── /novelty-check 演示（创意新颖性验证, 8个已有工作对比）
│   │   └── 完整操作流程总览（ASCII 流程图 + 所有命令参数）
│   ├── DEMO_REPORT.md                         ← 同内容备份
│   ├── arxiv_search_demo.py                   ← 可运行: arXiv 搜索 + PDF 下载
│   ├── research_review_demo.py                ← 可运行: 审稿演示（含预录制结果）
│   └── novelty_check_demo.py                  ← 可运行: 新颖性验证演示
│
└── claude-code-version/                       ← Claude Code CLI 版本
    ├── README.md                              ← 完整教程（568行, 23.7KB）
    │   ├── 12 章节一步一步教程
    │   ├── 从首次体验到全流程一键
    │   ├── 每步的预期输出和参数说明
    │   └── 故障排除
    ├── quick_start.ps1                        ← 快速启动（检查环境+启动 Claude Code）
    ├── overnight_review.ps1                   ← 过夜审稿脚本
    ├── run_all_demos.ps1                      ← 所有 Skill 演示命令列表
    ├── demo_results_reference.md              ← 预期结果参考（与 Cursor 版本对照）
    └── CLAUDE.md.template                     ← 项目说明模板
```

## 演示了哪些 ARIS Skill？

| Skill | Cursor 版本 | Claude Code 版本 | 结果概要 |
|-------|------------|-----------------|---------|
| `/arxiv` | ✅ Python 脚本 | ✅ 命令参考 | 搜索 9 篇论文 + 下载 3 个 PDF |
| `/research-review` | ✅ GPT-5.4 实际审稿 | ✅ 结果参考 | 评分 3/10, 8 个弱点 |
| `/research-lit` | ✅ GPT-5.4 文献分析 | ✅ 结果参考 | 4 大方向 + 5 个空白 |
| `/novelty-check` | ✅ GPT-5.4 新颖性验证 | ✅ 结果参考 | PARTIALLY NOVEL, 8 个已有工作 |
| `/idea-discovery` | 📝 流程说明 | ✅ 详细教程 | — |
| `/auto-review-loop` | 📝 流程图 | ✅ 详细教程 + 脚本 | — |
| `/paper-writing` | 📝 流程说明 | ✅ 详细教程 | — |
| `/research-pipeline` | 📝 流程说明 | ✅ 详细教程 | — |

## 快速开始

### Cursor 版本

```powershell
cd demos\cursor-version

# arXiv 搜索
python arxiv_search_demo.py "drug toxicity prediction"
python arxiv_search_demo.py "virtual cell modeling" --max 10 --download-all

# 查看审稿演示结果
python research_review_demo.py --demo

# 查看新颖性验证结果
python novelty_check_demo.py --demo
```

### Claude Code 版本

```powershell
cd demos\claude-code-version

# 方法 1: 快速启动
.\quick_start.ps1

# 方法 2: 查看所有命令
.\run_all_demos.ps1

# 方法 3: 过夜审稿
.\overnight_review.ps1 "你的论文主题"

# 方法 4: 直接启动
claude
> /arxiv "drug toxicity prediction"
```

## 该用哪个版本？

| 场景 | 推荐 |
|------|------|
| 第一次尝试 | Claude Code CLI (`quick_start.ps1`) |
| 写代码+简单搜索 | Cursor |
| 过夜自动任务 | Claude Code CLI (`overnight_review.ps1`) |
| 查看演示结果 | 两个都看 |
