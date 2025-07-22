from typing import Optional
from ..models.response import Landmarks, JointAngles, AlignmentVectors, Symmetry
from ..utils.geometry import calculate_angle, calculate_alignment_vector, calculate_symmetry, calculate_width_ratio


class AngleCalculator:
    """Service for calculating joint angles and alignment vectors."""
    
    def calculate_joint_angles(self, landmarks: Landmarks) -> JointAngles:
        """Calculate all joint angles from landmarks."""
        return JointAngles(
            neck_angle=self._calculate_neck_angle(landmarks),
            spine_angle=self._calculate_spine_angle(landmarks),
            left_shoulder_angle=self._calculate_shoulder_angle(landmarks, 'left'),
            right_shoulder_angle=self._calculate_shoulder_angle(landmarks, 'right'),
            left_elbow_angle=self._calculate_elbow_angle(landmarks, 'left'),
            right_elbow_angle=self._calculate_elbow_angle(landmarks, 'right'),
            left_hip_angle=self._calculate_hip_angle(landmarks, 'left'),
            right_hip_angle=self._calculate_hip_angle(landmarks, 'right'),
            left_knee_angle=self._calculate_knee_angle(landmarks, 'left'),
            right_knee_angle=self._calculate_knee_angle(landmarks, 'right')
        )
    
    def calculate_alignment_vectors(self, landmarks: Landmarks) -> AlignmentVectors:
        """Calculate alignment vectors from landmarks."""
        return AlignmentVectors(
            ear_to_shoulder=self._calculate_ear_to_shoulder_vector(landmarks),
            shoulder_to_hip=self._calculate_shoulder_to_hip_vector(landmarks),
            hip_to_knee=self._calculate_hip_to_knee_vector(landmarks),
            knee_to_ankle=self._calculate_knee_to_ankle_vector(landmarks)
        )
    
    def calculate_symmetry(self, landmarks: Landmarks) -> Symmetry:
        """Calculate symmetry metrics from landmarks."""
        return Symmetry(
            shoulder_height_diff=self._calculate_shoulder_height_diff(landmarks),
            hip_height_diff=self._calculate_hip_height_diff(landmarks),
            shoulder_width_ratio=self._calculate_shoulder_width_ratio(landmarks),
            hip_width_ratio=self._calculate_hip_width_ratio(landmarks)
        )
    
    def _calculate_neck_angle(self, landmarks: Landmarks) -> Optional[float]:
        """Calculate neck angle (ear to shoulder to hip)."""
        if not all([landmarks.left_ear, landmarks.left_shoulder, landmarks.left_hip]):
            return None
        
        return calculate_angle(
            landmarks.left_ear,
            landmarks.left_shoulder,
            landmarks.left_hip
        )
    
    def _calculate_spine_angle(self, landmarks: Landmarks) -> Optional[float]:
        """Calculate spine angle (shoulder to hip to knee)."""
        # Use center points for spine calculation
        if not all([landmarks.left_shoulder, landmarks.right_shoulder,
                   landmarks.left_hip, landmarks.right_hip,
                   landmarks.left_knee, landmarks.right_knee]):
            return None
        
        # Calculate center points
        shoulder_center_x = (landmarks.left_shoulder.x + landmarks.right_shoulder.x) / 2
        shoulder_center_y = (landmarks.left_shoulder.y + landmarks.right_shoulder.y) / 2
        hip_center_x = (landmarks.left_hip.x + landmarks.right_hip.x) / 2
        hip_center_y = (landmarks.left_hip.y + landmarks.right_hip.y) / 2
        knee_center_x = (landmarks.left_knee.x + landmarks.right_knee.x) / 2
        knee_center_y = (landmarks.left_knee.y + landmarks.right_knee.y) / 2
        
        # Create temporary landmark points
        from ..models.response import LandmarkPoint
        shoulder_center = LandmarkPoint(x=shoulder_center_x, y=shoulder_center_y)
        hip_center = LandmarkPoint(x=hip_center_x, y=hip_center_y)
        knee_center = LandmarkPoint(x=knee_center_x, y=knee_center_y)
        
        return calculate_angle(shoulder_center, hip_center, knee_center)
    
    def _calculate_shoulder_angle(self, landmarks: Landmarks, side: str) -> Optional[float]:
        """Calculate shoulder angle (ear to shoulder to elbow)."""
        if side == 'left':
            if not all([landmarks.left_ear, landmarks.left_shoulder, landmarks.left_elbow]):
                return None
            return calculate_angle(landmarks.left_ear, landmarks.left_shoulder, landmarks.left_elbow)
        else:
            if not all([landmarks.right_ear, landmarks.right_shoulder, landmarks.right_elbow]):
                return None
            return calculate_angle(landmarks.right_ear, landmarks.right_shoulder, landmarks.right_elbow)
    
    def _calculate_elbow_angle(self, landmarks: Landmarks, side: str) -> Optional[float]:
        """Calculate elbow angle (shoulder to elbow to wrist)."""
        if side == 'left':
            if not all([landmarks.left_shoulder, landmarks.left_elbow, landmarks.left_wrist]):
                return None
            return calculate_angle(landmarks.left_shoulder, landmarks.left_elbow, landmarks.left_wrist)
        else:
            if not all([landmarks.right_shoulder, landmarks.right_elbow, landmarks.right_wrist]):
                return None
            return calculate_angle(landmarks.right_shoulder, landmarks.right_elbow, landmarks.right_wrist)
    
    def _calculate_hip_angle(self, landmarks: Landmarks, side: str) -> Optional[float]:
        """Calculate hip angle (shoulder to hip to knee)."""
        if side == 'left':
            if not all([landmarks.left_shoulder, landmarks.left_hip, landmarks.left_knee]):
                return None
            return calculate_angle(landmarks.left_shoulder, landmarks.left_hip, landmarks.left_knee)
        else:
            if not all([landmarks.right_shoulder, landmarks.right_hip, landmarks.right_knee]):
                return None
            return calculate_angle(landmarks.right_shoulder, landmarks.right_hip, landmarks.right_knee)
    
    def _calculate_knee_angle(self, landmarks: Landmarks, side: str) -> Optional[float]:
        """Calculate knee angle (hip to knee to ankle)."""
        if side == 'left':
            if not all([landmarks.left_hip, landmarks.left_knee, landmarks.left_ankle]):
                return None
            return calculate_angle(landmarks.left_hip, landmarks.left_knee, landmarks.left_ankle)
        else:
            if not all([landmarks.right_hip, landmarks.right_knee, landmarks.right_ankle]):
                return None
            return calculate_angle(landmarks.right_hip, landmarks.right_knee, landmarks.right_ankle)
    
    def _calculate_ear_to_shoulder_vector(self, landmarks: Landmarks):
        """Calculate ear to shoulder alignment vector."""
        if not all([landmarks.left_ear, landmarks.left_shoulder]):
            return None
        
        return calculate_alignment_vector(landmarks.left_ear, landmarks.left_shoulder)
    
    def _calculate_shoulder_to_hip_vector(self, landmarks: Landmarks):
        """Calculate shoulder to hip alignment vector."""
        if not all([landmarks.left_shoulder, landmarks.left_hip]):
            return None
        
        return calculate_alignment_vector(landmarks.left_shoulder, landmarks.left_hip)
    
    def _calculate_hip_to_knee_vector(self, landmarks: Landmarks):
        """Calculate hip to knee alignment vector."""
        if not all([landmarks.left_hip, landmarks.left_knee]):
            return None
        
        return calculate_alignment_vector(landmarks.left_hip, landmarks.left_knee)
    
    def _calculate_knee_to_ankle_vector(self, landmarks: Landmarks):
        """Calculate knee to ankle alignment vector."""
        if not all([landmarks.left_knee, landmarks.left_ankle]):
            return None
        
        return calculate_alignment_vector(landmarks.left_knee, landmarks.left_ankle)
    
    def _calculate_shoulder_height_diff(self, landmarks: Landmarks) -> Optional[float]:
        """Calculate shoulder height difference."""
        if not all([landmarks.left_shoulder, landmarks.right_shoulder]):
            return None
        
        return calculate_symmetry(landmarks.left_shoulder, landmarks.right_shoulder)
    
    def _calculate_hip_height_diff(self, landmarks: Landmarks) -> Optional[float]:
        """Calculate hip height difference."""
        if not all([landmarks.left_hip, landmarks.right_hip]):
            return None
        
        return calculate_symmetry(landmarks.left_hip, landmarks.right_hip)
    
    def _calculate_shoulder_width_ratio(self, landmarks: Landmarks) -> Optional[float]:
        """Calculate shoulder width ratio relative to hip width."""
        if not all([landmarks.left_shoulder, landmarks.right_shoulder,
                   landmarks.left_hip, landmarks.right_hip]):
            return None
        
        return calculate_width_ratio(
            landmarks.left_shoulder, landmarks.right_shoulder,
            landmarks.left_hip, landmarks.right_hip
        )
    
    def _calculate_hip_width_ratio(self, landmarks: Landmarks) -> Optional[float]:
        """Calculate hip width ratio relative to shoulder width."""
        if not all([landmarks.left_shoulder, landmarks.right_shoulder,
                   landmarks.left_hip, landmarks.right_hip]):
            return None
        
        return calculate_width_ratio(
            landmarks.left_hip, landmarks.right_hip,
            landmarks.left_shoulder, landmarks.right_shoulder
        ) 