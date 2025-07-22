import math
import numpy as np
from typing import Tuple, Optional, List
from ..models.response import LandmarkPoint, AlignmentVector


def calculate_distance(point1: LandmarkPoint, point2: LandmarkPoint) -> float:
    """Calculate Euclidean distance between two points."""
    if not point1 or not point2:
        return 0.0
    
    dx = point2.x - point1.x
    dy = point2.y - point1.y
    return math.sqrt(dx * dx + dy * dy)


def calculate_angle(point1: LandmarkPoint, point2: LandmarkPoint, point3: LandmarkPoint) -> Optional[float]:
    """Calculate angle between three points (point2 is the vertex)."""
    if not all([point1, point2, point3]):
        return None
    
    # Calculate vectors
    v1 = (point1.x - point2.x, point1.y - point2.y)
    v2 = (point3.x - point2.x, point3.y - point2.y)
    
    # Calculate dot product
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    
    # Calculate magnitudes
    mag1 = math.sqrt(v1[0] * v1[0] + v1[1] * v1[1])
    mag2 = math.sqrt(v2[0] * v2[0] + v2[1] * v2[1])
    
    # Avoid division by zero
    if mag1 == 0 or mag2 == 0:
        return None
    
    # Calculate cosine of angle
    cos_angle = dot_product / (mag1 * mag2)
    
    # Clamp to valid range
    cos_angle = max(-1.0, min(1.0, cos_angle))
    
    # Convert to degrees
    angle_rad = math.acos(cos_angle)
    angle_deg = math.degrees(angle_rad)
    
    return angle_deg


def calculate_alignment_vector(point1: LandmarkPoint, point2: LandmarkPoint) -> Optional[AlignmentVector]:
    """Calculate alignment vector between two points."""
    if not point1 or not point2:
        return None
    
    dx = point2.x - point1.x
    dy = point2.y - point1.y
    magnitude = math.sqrt(dx * dx + dy * dy)
    
    # Calculate angle in degrees
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    
    # Normalize angle to 0-360 range
    if angle_deg < 0:
        angle_deg += 360
    
    return AlignmentVector(
        dx=dx,
        dy=dy,
        magnitude=magnitude,
        angle_degrees=angle_deg
    )


def calculate_symmetry(left_point: LandmarkPoint, right_point: LandmarkPoint) -> Optional[float]:
    """Calculate symmetry between left and right points."""
    if not left_point or not right_point:
        return None
    
    # Calculate height difference (normalized)
    height_diff = abs(left_point.y - right_point.y)
    return height_diff


def calculate_width_ratio(left_point: LandmarkPoint, right_point: LandmarkPoint, 
                         reference_left: LandmarkPoint, reference_right: LandmarkPoint) -> Optional[float]:
    """Calculate width ratio between two pairs of points."""
    if not all([left_point, right_point, reference_left, reference_right]):
        return None
    
    # Calculate widths
    width1 = abs(left_point.x - right_point.x)
    width2 = abs(reference_left.x - reference_right.x)
    
    if width2 == 0:
        return None
    
    return width1 / width2


def smooth_landmarks(landmarks_list: List[List[LandmarkPoint]], window_size: int = 5) -> List[LandmarkPoint]:
    """Apply moving average smoothing to landmarks."""
    if not landmarks_list or len(landmarks_list) < window_size:
        return landmarks_list[-1] if landmarks_list else []
    
    smoothed = []
    num_landmarks = len(landmarks_list[0])
    
    for i in range(num_landmarks):
        x_values = []
        y_values = []
        
        # Collect values for the window
        for j in range(max(0, len(landmarks_list) - window_size), len(landmarks_list)):
            if i < len(landmarks_list[j]):
                landmark = landmarks_list[j][i]
                if landmark:
                    x_values.append(landmark.x)
                    y_values.append(landmark.y)
        
        # Calculate average
        if x_values and y_values:
            avg_x = sum(x_values) / len(x_values)
            avg_y = sum(y_values) / len(y_values)
            smoothed.append(LandmarkPoint(x=avg_x, y=avg_y))
        else:
            smoothed.append(None)
    
    return smoothed


def normalize_coordinates(x: float, y: float, width: int, height: int) -> Tuple[float, float]:
    """Normalize coordinates to 0-1 range."""
    norm_x = x / width if width > 0 else 0.0
    norm_y = y / height if height > 0 else 0.0
    return norm_x, norm_y


def denormalize_coordinates(norm_x: float, norm_y: float, width: int, height: int) -> Tuple[float, float]:
    """Denormalize coordinates from 0-1 range to pixel coordinates."""
    x = norm_x * width
    y = norm_y * height
    return x, y


def calculate_center_point(point1: LandmarkPoint, point2: LandmarkPoint) -> Optional[LandmarkPoint]:
    """Calculate the center point between two landmarks."""
    if not point1 or not point2:
        return None
    
    center_x = (point1.x + point2.x) / 2
    center_y = (point1.y + point2.y) / 2
    
    return LandmarkPoint(x=center_x, y=center_y)


def calculate_plumb_line_deviation(ear: LandmarkPoint, shoulder: LandmarkPoint, 
                                 hip: LandmarkPoint, ankle: LandmarkPoint) -> Optional[float]:
    """Calculate deviation from plumb line (ideal posture)."""
    if not all([ear, shoulder, hip, ankle]):
        return None
    
    # Calculate ideal vertical line (x = 0.5)
    ideal_x = 0.5
    
    # Calculate average x position of body points
    body_x = (ear.x + shoulder.x + hip.x + ankle.x) / 4
    
    # Calculate deviation
    deviation = abs(body_x - ideal_x)
    
    return deviation 