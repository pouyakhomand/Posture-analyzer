#!/usr/bin/env python3
"""
Simple test script to verify the Posture Extractor Microservice works
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from app.main import app
        print("✅ app.main imported successfully")
        
        from app.services.pose_estimator import PoseEstimator
        print("✅ PoseEstimator imported successfully")
        
        from app.services.angle_calculator import AngleCalculator
        print("✅ AngleCalculator imported successfully")
        
        from app.services.thumbnail_generator import ThumbnailGenerator
        print("✅ ThumbnailGenerator imported successfully")
        
        from app.models.response import Landmarks, JointAngles
        print("✅ Response models imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_services():
    """Test that services can be instantiated."""
    print("\nTesting service instantiation...")
    
    try:
        from app.services.pose_estimator import PoseEstimator
        from app.services.angle_calculator import AngleCalculator
        from app.services.thumbnail_generator import ThumbnailGenerator
        
        pose_estimator = PoseEstimator()
        print("✅ PoseEstimator instantiated")
        
        angle_calculator = AngleCalculator()
        print("✅ AngleCalculator instantiated")
        
        thumbnail_generator = ThumbnailGenerator()
        print("✅ ThumbnailGenerator instantiated")
        
        return True
    except Exception as e:
        print(f"❌ Service instantiation error: {e}")
        return False

def test_models():
    """Test that models work correctly."""
    print("\nTesting models...")
    
    try:
        from app.models.response import Landmarks, LandmarkPoint, JointAngles
        
        # Test landmark creation
        landmark = LandmarkPoint(x=0.5, y=0.5, confidence=0.9)
        print("✅ LandmarkPoint created")
        
        # Test landmarks creation
        landmarks = Landmarks(
            nose=LandmarkPoint(x=0.5, y=0.15, confidence=0.9),
            left_shoulder=LandmarkPoint(x=0.42, y=0.25, confidence=0.9),
            right_shoulder=LandmarkPoint(x=0.58, y=0.25, confidence=0.9)
        )
        print("✅ Landmarks created")
        
        # Test joint angles creation
        joint_angles = JointAngles(
            neck_angle=45.0,
            spine_angle=180.0
        )
        print("✅ JointAngles created")
        
        return True
    except Exception as e:
        print(f"❌ Model error: {e}")
        return False

def test_geometry():
    """Test geometry calculations."""
    print("\nTesting geometry calculations...")
    
    try:
        from app.utils.geometry import calculate_angle, calculate_alignment_vector
        from app.models.response import LandmarkPoint
        
        # Test angle calculation
        point1 = LandmarkPoint(x=0.0, y=0.0)
        point2 = LandmarkPoint(x=0.0, y=1.0)
        point3 = LandmarkPoint(x=1.0, y=1.0)
        
        angle = calculate_angle(point1, point2, point3)
        print(f"✅ Angle calculation: {angle}")
        
        # Test alignment vector
        vector = calculate_alignment_vector(point1, point3)
        print(f"✅ Alignment vector: dx={vector.dx}, dy={vector.dy}")
        
        return True
    except Exception as e:
        print(f"❌ Geometry error: {e}")
        return False

def test_fastapi_app():
    """Test FastAPI app creation."""
    print("\nTesting FastAPI app...")
    
    try:
        from app.main import app
        
        # Check if app has expected attributes
        assert hasattr(app, 'routes')
        print("✅ FastAPI app created successfully")
        
        # Check if routes are registered
        routes = [route.path for route in app.routes]
        print(f"✅ Routes found: {routes}")
        
        return True
    except Exception as e:
        print(f"❌ FastAPI app error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Posture Extractor Microservice - Application Test")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_services,
        test_models,
        test_geometry,
        test_fastapi_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready to run.")
        print("\n🚀 To start the service, run:")
        print("   python start.py")
        print("   or")
        print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 