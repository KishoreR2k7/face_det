# 🎓 Face Recognition Attendance System

> AI-powered automated attendance tracking with real-time face recognition

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A complete face recognition system for automated attendance tracking using deep learning (InsightFace, DeepFace), FAISS vector search, and Flask API backend with React admin interface.

---

## ✨ Key Features

✅ **Real-time Face Recognition** - Instant face detection and identification  
✅ **Web Admin Panel** - Upload student photos, manage dataset, train models  
✅ **Auto-Training** - Automatic embedding generation and FAISS index creation  
✅ **Multi-Camera Support** - Track attendance across multiple locations  
✅ **GPU Acceleration** - CUDA support for faster processing  
✅ **REST API Backend** - Flask API for all operations  
✅ **Attendance Logs** - Automatic CSV export with timestamps  

---

## 🚀 Quick Start (3 Steps)

### 1️⃣ Setup Environment
```bash
# Run the automated setup script
setup_conda_env.bat

# Or manually:
conda create -n face_recognition python=3.10 -y
conda activate face_recognition
pip install -r requirements.txt
```

### 2️⃣ Start Services
```bash
# Terminal 1 - Backend
conda activate face_recognition
python src/api_backend.py

# Terminal 2 - Frontend
cd admin-frontend
npm install && npm run dev
```

### 3️⃣ Add Students & Train
1. Open http://localhost:5173
2. Login (admin / admin)
3. Go to "Training Center"
4. Add student with 5-10 photos
5. System auto-trains the model! 🎉

**📖 Detailed Guide**: See [QUICK_START.md](QUICK_START.md)

---

## 📁 Project Structure

```
face_reg_copy/
├── src/                         # Core Python modules
│   ├── api_backend.py          # Flask REST API
│   ├── recognize_faces.py      # Face recognition engine
│   ├── precompute_embeddings.py # Training & embedding generation
│   ├── detector_scrfd.py       # Face detection (SCRFD/YOLO)
│   └── utils.py                # Helper functions
├── admin-frontend/              # React admin UI
│   └── src/
│       ├── pages/
│       │   └── admin/
│       │       └── TrainingCenter.jsx  # Dataset upload & training
│       └── ...
├── dataset/                     # Training images
│   ├── student_name_1/
│   │   ├── photo1.jpg
│   │   └── photo2.jpg
│   └── student_name_2/
├── embeddings/                  # FAISS index storage
│   ├── faiss_index.bin         # Vector search index
│   └── labels.pkl              # Person labels
├── models/                      # ML models
│   └── yolov8n-face.pt         # Face detection model
├── config.yaml                  # Configuration
├── requirements.txt             # Dependencies
├── setup_conda_env.bat         # Conda setup script
├── test_system.py              # System test suite
└── QUICK_START.md              # Setup guide
```

---

## � Requirements

### Software
- **Python**: 3.10+
- **Node.js**: 18+ (for frontend)
- **Conda**: Anaconda/Miniconda
- **CUDA**: 12.6 (optional, for GPU)

### Python Packages
```
torch, torchvision           # PyTorch (GPU/CPU)
insightface                  # ArcFace embeddings
deepface                     # Face recognition
faiss-cpu / faiss-gpu        # Vector search
opencv-python                # Image processing
flask, flask-cors            # Backend API
```

**Install All**: `pip install -r requirements.txt`

---## 🎯 How It Works

### 1. Training Pipeline
```
Upload Photos → Detect Faces → Extract Embeddings → Build FAISS Index → Save Model
```

**What happens:**
- Admin uploads student photos via web interface
- System detects faces using SCRFD/YOLO
- InsightFace extracts 512-dim embeddings (face features)
- FAISS builds vector search index
- Model saved for instant recognition

### 2. Recognition Pipeline
```
Capture Frame → Detect Faces → Extract Embeddings → Search FAISS → Match Person
```

**What happens:**
- Camera captures live video frames
- Face detector finds all faces in frame
- System extracts embeddings for each face
- FAISS searches for nearest match (cosine similarity)
- If similarity > threshold: Person recognized ✅
- Attendance logged to database & CSV

---

## 📊 Configuration

### `config.yaml`
```yaml
DEVICE: cuda  # or 'cpu'

RECOGNITION:
  EMBEDDING_MODEL: VGG-Face
  DISTANCE_METRIC: cosine
  VERIFICATION_THRESHOLD: 0.4  # Lower = stricter matching

PATHS:
  DATASET_DIR: dataset
  EMBEDDINGS_DIR: embeddings
  FAISS_INDEX_FILE: faiss_index.bin

CAMERA_SOURCES:
  - name: Webcam
    source: 0
```

**Key Settings:**
- `VERIFICATION_THRESHOLD`: 0.2-0.5 (adjust based on accuracy needs)
- `DEVICE`: Use `cuda` for GPU, `cpu` for CPU
- `EMBEDDING_MODEL`: VGG-Face, Facenet, ArcFace (InsightFace)

---

## 🧪 Testing

Run the complete test suite:
```bash
conda activate face_recognition
python test_system.py
```

This checks:
- ✅ Dependencies installed
- ✅ CUDA availability
- ✅ Config file valid
- ✅ Dataset structure correct
- ✅ Embeddings generated
- ✅ Face detection working
- ✅ Recognition pipeline functional
- ✅ Database initialized
- ✅ API backend ready

---

## 🎥 Running Face Recognition

### Method 1: Video File/Webcam
```bash
conda activate face_recognition
python run_video.py
```

### Method 2: Camera Service (Multi-camera)
```bash
python camera-service/start_camera_service.py
```

### Method 3: Via Admin Panel
1. Open admin panel
2. Go to "Live Recognition"
3. Select camera
4. View real-time results

