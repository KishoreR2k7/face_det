@echo off
echo ========================================
echo Running System Test Suite
echo ========================================
echo.

REM Check if conda environment exists
call conda activate face_recognition 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Conda environment 'face_recognition' not found!
    echo Please run: setup_conda_env.bat first
    pause
    exit /b 1
)

echo Conda environment activated.
echo.

REM Run the test
python test_system.py

pause
