@echo off
title Save Anthropic API Key - Permanent
color 0B

echo ============================================
echo   Save ANTHROPIC_API_KEY Permanently
echo   (User-level environment variable)
echo ============================================
echo.
echo This will save your key so you NEVER need
echo to enter it again on this computer.
echo.

set /p KEY="Paste your Anthropic API key (sk-ant-...): "

if "%KEY%"=="" (
    echo [ERROR] No key entered. Exiting.
    pause
    exit /b 1
)

setx ANTHROPIC_API_KEY "%KEY%"

echo.
echo [OK] Key saved permanently!
echo [*]  Close this window and run start_server.bat
echo ============================================
pause
