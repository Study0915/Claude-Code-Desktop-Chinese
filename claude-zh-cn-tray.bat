@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
if not exist "%~dp0python\python.exe" (
    echo 未找到内置 Python: "%~dp0python\python.exe"
    echo 请改用 claude-zh-cn.bat，或确认发布包完整。
    pause
    exit /b 1
)

set "TRAY_PY=%~dp0python\pythonw.exe"
if not exist "%TRAY_PY%" set "TRAY_PY=%~dp0python\python.exe"

"%~dp0python\python.exe" -c "import pystray; import PIL" >nul 2>&1
if errorlevel 1 (
    echo 系统托盘监视器缺少 pystray / Pillow 依赖。
    echo 仍可通过 claude-zh-cn.bat 安装、卸载和查看状态。
    echo.
    "%~dp0python\python.exe" "%~dp0tray\app.py"
    echo.
    pause
    exit /b 1
)

start "" "%TRAY_PY%" "%~dp0tray\app.py"
