# ARIS 深度环境诊断脚本
#
# 用法: .\health_check.ps1
#
# 比 quick_start.ps1 更全面的检查，包括：
# - 所有必要组件的版本和路径
# - MCP 服务器配置状态
# - Skills 安装完整性
# - 网络连通性（代理、arXiv API、OpenAI API）
# - 磁盘空间
# - 电源策略
# - 生成可分享的诊断报告

$ErrorActionPreference = "Continue"

function Write-Banner {
    param([string]$Text, [ConsoleColor]$Color = "Cyan")
    Write-Host ""
    Write-Host ("=" * 68) -ForegroundColor $Color
    Write-Host "  $Text" -ForegroundColor $Color
    Write-Host ("=" * 68) -ForegroundColor $Color
    Write-Host ""
}

function Test-Item {
    param(
        [string]$Label,
        [bool]$Pass,
        [string]$Detail = "",
        [string]$FixHint = ""
    )
    $icon  = if ($Pass) { "[PASS]" } else { "[FAIL]" }
    $color = if ($Pass) { "Green"  } else { "Red"    }
    Write-Host "  $icon " -ForegroundColor $color -NoNewline
    Write-Host "$Label" -NoNewline
    if ($Detail) { Write-Host " — $Detail" -ForegroundColor DarkGray } else { Write-Host "" }
    if (-not $Pass -and $FixHint) {
        Write-Host "         Fix: $FixHint" -ForegroundColor Yellow
    }

    return [PSCustomObject]@{ Label=$Label; Pass=$Pass; Detail=$Detail }
}

$report = @()
$totalPass = 0
$totalFail = 0

# ══════════════════════════════════════════════════════════════════════
Write-Banner "1. Core Components"
# ══════════════════════════════════════════════════════════════════════

# Claude Code
$claudeVer = ""
try { $claudeVer = (claude --version 2>&1).ToString().Trim() } catch {}
$r = Test-Item "Claude Code CLI" ($claudeVer -ne "") $claudeVer "npm install -g @anthropic-ai/claude-code"
$report += $r; if ($r.Pass) { $totalPass++ } else { $totalFail++ }

# Codex CLI
$codexVer = ""
$codexPath = "E:\software\codex"
if (Test-Path $codexPath) {
    try { $codexVer = (& $codexPath --version 2>&1).ToString().Trim() } catch {}
}
$r = Test-Item "Codex CLI" ($codexVer -ne "") "$codexVer ($codexPath)" "npm install -g @openai/codex"
$report += $r; if ($r.Pass) { $totalPass++ } else { $totalFail++ }

# Python
$pyVer = ""
try { $pyVer = (python --version 2>&1).ToString().Trim() } catch {}
$r = Test-Item "Python" ($pyVer -ne "") $pyVer "Install Python 3.10+"
$report += $r; if ($r.Pass) { $totalPass++ } else { $totalFail++ }

# Node.js
$nodeVer = ""
try { $nodeVer = (node --version 2>&1).ToString().Trim() } catch {}
$r = Test-Item "Node.js" ($nodeVer -ne "") $nodeVer "Install Node.js 18+"
$report += $r; if ($r.Pass) { $totalPass++ } else { $totalFail++ }

# LaTeX
$latexOk = $false
try { $null = Get-Command pdflatex -ErrorAction Stop; $latexOk = $true } catch {}
$r = Test-Item "LaTeX (pdflatex)" $latexOk $(if($latexOk){"Available"}else{"Optional: needed for /paper-compile"}) "scoop install miktex"
$report += $r; if ($r.Pass) { $totalPass++ } else { $totalFail++ }

# Git
$gitVer = ""
try { $gitVer = (git --version 2>&1).ToString().Trim() } catch {}
$r = Test-Item "Git" ($gitVer -ne "") $gitVer
$report += $r; if ($r.Pass) { $totalPass++ } else { $totalFail++ }

# ══════════════════════════════════════════════════════════════════════
Write-Banner "2. ARIS Skills"
# ══════════════════════════════════════════════════════════════════════

$skillDir = "$env:USERPROFILE\.claude\skills"
$codexSkillDir = "$env:USERPROFILE\.codex\skills"

$claudeSkills = @()
$codexSkills  = @()
if (Test-Path $skillDir)      { $claudeSkills = Get-ChildItem $skillDir -Directory -ErrorAction SilentlyContinue }
if (Test-Path $codexSkillDir) { $codexSkills  = Get-ChildItem $codexSkillDir -Directory -ErrorAction SilentlyContinue }

$r = Test-Item "Claude Skills directory" ($claudeSkills.Count -gt 0) "$($claudeSkills.Count) skills in $skillDir"
$report += $r; if ($r.Pass) { $totalPass++ } else { $totalFail++ }

$r = Test-Item "Codex Skills directory" ($codexSkills.Count -gt 0) "$($codexSkills.Count) skills in $codexSkillDir"
$report += $r; if ($r.Pass) { $totalPass++ } else { $totalFail++ }

$criticalSkills = @("arxiv","research-lit","research-review","idea-creator","novelty-check",
                     "idea-discovery","auto-review-loop","paper-writing","paper-plan",
                     "paper-write","paper-compile","research-pipeline","run-experiment")

$missingSkills = @()
foreach ($s in $criticalSkills) {
    $found = (Test-Path (Join-Path $skillDir $s)) -or (Test-Path (Join-Path $codexSkillDir $s))
    if (-not $found) { $missingSkills += $s }
}

