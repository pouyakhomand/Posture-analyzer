import pytest
import numpy as np
from app.models.response import LandmarkPoint, Landmarks
from app.services.angle_calculator import AngleCalculator
from app.utils.geometry import calculate_angle, calculate_alignment_vector


def test_calculate_angle():
    """Test angle calculation between three points."""
    # Create test points
    point1 = LandmarkPoint(x=0.0, y=0.0)
    point2 = LandmarkPoint(x=0.0, y=1.0)  # Vertex
    point3 = LandmarkPoint(x=1.0, y=1.0)
    
    angle = calculate_angle(point1, point2, point3)
    assert angle is not None
    assert 0 <= angle <= 180


def test_calculate_alignment_vector():
    """Test alignment vector calculation."""
    point1 = LandmarkPoint(x=0.0, y=0.0)
    point2 = LandmarkPoint(x=1.0, y=1.0)
    
    vector = calculate_alignment_vector(point1, point2)
    assert vector is not None
    assert vector.dx == 1.0
    assert vector.dy == 1.0
    assert vector.magnitude > 0


def test_angle_calculator():
    """Test angle calculator service."""
    calculator = AngleCalculator()
    
    # Create test landmarks
    landmarks = Landmarks(
        left_ear=LandmarkPoint(x=0.5, y=0.1),
        left_shoulder=LandmarkPoint(x=0.5, y=0.2),
        left_hip=LandmarkPoint(x=0.5, y=0.4),
        left_knee=LandmarkPoint(x=0.5, y=0.6),
        left_ankle=LandmarkPoint(x=0.5, y=0.8),
        right_ear=LandmarkPoint(x=0.6, y=0.1),
        right_shoulder=LandmarkPoint(x=0.6, y=0.2),
        right_hip=LandmarkPoint(x=0.6, y=0.4),
        right_knee=LandmarkPoint(x=0.6, y=0.6),
        right_ankle=LandmarkPoint(x=0.6, y=0.8),
        left_elbow=LandmarkPoint(x=0.4, y=0.3),
        right_elbow=LandmarkPoint(x=0.7, y=0.3),
        left_wrist=LandmarkPoint(x=0.3, y=0.4),
        right_wrist=LandmarkPoint(x=0.8, y=0.4)
    )
    
    # Test joint angles
    joint_angles = calculator.calculate_joint_angles(landmarks)
    assert joint_angles is not None
    
    # Test alignment vectors
    alignment_vectors = calculator.calculate_alignment_vectors(landmarks)
    assert alignment_vectors is not None
    
    # Test symmetry
    symmetry = calculator.calculate_symmetry(landmarks)
    assert symmetry is not None


def test_landmark_validation():
    """Test landmark validation."""
    # Test with missing landmarks
    landmarks = Landmarks(
        left_shoulder=LandmarkPoint(x=0.5, y=0.2),
        right_shoulder=LandmarkPoint(x=0.6, y=0.2),
        left_hip=LandmarkPoint(x=0.5, y=0.4)
        # Missing right_hip
    )
    
    calculator = AngleCalculator()
    joint_angles = calculator.calculate_joint_angles(landmarks)
    
    # Should handle missing landmarks gracefully
    assert joint_angles is not None 