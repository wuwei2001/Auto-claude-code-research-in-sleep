# ARIS 快速启动脚本 — Claude Code CLI 版本
# 
# 用法: 在 PowerShell 中运行此脚本
# .\quick_start.ps1
#
# 此脚本会：
# 1. 检查所有必要组件是否安装
# 2. 显示可用的 ARIS 命令
# 3. 启动 Claude Code

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  ARIS Quick Start — Environment Check" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Claude Code
Write-Host "[1/5] Claude Code CLI... " -NoNewline
try {
    $ver = claude --version 2>&1
    Write-Host "OK ($ver)" -ForegroundColor Green
} catch {
    Write-Host "NOT FOUND" -ForegroundColor Red
    Write-Host "  Install: npm install -g @anthropic-ai/claude-code" -ForegroundColor Yellow
}

# 检查 Codex
Write-Host "[2/5] Codex CLI... " -NoNewline
if (Test-Path "E:\software\codex") {
    $cver = & "E:\software\codex" --version 2>&1
    Write-Host "OK ($cver)" -ForegroundColor Green
} else {
    Write-Host "NOT FOUND" -ForegroundColor Red
    Write-Host "  Install: npm install -g @openai/codex" -ForegroundColor Yellow
}

# 检查 Skills
Write-Host "[3/5] ARIS Skills... " -NoNewline
$skillCount = (Get-ChildItem "$env:USERPROFILE\.claude\skills" -Directory -ErrorAction SilentlyContinue).Count
if ($skillCount -gt 0) {
    Write-Host "OK ($skillCount skills installed)" -ForegroundColor Green
} else {
    Write-Host "NOT FOUND" -ForegroundColor Red
    Write-Host "  Install: cp -r skills/* ~/.claude/skills/" -ForegroundColor Yellow
}

# 检查 LaTeX
Write-Host "[4/5] LaTeX (pdflatex)... " -NoNewline
try {
    $null = Get-Command pdflatex -ErrorAction Stop
    Write-Host "OK" -ForegroundColor Green
} catch {
    Write-Host "NOT FOUND (optional, needed for /paper-writing)" -ForegroundColor Yellow
}

# 检查 Python
Write-Host "[5/5] Python... " -NoNewline
try {
    $pyver = python --version 2>&1
    Write-Host "OK ($pyver)" -ForegroundColor Green
} catch {
    Write-Host "NOT FOUND" -ForegroundColor Red
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Available ARIS Commands" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Green = No Codex needed (immediate)" -ForegroundColor Green
Write-Host "  Yellow = Needs Codex MCP" -ForegroundColor Yellow
Write-Host ""
Write-Host "  /arxiv `"keyword`"              Search arXiv papers" -ForegroundColor Green
Write-Host "  /research-lit `"topic`"          Literature review" -ForegroundColor Green
Write-Host "  /paper-compile `"paper/`"        Compile LaTeX to PDF" -ForegroundColor Green
Write-Host "  /analyze-results data/         Analyze experiment results" -ForegroundColor Green
Write-Host "  /pixel-art `"description`"       Generate pixel art SVG" -ForegroundColor Green
Write-Host ""
Write-Host "  /idea-discovery `"direction`"    Workflow 1: Find research ideas" -ForegroundColor Yellow
Write-Host "  /auto-review-loop `"topic`"      Workflow 2: Auto review loop" -ForegroundColor Yellow
Write-Host "  /paper-writing `"report.md`"     Workflow 3: Write paper" -ForegroundColor Yellow
Write-Host "  /research-pipeline `"dir`"       Full pipeline (all workflows)" -ForegroundColor Yellow
Write-Host "  /research-review `"abstract`"    Single review round" -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Starting Claude Code..." -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Type your command after the > prompt" -ForegroundColor White
Write-Host "  Example: /arxiv `"drug toxicity prediction`"" -ForegroundColor White
Write-Host "  Exit: /quit or Ctrl+C twice" -ForegroundColor White
Write-Host ""

# 启动 Claude Code
claude
