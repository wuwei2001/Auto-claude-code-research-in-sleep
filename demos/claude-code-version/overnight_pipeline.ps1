# ARIS 过夜全流程脚本 — 从文献综述到投稿就绪
#
# 用法: 周五晚上运行此脚本，周一早上看结果
# .\overnight_pipeline.ps1 "你的研究方向"
#
# 可选参数:
#   -Venue "NeurIPS"   指定目标会议（默认不指定）
#   -DownloadPDF       同时下载 arXiv PDF
#   -ManualMode        手动确认模式
#
# 执行流程:
#   Stage 1: /idea-discovery   — 文献综述 + 创意生成 + 新颖性验证 (30-60 min)
#   Stage 2: 代码实现           — 扩展 pilot 到完整实验 (15-60 min)
#   Stage 3: /run-experiment   — 部署到 GPU (5 min, 需要 GPU)
#   Stage 4: /auto-review-loop — GPT审稿 + Claude修改循环 (1-4 h)
#   Stage 5: 最终报告           — 输出所有产物

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Direction,

    [string]$Venue = "",
    [switch]$DownloadPDF,
    [switch]$ManualMode
)

$ErrorActionPreference = "Continue"

function Write-Banner {
    param([string]$Text, [ConsoleColor]$Color = "Cyan")
    Write-Host ""
    Write-Host ("=" * 68) -ForegroundColor $Color
    Write-Host "  $Text" -ForegroundColor $Color
    Write-Host ("=" * 68) -ForegroundColor $Color
    Write-Host ""
}

function Write-Check {
    param([string]$Label, [bool]$Pass, [string]$Detail = "")
    $icon = if ($Pass) { "[OK]" } else { "[!!]" }
    $color = if ($Pass) { "Green" } else { "Red" }
    Write-Host "  $icon $Label" -ForegroundColor $color -NoNewline
    if ($Detail) { Write-Host " — $Detail" -ForegroundColor DarkGray } else { Write-Host "" }
}

Write-Banner "ARIS Full Research Pipeline — Overnight Mode" "Magenta"

Write-Host "  Research Direction:" -ForegroundColor White
Write-Host "    $Direction" -ForegroundColor Yellow
if ($Venue) {
    Write-Host "  Target Venue: $Venue" -ForegroundColor Yellow
}
Write-Host ""

# ── 环境检查 ──
Write-Banner "Environment Check"

$checks = @()

try { $v = claude --version 2>&1; Write-Check "Claude Code" $true $v } catch { Write-Check "Claude Code" $false }
if (Test-Path "E:\software\codex") {
    $v = & "E:\software\codex" --version 2>&1; Write-Check "Codex CLI" $true $v
} else { Write-Check "Codex CLI" $false }

$sc = (Get-ChildItem "$env:USERPROFILE\.claude\skills" -Directory -ErrorAction SilentlyContinue).Count
Write-Check "ARIS Skills" ($sc -gt 0) "$sc installed"

try { $v = python --version 2>&1; Write-Check "Python" $true $v } catch { Write-Check "Python" $false }

$latexOk = $false
try { $null = Get-Command pdflatex -ErrorAction Stop; $latexOk = $true } catch {}
Write-Check "LaTeX (pdflatex)" $latexOk $(if($latexOk){"Available"}else{"Not found (paper-compile will be skipped)"})

$proxyOk = $false
try { $t = Test-NetConnection -ComputerName 127.0.0.1 -Port 7897 -ErrorAction Stop -WarningAction SilentlyContinue; $proxyOk = $t.TcpTestSucceeded } catch {}
Write-Check "Proxy (127.0.0.1:7897)" $proxyOk

# ── 预估时间线 ──
Write-Banner "Expected Timeline"

