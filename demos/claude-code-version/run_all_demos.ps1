# ARIS 所有 Skill 演示脚本 — Claude Code 版本
#
# 此脚本展示如何在 Claude Code CLI 中逐步运行每个 ARIS Skill。
# 不是自动执行，而是打印每个命令让你手动复制执行。
#
# 用法: .\run_all_demos.ps1

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  ARIS All Skills Demo — Claude Code CLI Version" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  以下是按难度排序的所有演示命令。" -ForegroundColor White
Write-Host "  先启动 Claude Code (输入 'claude')，然后逐个尝试。" -ForegroundColor White
Write-Host ""

Write-Host "================================================================" -ForegroundColor Green
Write-Host "  Level 1: 基础 (不需要 Codex MCP)" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "  Demo 1.1: arXiv 搜索" -ForegroundColor Yellow
Write-Host "  ────────────────────────" -ForegroundColor DarkGray
Write-Host '  > /arxiv "drug toxicity neural network prediction"' -ForegroundColor White
Write-Host '  > /arxiv "Hodgkin-Huxley parameter estimation" — max: 10' -ForegroundColor White
Write-Host '  > /arxiv "2403.18997" — download' -ForegroundColor DarkGray
Write-Host '  > /arxiv "virtual cell modeling" — download: all — dir: papers/' -ForegroundColor DarkGray
Write-Host ""

Write-Host "  Demo 1.2: 文献综述" -ForegroundColor Yellow
Write-Host "  ────────────────────────" -ForegroundColor DarkGray
Write-Host '  > /research-lit "virtual cell digital twin drug toxicity screening"' -ForegroundColor White
Write-Host '  > /research-lit "方向" — sources: web' -ForegroundColor DarkGray
Write-Host '  > /research-lit "方向" — arxiv download: true' -ForegroundColor DarkGray
Write-Host ""

Write-Host "  Demo 1.3: 像素画 (好玩的)" -ForegroundColor Yellow
Write-Host "  ────────────────────────" -ForegroundColor DarkGray
Write-Host '  > /pixel-art "两个科学家在讨论虚拟细胞"' -ForegroundColor White
Write-Host ""

Write-Host "================================================================" -ForegroundColor Yellow
Write-Host "  Level 2: 进阶 (需要 Codex MCP)" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "  Demo 2.1: 单轮审稿 (5-10 min)" -ForegroundColor Yellow
Write-Host "  ────────────────────────────────" -ForegroundColor DarkGray
Write-Host '  > /research-review "VirtualCellPlatform: multi-scale virtual cell' -ForegroundColor White
Write-Host '    modeling framework mapping single-cell omics to biophysical' -ForegroundColor White
Write-Host '    parameters. R2=0.47 synthetic, R2=0.36 real data."' -ForegroundColor White
Write-Host ""

Write-Host "  Demo 2.2: 新颖性验证 (5-10 min)" -ForegroundColor Yellow
Write-Host "  ────────────────────────────────" -ForegroundColor DarkGray
Write-Host '  > /novelty-check "Perturbation-Native Virtual Cell Twin:' -ForegroundColor White
Write-Host '    directly train virtual cell digital twins on dose-time-resolved' -ForegroundColor White
Write-Host '    single-cell perturbation datasets with toxicity endpoints"' -ForegroundColor White
Write-Host ""

Write-Host "  Demo 2.3: 创意生成 (10-30 min)" -ForegroundColor Yellow
Write-Host "  ────────────────────────────────" -ForegroundColor DarkGray
Write-Host '  > /idea-creator "virtual cell digital twin for drug toxicity"' -ForegroundColor White
Write-Host ""

Write-Host "================================================================" -ForegroundColor Magenta
Write-Host "  Level 3: Workflow (长时间运行)" -ForegroundColor Magenta
Write-Host "================================================================" -ForegroundColor Magenta
Write-Host ""

Write-Host "  Demo 3.1: 创意发现 Workflow 1 (30-120 min)" -ForegroundColor Yellow
Write-Host "  ──────────────────────────────────────────────" -ForegroundColor DarkGray
Write-Host '  > /idea-discovery "virtual cell digital twin for drug toxicity"' -ForegroundColor White
Write-Host ""

Write-Host "  Demo 3.2: 自动审稿 Workflow 2 (2-8 h, 适合过夜)" -ForegroundColor Yellow
Write-Host "  ──────────────────────────────────────────────────" -ForegroundColor DarkGray
Write-Host '  > /auto-review-loop "VirtualCellPlatform: multi-scale modeling"' -ForegroundColor White
Write-Host ""

Write-Host "  Demo 3.3: 论文写作 Workflow 3 (1-3 h)" -ForegroundColor Yellow
Write-Host "  ──────────────────────────────────────" -ForegroundColor DarkGray
Write-Host '  > /paper-writing "NARRATIVE_REPORT.md"' -ForegroundColor White
Write-Host '  > /paper-writing "NARRATIVE_REPORT.md" — venue: NeurIPS' -ForegroundColor DarkGray
Write-Host ""

Write-Host "  Demo 3.4: 全流程一键 (一整晚)" -ForegroundColor Yellow
Write-Host "  ────────────────────────────" -ForegroundColor DarkGray
Write-Host '  > /research-pipeline "virtual cell digital twin drug toxicity"' -ForegroundColor White
Write-Host ""

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  Ready to start? Type 'claude' to launch Claude Code." -ForegroundColor White
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

$choice = Read-Host "Press Enter to start Claude Code, or 'q' to quit"
if ($choice -ne 'q') {
    claude
}
