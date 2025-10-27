# 🚀 Quick Start Guide - Face Recognition Attendance System

## Prerequisites
- ✅ Anaconda or Miniconda installed
- ✅ CUDA 12.6 (for GPU support, optional)
- ✅ Node.js 18+ (for frontend)

---

## 📦 Step 1: Setup Conda Environment

### Windows (PowerShell/CMD):
```bash
# Run the automated setup script
setup_conda_env.bat
```

### Manual Setup (if script fails):
```bash
# Create environment
conda create -n face_recognition python=3.10 -y
conda activate face_recognition

# Install PyTorch with CUDA
conda install pytorch torchvision torchaudio pytorch-cuda=12.6 -c pytorch -c nvidia -y

# Install dependencies
pip install -r requirements.txt
```

---

## ⚙️ Step 2: Configure the System

### Create `.env` file:
```bash
# Copy the template
copy env.template .env

# Edit .env and add your settings
SECRET_KEY=your_secret_key_here
EMAIL1=admin@example.com
PWD1=admin123
```

### Verify `config.yaml`:
```yaml
DEVICE: cuda  # or 'cpu' if no GPU
RECOGNITION:
  VERIFICATION_THRESHOLD: 0.4  # Lower = more strict
```

---

## 🎯 Step 3: Run the System

### Terminal 1 - Start Backend:
```bash
conda activate face_recognition
cd "C:/Users/kishore/New folder/face_reg_copy"
python src/api_backend.py
```

### Terminal 2 - Start Admin Frontend:
```bash
cd admin-frontend
npm install
npm run dev
```

### Terminal 3 - Start User Frontend (Optional):
```bash
cd user-frontend
npm install
npm run dev
```

---

## 📸 Step 4: Add Students & Train Model

1. **Open Admin Panel**: http://localhost:5173
2. **Login**: 
   - Email: `admin`
   - Password: `admin`
3. **Go to "Training Center"**
4. **Add Student**:
   - Enter Name & Roll Number
   - Upload 5-10 clear photos/videos
   - Click "Add Student & Train"
5. **Wait for Training**: The system will automatically:
   - Extract faces from images/videos
   - Generate embeddings (face features)
   - Build FAISS index for fast search
   - Save the model

---

## 🎥 Step 5: Start Face Recognition

### Run Video Recognition:
```bash
conda activate face_recognition
python run_video.py
```

### Or Use Camera Service:
```bash
python camera-service/start_camera_service.py
```

---

## 🔧 Troubleshooting

### ❌ Face Not Recognized?
```bash
# 1. Check if embeddings exist
dir embeddings

# 2. Retrain the model
python src/precompute_embeddings.py

# 3. Lower the threshold in config.yaml
VERIFICATION_THRESHOLD: 0.3  # Try 0.2-0.4
```

### ❌ CUDA Not Available?
```bash
# Check CUDA
python -c "import torch; print(torch.cuda.is_available())"

# If False, use CPU mode
# Edit config.yaml: DEVICE: cpu
```

### ❌ Backend API Errors?
```bash
# Check if database exists
dir attendance_system.db

# Reinitialize database
python -c "from src.api_backend import init_db; init_db()"
```

### ❌ Frontend Can't Connect?
- Ensure backend is running on `http://localhost:5000`
- Check CORS settings in `src/api_backend.py`
- Verify API endpoints in frontend

---

## 📊 How It Works

### Training Flow:
```
Upload Images → Detect Faces → Extract Embeddings → Save to FAISS Index
```

### Recognition Flow:
```
Capture Frame → Detect Faces → Extract Embeddings → Search FAISS Index → Match Person
```

### Key Files:
- **`src/api_backend.py`**: Flask API server
- **`src/recognize_faces.py`**: Face recognition logic
- **`src/precompute_embeddings.py`**: Training script
- **`config.yaml`**: System configuration
- **`dataset/`**: Training images (organized by name/roll_no)
- **`embeddings/`**: FAISS index and labels

---

## 🎓 Add More Students

### Method 1: Admin Panel (Recommended)
1. Go to "Training Center"
2. Fill form and upload images
3. System auto-trains

### Method 2: Manual Dataset Upload
```bash
# Create folder with student name/roll_no
mkdir dataset/STUDENT_NAME

# Add 5-10 images
copy image1.jpg dataset/STUDENT_NAME/
copy image2.jpg dataset/STUDENT_NAME/

# Run training
python src/precompute_embeddings.py
```

---

## 📈 Performance Tips

1. **Use GPU**: 10x faster training & recognition
2. **Good Quality Images**: Well-lit, front-facing, clear
3. **Multiple Angles**: Different poses for better accuracy
4. **Optimal Threshold**: Test with 0.3-0.5 for best results
5. **Regular Retraining**: After adding new students

---

## 🆘 Need Help?

- Check logs in terminal for errors
- Verify all dependencies installed: `pip list`
- Ensure correct Python version: `python --version` (should be 3.10)
- Review `DEPLOYMENT.md` for detailed setup

---

## ✅ Success Checklist

- [ ] Conda environment created and activated
- [ ] Dependencies installed without errors
- [ ] Backend API running on port 5000
- [ ] Frontend running on port 5173
- [ ] At least 1 student added with images
- [ ] Model trained (embeddings folder exists)
- [ ] Face recognition working in video

**System Ready! 🎉**
