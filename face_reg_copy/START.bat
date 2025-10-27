@echo off
REM ========================================
REM Face Recognition System - Complete Startup
REM ========================================

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   FACE RECOGNITION ATTENDANCE SYSTEM - STARTUP WIZARD      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check conda
where conda >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [X] ERROR: Conda not found!
    echo     Please install Anaconda/Miniconda first.
    pause
    exit /b 1
)
echo [√] Conda found

REM Check if environment exists
call conda activate face_recognition 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] Conda environment 'face_recognition' not found
    echo     Setting up environment now...
    echo.
    call setup_conda_env.bat
    if %ERRORLEVEL% NEQ 0 (
        echo [X] Setup failed!
        pause
        exit /b 1
    )
)

echo [√] Environment ready
echo.

REM Ask user what to do
:menu
echo ========================================
echo What would you like to do?
echo ========================================
echo.
echo 1. Setup conda environment (first time)
echo 2. Test the system
echo 3. Start backend API (Flask)
echo 4. Start admin frontend (React)
echo 5. Run face recognition (Video)
echo 6. Train/Retrain model
echo 7. Exit
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto test
if "%choice%"=="3" goto backend
if "%choice%"=="4" goto frontend
if "%choice%"=="5" goto video
if "%choice%"=="6" goto train
if "%choice%"=="7" goto end
goto menu

:setup
echo.
echo Starting setup...
call setup_conda_env.bat
pause
goto menu

:test
echo.
echo Running system tests...
call conda activate face_recognition
python test_system.py
pause
goto menu

:backend
echo.
echo ========================================
echo Starting Flask Backend API
echo ========================================
echo Server will run on: http://localhost:5000
echo Press Ctrl+C to stop
echo ========================================
echo.
call conda activate face_recognition
python src/api_backend.py
pause
goto menu

:frontend
echo.
echo ========================================
echo Starting React Admin Frontend
echo ========================================
echo Frontend will run on: http://localhost:5173
echo Press Ctrl+C to stop
echo ========================================
echo.
cd admin-frontend
if not exist "node_modules\" (
    echo Installing npm packages...
    call npm install
)
call npm run dev
cd ..
pause
goto menu

:video
echo.
echo ========================================
echo Starting Face Recognition Video
echo ========================================
echo Press 'q' to quit video window
echo ========================================
echo.
call conda activate face_recognition
python run_video.py
pause
goto menu

:train
echo.
echo ========================================
echo Training Face Recognition Model
echo ========================================
echo This will process all images in dataset/
echo ========================================
echo.
call conda activate face_recognition
python src/precompute_embeddings.py
echo.
echo ========================================
echo Training complete!
echo ========================================
pause
goto menu

:end
echo.
echo Thank you for using Face Recognition System!
echo.
exit /b 0
