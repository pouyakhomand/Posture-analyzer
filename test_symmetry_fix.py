#!/usr/bin/env python3
"""
Test script to verify the symmetry validation fix.
"""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_symmetry_validation():
    """Test that the Symmetry model accepts realistic width ratios."""
    print("Testing Symmetry model validation...")
    
    try:
        from models.response import Symmetry
        
        # Test with the problematic ratio that was causing the error
        symmetry = Symmetry(
            shoulder_height_diff=0.1,
            hip_height_diff=0.05,
            shoulder_width_ratio=2.6786787224063247,  # This was the value causing the error
            hip_width_ratio=0.5
        )
        
        print("✅ Symmetry model created successfully with ratio 2.68")
        
        # Test with even higher ratios to ensure the fix works
        symmetry2 = Symmetry(
            shoulder_height_diff=0.2,
            hip_height_diff=0.1,
            shoulder_width_ratio=3.5,  # Test higher ratio
            hip_width_ratio=0.8
        )
        
        print("✅ Symmetry model created successfully with ratio 3.5")
        
        # Test with very high ratio
        symmetry3 = Symmetry(
            shoulder_height_diff=0.3,
            hip_height_diff=0.15,
            shoulder_width_ratio=4.8,  # Test near the new limit
            hip_width_ratio=1.2
        )
        
        print("✅ Symmetry model created successfully with ratio 4.8")
        
        print("\n🎉 All symmetry validation tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Symmetry validation test failed: {e}")
        return False

def test_angle_calculator_symmetry():
    """Test that the angle calculator can create symmetry objects."""
    print("\nTesting AngleCalculator symmetry creation...")
    
    try:
        from models.response import Landmarks, LandmarkPoint
        from services.angle_calculator import AngleCalculator
        
        # Create test landmarks with realistic ratios
        landmarks = Landmarks(
            left_shoulder=LandmarkPoint(x=0.3, y=0.2, confidence=0.9),
            right_shoulder=LandmarkPoint(x=0.7, y=0.2, confidence=0.9),
            left_hip=LandmarkPoint(x=0.4, y=0.5, confidence=0.9),
            right_hip=LandmarkPoint(x=0.6, y=0.5, confidence=0.9)
        )
        
        calculator = AngleCalculator()
        symmetry = calculator.calculate_symmetry(landmarks)
        
        print(f"✅ Symmetry calculated successfully:")
        print(f"   - Shoulder height diff: {symmetry.shoulder_height_diff}")
        print(f"   - Hip height diff: {symmetry.hip_height_diff}")
        print(f"   - Shoulder width ratio: {symmetry.shoulder_width_ratio}")
        print(f"   - Hip width ratio: {symmetry.hip_width_ratio}")
        
        return True
        
    except Exception as e:
        print(f"❌ AngleCalculator symmetry test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing Symmetry Validation Fix")
    print("=" * 40)
    
    # Test 1: Direct model validation
    test1_passed = test_symmetry_validation()
    
    # Test 2: Angle calculator integration
    test2_passed = test_angle_calculator_symmetry()
    
    print("\n" + "=" * 40)
    if test1_passed and test2_passed:
        print("🎉 All tests passed! The symmetry validation fix is working correctly.")
        print("\nThe API should now accept realistic shoulder width ratios.")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        sys.exit(1) 