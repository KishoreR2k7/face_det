"""
Complete System Test - Face Recognition Attendance
Tests the entire pipeline from dataset upload to recognition
"""

import os
import sys
import cv2
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all required packages are installed"""
    print("\n" + "="*60)
    print("TEST 1: Checking Dependencies")
    print("="*60)
    
    packages = {
        'torch': 'PyTorch',
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'faiss': 'FAISS',
        'yaml': 'PyYAML',
        'PIL': 'Pillow',
        'flask': 'Flask',
        'insightface': 'InsightFace (optional)',
        'deepface': 'DeepFace (optional)',
    }
    
    results = {}
    for pkg, name in packages.items():
        try:
            __import__(pkg)
            results[name] = '✅ Installed'
        except ImportError:
            results[name] = '❌ Missing'
    
    for name, status in results.items():
        print(f"  {name:25} {status}")
    
    return all('✅' in v for v in results.values() if 'optional' not in v)


def test_cuda():
    """Test CUDA availability"""
    print("\n" + "="*60)
    print("TEST 2: Checking CUDA Support")
    print("="*60)
    
    import torch
    
    cuda_available = torch.cuda.is_available()
    print(f"  CUDA Available: {'✅ Yes' if cuda_available else '⚠️  No (using CPU)'}")
    
    if cuda_available:
        print(f"  GPU Device: {torch.cuda.get_device_name(0)}")
        print(f"  CUDA Version: {torch.version.cuda}")
    
    return True


def test_config():
    """Test configuration file"""
    print("\n" + "="*60)
    print("TEST 3: Configuration File")
    print("="*60)
    
    from utils import load_config
    
    config = load_config()
    if not config:
        print("  ❌ Failed to load config.yaml")
        return False
    
    print("  ✅ config.yaml loaded")
    
    required_keys = ['PATHS', 'RECOGNITION', 'DEVICE']
    for key in required_keys:
        if key in config:
            print(f"  ✅ {key}: {config[key] if key == 'DEVICE' else '...'}")
        else:
            print(f"  ❌ Missing key: {key}")
            return False
    
    print(f"  Recognition Model: {config['RECOGNITION']['EMBEDDING_MODEL']}")
    print(f"  Threshold: {config['RECOGNITION']['VERIFICATION_THRESHOLD']}")
    
    return True


def test_dataset():
    """Test dataset structure"""
    print("\n" + "="*60)
    print("TEST 4: Dataset Structure")
    print("="*60)
    
    from utils import load_config
    
    config = load_config()
    dataset_dir = config['PATHS']['DATASET_DIR']
    
    if not os.path.exists(dataset_dir):
        print(f"  ❌ Dataset directory not found: {dataset_dir}")
        return False
    
    print(f"  ✅ Dataset directory: {dataset_dir}")
    
    person_folders = [f for f in os.listdir(dataset_dir) 
                     if os.path.isdir(os.path.join(dataset_dir, f))]
    
    if not person_folders:
        print("  ⚠️  No person folders found")
        print("  → Add dataset folders in format: dataset/PERSON_NAME/")
        return False
    
    print(f"  ✅ Found {len(person_folders)} persons:")
    
    total_images = 0
    for person in person_folders:
        person_path = os.path.join(dataset_dir, person)
        images = [f for f in os.listdir(person_path) 
                 if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        total_images += len(images)
        print(f"      - {person}: {len(images)} images")
    
    if total_images == 0:
        print("  ⚠️  No images found in dataset folders")
        return False
    
    print(f"  ✅ Total images: {total_images}")
    return True


def test_embeddings():
    """Test if embeddings exist"""
    print("\n" + "="*60)
    print("TEST 5: Face Embeddings & FAISS Index")
    print("="*60)
    
    from utils import load_config, load_faiss_data
    
    config = load_config()
    embeddings_dir = config['PATHS']['EMBEDDINGS_DIR']
    
    if not os.path.exists(embeddings_dir):
        print(f"  ⚠️  Embeddings directory not found: {embeddings_dir}")
        print("  → Run: python src/precompute_embeddings.py")
        return False
    
    print(f"  ✅ Embeddings directory exists")
    
    index, labels = load_faiss_data(config)
    
    if index is None or labels is None:
        print("  ❌ FAISS index or labels not loaded")
        print("  → Run: python src/precompute_embeddings.py")
        return False
    
    print(f"  ✅ FAISS index loaded")
    print(f"  ✅ Labels loaded: {len(labels)} persons")
    print(f"      Persons: {', '.join(labels)}")
    print(f"  ✅ Total embeddings: {index.ntotal}")
    
    return True


def test_face_detector():
    """Test face detection"""
    print("\n" + "="*60)
    print("TEST 6: Face Detection")
    print("="*60)
    
    from detector_scrfd import detect_faces
    
    # Create a test image (simple face-like pattern)
    test_img = np.ones((480, 640, 3), dtype=np.uint8) * 255
    
    try:
        boxes = detect_faces(test_img, device='cpu')
        print(f"  ✅ Face detector loaded successfully")
        print(f"  Detected {len(boxes)} faces in test image")
        return True
    except Exception as e:
        print(f"  ❌ Face detector failed: {e}")
        return False


def test_recognizer():
    """Test face recognition system"""
    print("\n" + "="*60)
    print("TEST 7: Face Recognition System")
    print("="*60)
    
    try:
        from recognize_faces import FaceRecognizer
        
        recognizer = FaceRecognizer()
        print("  ✅ FaceRecognizer initialized")
        print(f"  ✅ Loaded {len(recognizer.labels)} persons")
        print(f"  ✅ Model: {recognizer.embedding_model_name}")
        print(f"  ✅ Threshold: {recognizer.recognition_threshold}")
        
        # Test with blank image
        test_img = np.ones((480, 640, 3), dtype=np.uint8) * 255
        results = recognizer.recognize_face(test_img)
        
        print(f"  ✅ Recognition pipeline working")
        print(f"  Found {len(results)} results in test image")
        
        return True
    except Exception as e:
        print(f"  ❌ Face recognition failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database():
    """Test database initialization"""
    print("\n" + "="*60)
    print("TEST 8: Database")
    print("="*60)
    
    import sqlite3
    
    db_path = "attendance_system.db"
    
    if not os.path.exists(db_path):
        print(f"  ⚠️  Database not found: {db_path}")
        print("  → Run: python src/api_backend.py (it will create DB)")
        return False
    
    print(f"  ✅ Database exists: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Check tables
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in c.fetchall()]
        
        required_tables = ['students', 'cameras', 'attendance', 'users', 'dataset']
        
        for table in required_tables:
            if table in tables:
                c.execute(f"SELECT COUNT(*) FROM {table}")
                count = c.fetchone()[0]
                print(f"  ✅ Table '{table}': {count} records")
            else:
                print(f"  ❌ Missing table: {table}")
                return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Database error: {e}")
        return False


def test_api_backend():
    """Test if API backend can be imported"""
    print("\n" + "="*60)
    print("TEST 9: API Backend")
    print("="*60)
    
    try:
        sys.path.insert(0, 'src')
        import api_backend
        
        print("  ✅ API backend module loaded")
        print("  ✅ Flask app initialized")
        print("  → To start: python src/api_backend.py")
        return True
    except Exception as e:
        print(f"  ❌ API backend error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n")
    print("█" * 60)
    print("  FACE RECOGNITION SYSTEM - COMPLETE TEST SUITE")
    print("█" * 60)
    
    tests = [
        ("Dependencies", test_imports),
        ("CUDA Support", test_cuda),
        ("Configuration", test_config),
        ("Dataset", test_dataset),
        ("Embeddings", test_embeddings),
        ("Face Detector", test_face_detector),
        ("Face Recognizer", test_recognizer),
        ("Database", test_database),
        ("API Backend", test_api_backend),
    ]
    
    results = {}
    
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"  ❌ Test crashed: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name:25} {status}")
    
    print("\n" + "="*60)
    print(f"  Results: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is ready to use.")
        print("\nNext steps:")
        print("  1. Start backend: python src/api_backend.py")
        print("  2. Start frontend: cd admin-frontend && npm run dev")
        print("  3. Open browser: http://localhost:5173")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Missing dependencies: pip install -r requirements.txt")
        print("  - No dataset: Add images to dataset/PERSON_NAME/")
        print("  - No embeddings: python src/precompute_embeddings.py")
        print("  - No database: python src/api_backend.py (run once)")
    
    print("\n")
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
