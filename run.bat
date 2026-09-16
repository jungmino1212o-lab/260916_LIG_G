@echo off
chcp 65001 > nul
title LIG DNA TODO APP Server

echo ================================================================
echo       🧬 LIG DNA 스마트 워크 & TODO 매니저 실행기 🧬
echo ================================================================
echo.

:: 파이썬 실행 파일 위치 감지
set "PY_CMD=python"
python --version >nul 2>&1
if errorlevel 1 (
    if exist "%LOCALAPPDATA%\Programs\Python311\python.exe" (
        set "PY_CMD=%LOCALAPPDATA%\Programs\Python311\python.exe"
    ) else (
        echo [!] Python 실행 환경을 찾을 수 없습니다.
        pause
        exit /b 1
    )
)

echo [*] Python 실행 파일: %PY_CMD%
echo [*] 애플리케이션 라이브러리 확인 중...
%PY_CMD% -m pip install -r requirements.txt >nul 2>&1

echo [*] 웹 브라우저 자동 오픈 중... (http://127.0.0.1:5000)
start "" "http://127.0.0.1:5000"

echo [*] Flask 서버를 시작합니다. (종료하려면 Ctrl+C)
echo.
%PY_CMD% app.py

pause
