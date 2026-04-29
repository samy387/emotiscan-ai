@echo off
title EmotiScan AI - Server Launcher
color 0A

echo ============================================
echo      EmotiScan AI - Backend Server
echo ============================================
echo.

REM Check if API key is already set
if "%ANTHROPIC_API_KEY%"=="" (
    echo [!] ANTHROPIC_API_KEY is not set.
    echo.
    set /p ANTHROPIC_API_KEY="Enter your Anthropic API key (sk-ant-...): "
    echo.
)

echo [*] Installing / verifying dependencies...
pip install -r requirements.txt -q

echo.
echo [OK] API Key loaded.
echo [*]  Starting server at http://localhost:5000
echo [*]  Open app.html in your browser to use the app.
echo.
echo Press Ctrl+C to stop the server.
echo ============================================
echo.

python server.py

pause
