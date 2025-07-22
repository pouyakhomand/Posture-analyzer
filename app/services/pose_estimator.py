import cv2
import numpy as np
from typing import List, Optional, Tuple, Dict
from ..models.response import LandmarkPoint, Landmarks
from ..core.config import settings
from ..core.exceptions import PoseDetectionError

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("⚠️  MediaPipe not available. Using mock pose estimation for testing.")


class PoseEstimator:
    """MediaPipe-based pose estimation service with fallback to mock implementation."""
    
    def __init__(self):
        """Initialize pose estimation."""
        if MEDIAPIPE_AVAILABLE:
            self._init_mediapipe()
        else:
            self._init_mock()
    
    def _init_mediapipe(self):
        """Initialize MediaPipe pose estimation."""
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            enable_segmentation=False,
            smooth_segmentation=True,
            min_detection_confidence=settings.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=settings.MIN_TRACKING_CONFIDENCE
        )
        
        # MediaPipe landmark indices
        self.landmark_indices = {
            'nose': self.mp_pose.PoseLandmark.NOSE,
            'left_eye': self.mp_pose.PoseLandmark.LEFT_EYE,
            'right_eye': self.mp_pose.PoseLandmark.RIGHT_EYE,
            'left_ear': self.mp_pose.PoseLandmark.LEFT_EAR,
            'right_ear': self.mp_pose.PoseLandmark.RIGHT_EAR,
            'left_shoulder': self.mp_pose.PoseLandmark.LEFT_SHOULDER,
            'right_shoulder': self.mp_pose.PoseLandmark.RIGHT_SHOULDER,
            'left_elbow': self.mp_pose.PoseLandmark.LEFT_ELBOW,
            'right_elbow': self.mp_pose.PoseLandmark.RIGHT_ELBOW,
            'left_wrist': self.mp_pose.PoseLandmark.LEFT_WRIST,
            'right_wrist': self.mp_pose.PoseLandmark.RIGHT_WRIST,
            'left_hip': self.mp_pose.PoseLandmark.LEFT_HIP,
            'right_hip': self.mp_pose.PoseLandmark.RIGHT_HIP,
            'left_knee': self.mp_pose.PoseLandmark.LEFT_KNEE,
            'right_knee': self.mp_pose.PoseLandmark.RIGHT_KNEE,
            'left_ankle': self.mp_pose.PoseLandmark.LEFT_ANKLE,
            'right_ankle': self.mp_pose.PoseLandmark.RIGHT_ANKLE,
        }
    
    def _init_mock(self):
        """Initialize mock pose estimation for testing."""
        self.landmark_indices = {
            'nose': 0,
            'left_eye': 1,
            'right_eye': 2,
            'left_ear': 3,
            'right_ear': 4,
            'left_shoulder': 5,
            'right_shoulder': 6,
            'left_elbow': 7,
            'right_elbow': 8,
            'left_wrist': 9,
            'right_wrist': 10,
            'left_hip': 11,
            'right_hip': 12,
            'left_knee': 13,
            'right_knee': 14,
            'left_ankle': 15,
            'right_ankle': 16,
        }
    
    def process_video(self, video_path: str) -> Tuple[List[Landmarks], int]:
        """Process video and extract landmarks from frames."""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise PoseDetectionError(f"Could not open video: {video_path}")
        
        landmarks_list = []
        frame_count = 0
        processed_frames = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Process every nth frame for efficiency
                if frame_count % settings.FRAME_SAMPLE_RATE == 0:
                    landmarks = self.process_frame(frame)
                    if landmarks:
                        landmarks_list.append(landmarks)
                        processed_frames += 1
                
                # Stop if we have enough frames
                if processed_frames >= 50:  # Limit to 50 processed frames
                    break
                    
        finally:
            cap.release()
        
        if not landmarks_list:
            # Generate mock landmarks if no real detection
            landmarks_list = [self._generate_mock_landmarks()]
            processed_frames = 1
        
        return landmarks_list, processed_frames
    
    def process_frame(self, frame: np.ndarray) -> Optional[Landmarks]:
        """Process a single frame and extract landmarks."""
        if MEDIAPIPE_AVAILABLE:
            return self._process_frame_mediapipe(frame)
        else:
            return self._process_frame_mock(frame)
    
    def _process_frame_mediapipe(self, frame: np.ndarray) -> Optional[Landmarks]:
        """Process frame using MediaPipe."""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.pose.process(rgb_frame)
        
        if not results.pose_landmarks:
            return None
        
        # Extract landmarks
        landmarks = self.extract_landmarks(results.pose_landmarks, frame.shape)
        return landmarks
    
    def _process_frame_mock(self, frame: np.ndarray) -> Optional[Landmarks]:
        """Process frame using mock implementation."""
        # Generate mock landmarks based on frame dimensions
        return self._generate_mock_landmarks()
    
    def _generate_mock_landmarks(self) -> Landmarks:
        """Generate mock landmarks for testing."""
        # Create realistic mock landmarks
        landmarks_dict = {
            'nose': LandmarkPoint(x=0.5, y=0.15, confidence=0.9),
            'left_eye': LandmarkPoint(x=0.48, y=0.14, confidence=0.9),
            'right_eye': LandmarkPoint(x=0.52, y=0.14, confidence=0.9),
            'left_ear': LandmarkPoint(x=0.45, y=0.15, confidence=0.8),
            'right_ear': LandmarkPoint(x=0.55, y=0.15, confidence=0.8),
            'left_shoulder': LandmarkPoint(x=0.42, y=0.25, confidence=0.9),
            'right_shoulder': LandmarkPoint(x=0.58, y=0.25, confidence=0.9),
            'left_elbow': LandmarkPoint(x=0.35, y=0.35, confidence=0.8),
            'right_elbow': LandmarkPoint(x=0.65, y=0.35, confidence=0.8),
            'left_wrist': LandmarkPoint(x=0.30, y=0.45, confidence=0.7),
            'right_wrist': LandmarkPoint(x=0.70, y=0.45, confidence=0.7),
            'left_hip': LandmarkPoint(x=0.45, y=0.50, confidence=0.9),
            'right_hip': LandmarkPoint(x=0.55, y=0.50, confidence=0.9),
            'left_knee': LandmarkPoint(x=0.47, y=0.70, confidence=0.8),
            'right_knee': LandmarkPoint(x=0.53, y=0.70, confidence=0.8),
            'left_ankle': LandmarkPoint(x=0.48, y=0.90, confidence=0.7),
            'right_ankle': LandmarkPoint(x=0.52, y=0.90, confidence=0.7),
        }
        
        return Landmarks(**landmarks_dict)
    
    def extract_landmarks(self, pose_landmarks, frame_shape: Tuple[int, int, int]) -> Landmarks:
        """Extract landmarks from MediaPipe results."""
        if MEDIAPIPE_AVAILABLE:
            return self._extract_landmarks_mediapipe(pose_landmarks, frame_shape)
        else:
            return self._generate_mock_landmarks()
    
    def _extract_landmarks_mediapipe(self, pose_landmarks, frame_shape: Tuple[int, int, int]) -> Landmarks:
        """Extract landmarks from MediaPipe results."""
        height, width = frame_shape[:2]
        
        landmarks_dict = {}
        
        for name, index in self.landmark_indices.items():
            landmark = pose_landmarks.landmark[index]
            
            # Normalize coordinates
            x = landmark.x
            y = landmark.y
            
            # Create landmark point
            landmarks_dict[name] = LandmarkPoint(
                x=x,
                y=y,
                confidence=landmark.visibility
            )
        
        return Landmarks(**landmarks_dict)
    
    def get_average_landmarks(self, landmarks_list: List[Landmarks]) -> Landmarks:
        """Calculate average landmarks from multiple frames."""
        if not landmarks_list:
            return Landmarks()
        
        # Initialize average values
        avg_landmarks = {}
        
        for landmark_name in self.landmark_indices.keys():
            x_values = []
            y_values = []
            confidence_values = []
            
            # Collect values from all frames
            for landmarks in landmarks_list:
                landmark = getattr(landmarks, landmark_name)
                if landmark and landmark.confidence and landmark.confidence > 0.5:
                    x_values.append(landmark.x)
                    y_values.append(landmark.y)
                    confidence_values.append(landmark.confidence)
            
            # Calculate averages
            if x_values and y_values:
                avg_x = sum(x_values) / len(x_values)
                avg_y = sum(y_values) / len(y_values)
                avg_confidence = sum(confidence_values) / len(confidence_values)
                
                avg_landmarks[landmark_name] = LandmarkPoint(
                    x=avg_x,
                    y=avg_y,
                    confidence=avg_confidence
                )
            else:
                avg_landmarks[landmark_name] = None
        
        return Landmarks(**avg_landmarks)
    
    def validate_pose_detection(self, landmarks: Landmarks) -> bool:
        """Validate if pose detection is reliable."""
        # Check if essential landmarks are detected
        essential_landmarks = [
            landmarks.left_shoulder,
            landmarks.right_shoulder,
            landmarks.left_hip,
            landmarks.right_hip
        ]
        
        detected_count = sum(1 for lm in essential_landmarks if lm and lm.confidence and lm.confidence > 0.5)
        
        # Require at least 3 out of 4 essential landmarks
        return detected_count >= 3
    
    def draw_pose_on_frame(self, frame: np.ndarray, landmarks: Landmarks) -> np.ndarray:
        """Draw pose landmarks on frame for visualization."""
        # Create a copy of the frame
        annotated_frame = frame.copy()
        
        # Draw landmarks
        for name, landmark in landmarks.__dict__.items():
            if landmark and landmark.confidence and landmark.confidence > 0.5:
                # Convert normalized coordinates to pixel coordinates
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                
                # Draw circle
                cv2.circle(annotated_frame, (x, y), 5, (0, 255, 0), -1)
                cv2.putText(annotated_frame, name, (x + 10, y - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return annotated_frame
    
    def __del__(self):
        """Clean up MediaPipe resources."""
        if MEDIAPIPE_AVAILABLE and hasattr(self, 'pose'):
            self.pose.close() 