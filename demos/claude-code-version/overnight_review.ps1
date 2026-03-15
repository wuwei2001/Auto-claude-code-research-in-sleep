# ARIS 过夜审稿脚本
#
# 用法: 睡觉前运行此脚本
# .\overnight_review.ps1 "你的论文主题"
#
# 此脚本会：
# 1. 检查环境
# 2. 确认电源设置
# 3. 启动 Claude Code 并运行 auto-review-loop

param(
    [Parameter(Mandatory=$true)]
    [string]$Topic
)

Write-Host ""
Write-Host "============================================" -ForegroundColor Magenta
Write-Host "  ARIS Overnight Review Setup" -ForegroundColor Magenta
Write-Host "============================================" -ForegroundColor Magenta
Write-Host ""
Write-Host "  Topic: $Topic" -ForegroundColor White
Write-Host ""

# 检查电源设置
Write-Host "[Check] Power settings..." -ForegroundColor Yellow
Write-Host "  IMPORTANT: Make sure your computer will NOT go to sleep!" -ForegroundColor Red
Write-Host "  Settings > System > Power > Screen/Sleep > Never" -ForegroundColor Yellow
Write-Host ""

# 检查代理
Write-Host "[Check] Network proxy..." -ForegroundColor Yellow
try {
    $null = Test-NetConnection -ComputerName 127.0.0.1 -Port 7897 -ErrorAction Stop -WarningAction SilentlyContinue
    Write-Host "  Proxy at 127.0.0.1:7897 is reachable" -ForegroundColor Green
} catch {
    Write-Host "  WARNING: Proxy at 127.0.0.1:7897 may not be running!" -ForegroundColor Red
    Write-Host "  Make sure your proxy is started before proceeding." -ForegroundColor Yellow
}
Write-Host ""

# 显示预计时间
Write-Host "[Info] Expected duration: 2-8 hours" -ForegroundColor Cyan
Write-Host "[Info] Max rounds: 4" -ForegroundColor Cyan
Write-Host "[Info] Stop condition: score >= 6/10" -ForegroundColor Cyan
Write-Host "[Info] State saved to: REVIEW_STATE.json (auto-resume)" -ForegroundColor Cyan
Write-Host ""

Write-Host "============================================" -ForegroundColor Magenta
Write-Host "  Starting Claude Code with auto-review-loop..." -ForegroundColor Magenta
Write-Host "  You can go to sleep now!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Magenta
Write-Host ""

# 启动 Claude Code 并直接发送 auto-review-loop 命令
claude -p "/auto-review-loop `"$Topic`""