if ($missingSkills.Count -eq 0) {
    $r = Test-Item "Critical ARIS skills" $true "All $($criticalSkills.Count) present"
} else {
    $r = Test-Item "Critical ARIS skills" $false "Missing: $($missingSkills -join ', ')"
}
$report += $r; if ($r.Pass) { $totalPass++ } else { $totalFail++ }

# ══════════════════════════════════════════════════════════════════════
Write-Banner "3. MCP Configuration"
# ══════════════════════════════════════════════════════════════════════

$mcpFile = "$env:USERPROFILE\.claude\settings.json"
$mcpOk = $false
$mcpDetail = ""
if (Test-Path $mcpFile) {
    try {
        $settings = Get-Content $mcpFile -Raw | ConvertFrom-Json
        if ($settings.mcpServers -and $settings.mcpServers.codex) {
            $mcpOk = $true
            $mcpDetail = "codex server configured"
        } else {
            $mcpDetail = "codex server NOT found in settings"
        }
    } catch {
        $mcpDetail = "Failed to parse settings.json"
    }
} else {
    $mcpDetail = "settings.json not found"
}
$r = Test-Item "Codex MCP server" $mcpOk $mcpDetail "claude mcp add codex -- $codexPath mcp-server"
$report += $r; if ($r.Pass) { $totalPass++ } else { $totalFail++ }

# Codex config (model setting)
$codexCfg = "$env:USERPROFILE\.codex\config.toml"
$modelOk = $false
if (Test-Path $codexCfg) {
    $cfgContent = Get-Content $codexCfg -Raw -ErrorAction SilentlyContinue
    if ($cfgContent -match 'model\s*=\s*"gpt-5') {
        $modelOk = $true
    }
}
$r = Test-Item "Codex model config (gpt-5.x)" $modelOk $(if($modelOk){"GPT-5.x configured"}else{"Check $codexCfg"})
$report += $r; if ($r.Pass) { $totalPass++ } else { $totalFail++ }

# ══════════════════════════════════════════════════════════════════════
Write-Banner "4. Network Connectivity"
# ══════════════════════════════════════════════════════════════════════

# Local proxy
$proxyOk = $false
try {
    $tcp = Test-NetConnection -ComputerName 127.0.0.1 -Port 7897 -ErrorAction Stop -WarningAction SilentlyContinue
    $proxyOk = $tcp.TcpTestSucceeded
} catch {}
$r = Test-Item "Local proxy (127.0.0.1:7897)" $proxyOk "" "Start your proxy software"
$report += $r; if ($r.Pass) { $totalPass++ } else { $totalFail++ }

# arXiv API
$arxivOk = $false
try {
    $testUrl = "http://export.arxiv.org/api/query?search_query=test&max_results=1"
    $proxy = New-Object System.Net.WebProxy("http://127.0.0.1:7897")
    $wc = New-Object System.Net.WebClient
    $wc.Proxy = $proxy
    $resp = $wc.DownloadString($testUrl)
    $arxivOk = $resp.Length -gt 100
} catch {
    try {
        $wc2 = New-Object System.Net.WebClient
        $resp = $wc2.DownloadString($testUrl)
        $arxivOk = $resp.Length -gt 100
    } catch {}
}
$r = Test-Item "arXiv API reachable" $arxivOk "" "Check internet & proxy"
$report += $r; if ($r.Pass) { $totalPass++ } else { $totalFail++ }

# ══════════════════════════════════════════════════════════════════════
Write-Banner "5. System Resources"
# ══════════════════════════════════════════════════════════════════════

# Disk space
$drive = (Get-Item $PSScriptRoot).PSDrive
$freeGB = [math]::Round($drive.Free / 1GB, 1)
$r = Test-Item "Disk space ($($drive.Name):)" ($freeGB -ge 2) "$freeGB GB free" "Need at least 2 GB"
$report += $r; if ($r.Pass) { $totalPass++ } else { $totalFail++ }

# RAM
$totalRAM = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1)
$r = Test-Item "Total RAM" ($totalRAM -ge 8) "$totalRAM GB"
$report += $r; if ($r.Pass) { $totalPass++ } else { $totalFail++ }

# ══════════════════════════════════════════════════════════════════════
Write-Banner "6. Diagnosis Summary"
# ══════════════════════════════════════════════════════════════════════

$total = $totalPass + $totalFail
Write-Host "  Results: $totalPass/$total passed" -ForegroundColor $(if($totalFail -eq 0){"Green"}else{"Yellow"})
Write-Host ""

if ($totalFail -eq 0) {
    Write-Host "  All checks passed! ARIS is ready to use." -ForegroundColor Green
} else {
    Write-Host "  $totalFail check(s) failed. Review the [FAIL] items above." -ForegroundColor Yellow
    Write-Host "  Some features may not work correctly." -ForegroundColor Yellow
}

Write-Host ""

# ── 保存诊断报告 ──
$reportFile = Join-Path $PSScriptRoot "health_report.txt"
$lines = @(
    "ARIS Health Check Report"
    "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    "OS: $([System.Environment]::OSVersion.VersionString)"
    ""
    "Results: $totalPass/$total passed"
    ""
)
foreach ($r in $report) {
    $status = if ($r.Pass) { "PASS" } else { "FAIL" }
    $lines += "  [$status] $($r.Label) — $($r.Detail)"
}
$lines | Out-File $reportFile -Encoding UTF8

Write-Host "  Report saved to: $reportFile" -ForegroundColor DarkGray
Write-Host ""
