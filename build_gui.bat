@echo off
echo ========================================
echo Kirby x Miles ESL - GUI Builder
echo ========================================
echo.
echo Installing auto-py-to-exe...
pip install auto-py-to-exe --quiet
echo.
echo Launching GUI builder...
echo.
echo In the GUI:
echo   1. Script Location: Select game.py
echo   2. Onefile: Select "One File" (IMPORTANT for portability!)
echo   3. Console Window: Select "Window Based (hide console)"
echo   4. Additional Files: Add these folders:
echo      - assets (add as folder)
echo   5. Click "Convert .py to .exe"
echo.
python -m auto_py_to_exe
pause
