@echo off
REM Face Recognition System - Conda Environment Setup Script
REM This script creates and configures a conda environment for the project

echo ========================================
echo Face Recognition System Setup
echo ========================================
echo.

REM Check if conda is available
where conda >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Conda not found! Please install Anaconda or Miniconda first.
    echo Download from: https://www.anaconda.com/download
    pause
    exit /b 1
)

echo Step 1: Creating conda environment 'face_recognition'...
call conda create -n face_recognition python=3.10 -y

echo.
echo Step 2: Activating environment...
call conda activate face_recognition

echo.
echo Step 3: Installing PyTorch with CUDA 12.6 support...
call conda install pytorch torchvision torchaudio pytorch-cuda=12.6 -c pytorch -c nvidia -y

echo.
echo Step 4: Installing core dependencies...
pip install insightface==0.7.3
pip install onnxruntime>=1.20.0
pip install deepface==0.0.93
pip install faiss-cpu>=1.9.0
pip install opencv-python==4.10.0.84
pip install Pillow==10.4.0
pip install numpy==1.26.4
pip install pandas==2.2.3
pip install tqdm==4.66.5
pip install matplotlib==3.9.2
pip install pyyaml==6.0.2

echo.
echo Step 5: Installing Flask backend dependencies...
pip install Flask==2.2.5
pip install flask-cors==3.0.10
pip install PyJWT==2.8.0
pip install python-dotenv==1.0.0

echo.
echo Step 6: Installing additional tools...
pip install ultralytics

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To use the environment:
echo   1. Run: conda activate face_recognition
echo   2. Start backend: python src/api_backend.py
echo   3. Start frontend: cd admin-frontend ^&^& npm install ^&^& npm run dev
echo.
echo For GPU support, verify CUDA installation:
echo   python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}')"
echo.
pause
