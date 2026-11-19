@echo off
setlocal
cd /d "%~dp0.."

set "BLOG_QUARTO=%LOCALAPPDATA%\Programs\Quarto\bin\quarto.exe"
if not exist "%BLOG_QUARTO%" (
    where quarto >nul 2>nul
    if errorlevel 1 (
        echo Quarto was not found. Install Quarto or add it to PATH.
        pause
        exit /b 1
    )
    set "BLOG_QUARTO=quarto"
)

echo Keep this window open while editing. Press Ctrl+C to stop the preview.
call "%BLOG_QUARTO%" preview --profile preview --host 127.0.0.1 --timeout 0 %*
if errorlevel 1 pause