---

## 📈 Performance Tips

1. **Use GPU**: 10x faster than CPU
   ```bash
   # Check CUDA
   python -c "import torch; print(torch.cuda.is_available())"
   ```

2. **Good Training Data**:
   - 5-10 clear photos per person
   - Different angles and expressions
   - Good lighting
   - Face clearly visible

3. **Adjust Threshold**:
   - Too many false positives? **Increase** threshold (0.4 → 0.5)
   - Missing recognitions? **Decrease** threshold (0.4 → 0.3)

4. **Multiple Cameras**:
   - Add via admin panel
   - System handles deduplication automatically

---

## 🔧 Troubleshooting

### ❌ Face Not Recognized?

**Check 1**: Is the person in the dataset?
```bash
dir dataset
```

**Check 2**: Are embeddings generated?
```bash
dir embeddings
# Should see: faiss_index.bin, labels.pkl
```

**Check 3**: Retrain the model
```bash
python src/precompute_embeddings.py
```

**Check 4**: Lower threshold in `config.yaml`
```yaml
VERIFICATION_THRESHOLD: 0.3  # Try 0.2-0.4
```

---

### ❌ Import Errors?

**Missing packages:**
```bash
conda activate face_recognition
pip install -r requirements.txt
```

**CUDA errors:**
```bash
# Use CPU mode
# Edit config.yaml: DEVICE: cpu
```

---

### ❌ Frontend Not Loading?

**Backend not running:**
```bash
# Terminal 1
python src/api_backend.py
```

**Frontend not installed:**
```bash
cd admin-frontend
npm install
npm run dev
```

**CORS errors:**
- Check `src/api_backend.py` has `CORS(app)` enabled
- Verify frontend uses `http://localhost:5000` for API

---

## 📚 API Endpoints

### Authentication
- `POST /auth/login` - Login and get JWT token

### Students
- `GET /students` - List all students
- `POST /students` - Add new student

### Dataset & Training
- `POST /dataset/upload/<roll_no>` - Upload images/videos
- `POST /dataset/train` - Trigger manual training
- `DELETE /dataset/<person_name>` - Delete person data

### Cameras
- `GET /cameras` - List cameras
- `POST /cameras` - Add camera

### Attendance
- `GET /attendance` - Get attendance records
- `POST /attendance/mark` - Manual attendance mark
- `DELETE /attendance/<id>` - Delete record

---

## 📝 Attendance Logs

### Database
SQLite database: `attendance_system.db`

Tables:
- `students`: Student information
- `attendance`: Attendance records
- `cameras`: Camera configurations
- `users`: Admin users
- `dataset`: Uploaded images metadata

### CSV Export
Location: `attendance/attendance_log.csv`

Format:
```csv
Name,Camera,Timestamp,Date,Time
John Doe,Webcam,2025-10-27 14:30:15,2025-10-27,14:30:15
Jane Smith,Camera 1,2025-10-27 14:31:22,2025-10-27,14:31:22
```

---

## 🧹 Cleanup (Optional)

Remove duplicate/unnecessary files:
```bash
# See detailed list
type CLEANUP_GUIDE.md

# Or manually remove
del test_*.py
del *_COMPLETE.md
rmdir /S /Q frontend ui
```

**Recommended**: Keep only essential files (see CLEANUP_GUIDE.md)

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

- **InsightFace**: Face detection and recognition models
- **FAISS**: Efficient similarity search
- **DeepFace**: Face recognition framework
- **PyTorch**: Deep learning framework
- **Flask**: Backend API framework
- **React**: Frontend UI library

---

## 📞 Support

**Issues?** Open a GitHub issue  
**Questions?** Check [QUICK_START.md](QUICK_START.md)  
**Documentation**: See individual `.md` files

---

## 🎓 Project Status

✅ Core recognition working  
✅ Admin panel functional  
✅ Training pipeline automated  
✅ Multi-camera support  
✅ Attendance logging  
⏳ Mobile app (planned)  
⏳ Advanced analytics (planned)  

---

**Built with ❤️ for automated attendance tracking**

   - Verify image quality and face visibility

3. **Slow performance**
   - Reduce frame resolution in config
   - Ensure FAISS index is properly built
   - Check system resources

4. **Module import errors**
   - Verify all dependencies are installed
   - Check Python version compatibility
   - Reinstall requirements: `pip install -r requirements.txt --force-reinstall`

## 🔒 Security & Privacy

- Face images and embeddings are stored locally
- No data is transmitted to external servers
- Attendance logs contain only names and timestamps
- Consider encryption for sensitive deployments
- Ensure compliance with local privacy regulations

## 🚀 Future Enhancements

- [ ] Support for multiple camera sources
- [ ] Cloud storage integration for attendance logs
- [ ] Mobile app interface
- [ ] Advanced analytics and reporting
- [ ] Integration with existing attendance systems
- [ ] GPU acceleration for faster processing
- [ ] Anti-spoofing measures (liveness detection)
- [ ] User management dashboard

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FAISS](https://github.com/facebookresearch/faiss) - Facebook AI Similarity Search for efficient vector matching
- [OpenCV](https://opencv.org/) - Computer vision library for image and video processing
- [Streamlit](https://streamlit.io/) - Framework for building interactive web applications
- Deep learning community for face recognition models

## 📞 Contact & Support

For questions, issues, or suggestions:
- Create an issue in this repository
- Check existing issues for solutions
- Review documentation and troubleshooting guide

---

**Note**: This system is designed for educational purposes and small to medium-scale deployments. For production environments with high traffic or strict security requirements, consider additional hardening, scaling infrastructure, and compliance measures.
# face_reg
