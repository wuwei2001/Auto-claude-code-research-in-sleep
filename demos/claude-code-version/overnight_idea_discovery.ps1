# ARIS 过夜创意发现脚本
#
# 用法: 睡觉前运行此脚本，让 ARIS 自动完成从文献综述到创意发现的完整流程
# .\overnight_idea_discovery.ps1 "你的研究方向"
#
# 可选参数:
#   -DownloadPDF    同时下载 arXiv PDF
#   -ManualMode     手动确认模式（每步等待确认）
#
# 此脚本会：
# 1. 检查环境和网络
# 2. 确认电源设置
# 3. 启动 Claude Code 并运行 /idea-discovery
# 4. 自动完成: 文献综述 → 创意生成 → 新颖性验证 → 专家审查

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Direction,

    [switch]$DownloadPDF,
    [switch]$ManualMode
)

$ErrorActionPreference = "Continue"

function Write-Banner {
    param([string]$Text, [ConsoleColor]$Color = "Cyan")
    Write-Host ""
    Write-Host ("=" * 64) -ForegroundColor $Color
    Write-Host "  $Text" -ForegroundColor $Color
    Write-Host ("=" * 64) -ForegroundColor $Color
    Write-Host ""
}

function Write-Check {
    param([string]$Label, [bool]$Pass, [string]$Detail = "")
    $icon = if ($Pass) { "[OK]" } else { "[!!]" }
    $color = if ($Pass) { "Green" } else { "Red" }
    Write-Host "  $icon $Label" -ForegroundColor $color -NoNewline
    if ($Detail) { Write-Host " — $Detail" -ForegroundColor DarkGray } else { Write-Host "" }
}

Write-Banner "ARIS Overnight Idea Discovery" "Magenta"

Write-Host "  Research Direction:" -ForegroundColor White
Write-Host "    $Direction" -ForegroundColor Yellow
Write-Host ""
if ($ManualMode) {
    Write-Host "  Mode: MANUAL (will pause at each checkpoint)" -ForegroundColor Yellow
} else {
    Write-Host "  Mode: AUTO (fully autonomous, ideal for overnight)" -ForegroundColor Green
}
Write-Host ""

# ── 环境检查 ──
Write-Banner "Environment Check"

$allGood = $true

# Claude Code
$claudeOk = $false
try {
    $ver = claude --version 2>&1
    $claudeOk = $true
    Write-Check "Claude Code CLI" $true $ver
} catch {
    Write-Check "Claude Code CLI" $false "Not found — npm install -g @anthropic-ai/claude-code"
    $allGood = $false
}

# Codex
$codexOk = $false
if (Test-Path "E:\software\codex") {
    $cver = & "E:\software\codex" --version 2>&1
    $codexOk = $true
    Write-Check "Codex CLI" $true $cver
} else {
    Write-Check "Codex CLI" $false "Not found at E:\software\codex"
    $allGood = $false
}

# Skills
$skillDir = "$env:USERPROFILE\.claude\skills"
$skillCount = (Get-ChildItem $skillDir -Directory -ErrorAction SilentlyContinue).Count
$skillOk = $skillCount -gt 0
Write-Check "ARIS Skills" $skillOk "$skillCount skills installed"
if (-not $skillOk) { $allGood = $false }

# Python
$pyOk = $false
try {
    $pyver = python --version 2>&1
    $pyOk = $true
    Write-Check "Python" $true $pyver
} catch {
    Write-Check "Python" $false "Not found"
}

# Network proxy
$proxyOk = $false
try {
    $tcp = Test-NetConnection -ComputerName 127.0.0.1 -Port 7897 -ErrorAction Stop -WarningAction SilentlyContinue
    $proxyOk = $tcp.TcpTestSucceeded
} catch {}
Write-Check "Network proxy (127.0.0.1:7897)" $proxyOk

if (-not $allGood) {
    Write-Host ""
    Write-Host "  [WARNING] Some critical components are missing." -ForegroundColor Red
    Write-Host "  The script will continue, but some skills may not work." -ForegroundColor Yellow
    Write-Host ""
}

# ── 电源和休眠提醒 ──
Write-Banner "Pre-flight Checklist"

Write-Host "  Please verify BEFORE going to sleep:" -ForegroundColor White
Write-Host ""
Write-Host "  [ ] Computer will NOT go to sleep" -ForegroundColor Yellow
Write-Host "      Settings > System > Power > Screen/Sleep > Never" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  [ ] Network proxy stays connected" -ForegroundColor Yellow
Write-Host "      Do NOT close your proxy software" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  [ ] Terminal window stays open" -ForegroundColor Yellow
Write-Host "      Minimize is OK, but do NOT close" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  [ ] Sufficient disk space for PDF downloads" -ForegroundColor Yellow
Write-Host ""

# ── 预计时间 ──
Write-Banner "Expected Timeline"

Write-Host "  Phase 1: Literature Survey      5-15 min" -ForegroundColor White
Write-Host "  Phase 2: Idea Generation       10-30 min" -ForegroundColor White
Write-Host "  Phase 3: Novelty Check          5-15 min" -ForegroundColor White
Write-Host "  Phase 4: Expert Review          5-10 min" -ForegroundColor White
Write-Host "  Phase 5: Report Generation      2-5  min" -ForegroundColor White
Write-Host "  ──────────────────────────────────────────" -ForegroundColor DarkGray
Write-Host "  Total:                         30-120 min" -ForegroundColor Green
Write-Host ""
Write-Host "  Output files:" -ForegroundColor DarkGray
Write-Host "    IDEA_REPORT.md          — ranked ideas with scores" -ForegroundColor DarkGray
Write-Host "    LITERATURE_SUMMARY.md   — literature landscape" -ForegroundColor DarkGray
Write-Host "    papers/                 — downloaded PDFs (if enabled)" -ForegroundColor DarkGray
Write-Host ""

# ── 构建命令 ──
$cmd = "/idea-discovery `"$Direction`""

if ($DownloadPDF) {
    $cmd += " — arxiv download: true"
}
if ($ManualMode) {
    $cmd += " — AUTO_PROCEED: false"
}

Write-Banner "Launching Claude Code" "Green"

Write-Host "  Command: $cmd" -ForegroundColor White
Write-Host ""
Write-Host "  You can go to sleep now!" -ForegroundColor Green
Write-Host "  Check IDEA_REPORT.md in the morning." -ForegroundColor Green
Write-Host ""

# 启动 Claude Code
claude -p $cmd