$now = Get-Date
$t = @(
    @("Stage 1", "/idea-discovery",   "30-60  min", $now.AddMinutes(0).ToString("HH:mm"),  $now.AddMinutes(60).ToString("HH:mm")),
    @("Gate 1",  "Auto-select idea",  "instant",    $now.AddMinutes(60).ToString("HH:mm"), ""),
    @("Stage 2", "Code implementation","15-60  min", $now.AddMinutes(60).ToString("HH:mm"), $now.AddMinutes(120).ToString("HH:mm")),
    @("Stage 3", "/run-experiment",    "5      min", $now.AddMinutes(120).ToString("HH:mm"),$now.AddMinutes(125).ToString("HH:mm")),
    @("Stage 4", "/auto-review-loop",  "1-4    h",   $now.AddMinutes(125).ToString("HH:mm"),$now.AddMinutes(365).ToString("HH:mm")),
    @("Stage 5", "Final report",       "5      min", $now.AddMinutes(365).ToString("HH:mm"),"")
)

foreach ($row in $t) {
    $label = "{0}: {1}" -f $row[0], $row[1]
    Write-Host ("  {0,-42} {1}" -f $label, $row[2]) -ForegroundColor White
}
Write-Host ""
Write-Host "  Estimated completion: $($now.AddHours(6).ToString('HH:mm')) (pessimistic)" -ForegroundColor Green
Write-Host "  You can leave after:  $($now.AddMinutes(5).ToString('HH:mm'))" -ForegroundColor Green
Write-Host ""

# ── 预飞检查 ──
Write-Banner "Pre-flight Checklist" "Yellow"

Write-Host "  [ ] Computer sleep disabled" -ForegroundColor Yellow
Write-Host "  [ ] Proxy software running" -ForegroundColor Yellow
Write-Host "  [ ] Terminal window pinned" -ForegroundColor Yellow
Write-Host "  [ ] At least 2 GB free disk space" -ForegroundColor Yellow
Write-Host "  [ ] CLAUDE.md in project root (optional but recommended)" -ForegroundColor Yellow
Write-Host ""

# ── 输出文件 ──
Write-Banner "Output Files (check in the morning)"

Write-Host "  Stage 1:" -ForegroundColor DarkGray
Write-Host "    IDEA_REPORT.md            — ranked research ideas" -ForegroundColor White
Write-Host "    LITERATURE_SUMMARY.md     — literature landscape" -ForegroundColor White
Write-Host ""
Write-Host "  Stage 4:" -ForegroundColor DarkGray
Write-Host "    AUTO_REVIEW.md            — multi-round review log" -ForegroundColor White
Write-Host "    REVIEW_STATE.json         — resume state" -ForegroundColor White
Write-Host ""
Write-Host "  Stage 5:" -ForegroundColor DarkGray
Write-Host "    PIPELINE_REPORT.md        — full pipeline summary" -ForegroundColor White
Write-Host ""

# ── 构建命令 ──
$cmd = "/research-pipeline `"$Direction`""

if ($DownloadPDF) { $cmd += " — arxiv download: true" }
if ($ManualMode) { $cmd += " — AUTO_PROCEED: false" }
if ($Venue) { $cmd += " — venue: $Venue" }

Write-Banner "Launching Full Pipeline" "Green"

Write-Host "  Command: $cmd" -ForegroundColor White
Write-Host ""
Write-Host "  The pipeline will run autonomously for 4-12 hours." -ForegroundColor Green
Write-Host "  Sweet dreams!" -ForegroundColor Green
Write-Host ""

$startTime = Get-Date

# 启动 Claude Code
claude -p $cmd

$elapsed = (Get-Date) - $startTime

Write-Banner "Pipeline Complete" "Cyan"
Write-Host "  Total elapsed: $($elapsed.Hours)h $($elapsed.Minutes)m" -ForegroundColor White
Write-Host ""
Write-Host "  Check these files:" -ForegroundColor Yellow
Write-Host "    type IDEA_REPORT.md" -ForegroundColor White
Write-Host "    type AUTO_REVIEW.md" -ForegroundColor White
Write-Host "    type REVIEW_STATE.json" -ForegroundColor White
Write-Host ""
