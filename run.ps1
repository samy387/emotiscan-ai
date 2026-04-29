# =============================================
#   EmotiScan AI - All-in-One Launcher
#   Run this script to start the app
# =============================================

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "        EmotiScan AI - Launcher" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# --- Step 1: Check/Set API Key ---
if (-not $env:ANTHROPIC_API_KEY) {
    Write-Host "[!] ANTHROPIC_API_KEY is not set." -ForegroundColor Yellow
    Write-Host ""
    $key = Read-Host "    Enter your Anthropic API key (sk-ant-...)"
    if (-not $key) {
        Write-Host "[ERROR] No key entered. Exiting." -ForegroundColor Red
        pause
        exit 1
    }
    # Save permanently to user environment
    [System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", $key, "User")
    $env:ANTHROPIC_API_KEY = $key
    Write-Host "[OK] API key saved permanently." -ForegroundColor Green
} else {
    $masked = $env:ANTHROPIC_API_KEY.Substring(0, [Math]::Min(12, $env:ANTHROPIC_API_KEY.Length)) + "..."
    Write-Host "[OK] API key found: $masked" -ForegroundColor Green
}

Write-Host ""

# --- Step 2: Install dependencies ---
Write-Host "[*] Checking Python packages..." -ForegroundColor Cyan
pip install -r "$projectDir\requirements.txt" -q
Write-Host "[OK] Packages ready." -ForegroundColor Green
Write-Host ""

# --- Step 3: Open app.html in browser ---
Write-Host "[*] Opening app.html in browser..." -ForegroundColor Cyan
Start-Process "$projectDir\app.html"
Start-Sleep -Seconds 1

# --- Step 4: Start Flask server ---
Write-Host "[START] Starting Flask server at http://localhost:5000" -ForegroundColor Cyan
Write-Host "[INFO]  Press Ctrl+C to stop the server." -ForegroundColor Gray
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Set-Location $projectDir
python server.py
