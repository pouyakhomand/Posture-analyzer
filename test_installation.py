#!/usr/bin/env python3
"""
Test script to verify Posture Extractor Microservice installation
"""

import sys
import importlib

def test_imports():
    """Test that all required packages can be imported."""
    required_packages = [
        'fastapi',
        'uvicorn',
        'opencv-python',
        'numpy',
        'pydantic',
        'PIL',
        'aiofiles'
    ]
    
    print("🔍 Testing package imports...")
    
    for package in required_packages:
        try:
            if package == 'opencv-python':
                importlib.import_module('cv2')
            elif package == 'PIL':
                importlib.import_module('PIL')
            else:
                importlib.import_module(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            return False
    
    # Test MediaPipe separately
    try:
        importlib.import_module('mediapipe')
        print("✅ mediapipe")
    except ImportError:
        print("⚠️  mediapipe: Not available (will use mock implementation)")
    
    return True

def test_app_imports():
    """Test that the application modules can be imported."""
    print("\n🔍 Testing application imports...")
    
    try:
        from app.main import app
        print("✅ app.main")
        
        from app.services.pose_estimator import PoseEstimator
        print("✅ app.services.pose_estimator")
        
        from app.services.angle_calculator import AngleCalculator
        print("✅ app.services.angle_calculator")
        
        from app.services.thumbnail_generator import ThumbnailGenerator
        print("✅ app.services.thumbnail_generator")
        
        from app.models.response import Landmarks, JointAngles
        print("✅ app.models.response")
        
        from app.utils.geometry import calculate_angle
        print("✅ app.utils.geometry")
        
        return True
        
    except ImportError as e:
        print(f"❌ Application import error: {e}")
        return False

def test_mediapipe():
    """Test MediaPipe initialization."""
    print("\n🔍 Testing MediaPipe...")
    
    try:
        import mediapipe as mp
        pose = mp.solutions.pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            enable_segmentation=False,
            smooth_segmentation=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        pose.close()
        print("✅ MediaPipe pose estimation")
        return True
    except ImportError:
        print("⚠️  MediaPipe not available - using mock implementation")
        return True
    except Exception as e:
        print(f"❌ MediaPipe error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Posture Extractor Microservice - Installation Test")
    print("=" * 60)
    
    # Test package imports
    if not test_imports():
        print("\n❌ Package import test failed!")
        sys.exit(1)
    
    # Test app imports
    if not test_app_imports():
        print("\n❌ Application import test failed!")
        sys.exit(1)
    
    # Test MediaPipe
    if not test_mediapipe():
        print("\n❌ MediaPipe test failed!")
        sys.exit(1)
    
    print("\n🎉 All tests passed! Installation is successful.")
    print("\n🚀 You can now start the service with:")
    print("   python start.py")
    print("   or")
    print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main() 