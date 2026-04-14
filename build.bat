@echo off
echo ========================================
echo Kirby x Miles ESL - Automated Build
echo ========================================
echo.

echo [1/3] Installing PyInstaller...
pip install pyinstaller --quiet
if errorlevel 1 (
    echo ERROR: pip failed. Make sure Python is installed and in your PATH.
    pause
    exit /b 1
)

echo [2/3] Building KirbyMilesESL.exe ...
echo       This may take 30-60 seconds.
echo.

pyinstaller ^
    --onefile ^
    --windowed ^
    --name "KirbyMilesESL" ^
    --collect-all pygame ^
    --add-data "assets;assets" ^
    game.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed. See output above for details.
    pause
    exit /b 1
)

echo.
echo [3/3] Done!
echo.
echo Your executable is at:
echo   dist\KirbyMilesESL.exe
echo.
echo You can copy  dist\KirbyMilesESL.exe  to any Windows PC and run it directly.
echo No Python or pygame installation needed on the target machine.
echo.
pause
