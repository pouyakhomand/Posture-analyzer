import cv2
import numpy as np
import uuid
from typing import Optional, Tuple
from pathlib import Path
from PIL import Image
import io
import base64
from ..core.config import settings
from ..utils.file_utils import ensure_thumbnail_directory, save_thumbnail, encode_image_to_base64


class ThumbnailGenerator:
    """Service for generating thumbnails from videos."""
    
    def __init__(self):
        """Initialize thumbnail generator."""
        self.thumbnail_dir = ensure_thumbnail_directory()
    
    def generate_thumbnail(self, video_path: str, landmarks=None) -> Tuple[str, str]:
        """Generate thumbnail from video and optionally draw landmarks."""
        # Extract representative frame
        frame = self._extract_representative_frame(video_path)
        if frame is None:
            raise ValueError("Could not extract frame from video")
        
        # Draw landmarks if provided
        if landmarks:
            frame = self._draw_landmarks_on_frame(frame, landmarks)
        
        # Generate filename
        thumbnail_filename = f"thumb_{uuid.uuid4()}.jpg"
        
        # Save thumbnail
        thumbnail_path = self._save_thumbnail(frame, thumbnail_filename)
        
        # Encode to base64
        thumbnail_base64 = self._encode_frame_to_base64(frame)
        
        return thumbnail_path, thumbnail_base64
    
    def _extract_representative_frame(self, video_path: str) -> Optional[np.ndarray]:
        """Extract a representative frame from video."""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None
        
        try:
            # Get video properties
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            if total_frames <= 0:
                return None
            
            # Extract middle frame
            middle_frame = total_frames // 2
            cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)
            
            ret, frame = cap.read()
            if not ret:
                # Try first frame if middle frame fails
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()
                if not ret:
                    return None
            
            return frame
            
        finally:
            cap.release()
    
    def _draw_landmarks_on_frame(self, frame: np.ndarray, landmarks) -> np.ndarray:
        """Draw landmarks on frame for visualization."""
        # Create a copy of the frame
        annotated_frame = frame.copy()
        
        # Draw landmarks
        for name, landmark in landmarks.__dict__.items():
            if landmark and landmark.confidence and landmark.confidence > 0.5:
                # Convert normalized coordinates to pixel coordinates
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                
                # Draw circle
                cv2.circle(annotated_frame, (x, y), 8, (0, 255, 0), -1)
                cv2.circle(annotated_frame, (x, y), 8, (0, 0, 0), 2)
                
                # Draw label
                cv2.putText(annotated_frame, name.replace('_', ' ').title(), 
                           (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.4, (255, 255, 255), 1)
        
        # Draw connections between landmarks
        self._draw_landmark_connections(annotated_frame, landmarks)
        
        return annotated_frame
    
    def _draw_landmark_connections(self, frame: np.ndarray, landmarks):
        """Draw connections between landmarks."""
        connections = [
            # Head and neck
            ('left_ear', 'left_shoulder'),
            ('right_ear', 'right_shoulder'),
            ('left_eye', 'right_eye'),
            
            # Shoulders and arms
            ('left_shoulder', 'right_shoulder'),
            ('left_shoulder', 'left_elbow'),
            ('right_shoulder', 'right_elbow'),
            ('left_elbow', 'left_wrist'),
            ('right_elbow', 'right_wrist'),
            
            # Torso
            ('left_shoulder', 'left_hip'),
            ('right_shoulder', 'right_hip'),
            ('left_hip', 'right_hip'),
            
            # Legs
            ('left_hip', 'left_knee'),
            ('right_hip', 'right_knee'),
            ('left_knee', 'left_ankle'),
            ('right_knee', 'right_ankle'),
        ]
        
        for start_name, end_name in connections:
            start_landmark = getattr(landmarks, start_name, None)
            end_landmark = getattr(landmarks, end_name, None)
            
            if (start_landmark and end_landmark and 
                start_landmark.confidence and end_landmark.confidence and
                start_landmark.confidence > 0.5 and end_landmark.confidence > 0.5):
                
                start_x = int(start_landmark.x * frame.shape[1])
                start_y = int(start_landmark.y * frame.shape[0])
                end_x = int(end_landmark.x * frame.shape[1])
                end_y = int(end_landmark.y * frame.shape[0])
                
                cv2.line(frame, (start_x, start_y), (end_x, end_y), (255, 255, 255), 2)
    
    def _save_thumbnail(self, frame: np.ndarray, filename: str) -> str:
        """Save frame as thumbnail image."""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(rgb_frame)
        
        # Save with quality setting
        thumbnail_path = self.thumbnail_dir / filename
        
        # Save as JPEG with specified quality
        pil_image.save(thumbnail_path, 'JPEG', quality=settings.THUMBNAIL_QUALITY)
        
        return str(thumbnail_path)
    
    def _encode_frame_to_base64(self, frame: np.ndarray) -> str:
        """Encode frame to base64 string."""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(rgb_frame)
        
        # Convert to bytes
        buffer = io.BytesIO()
        pil_image.save(buffer, format='JPEG', quality=settings.THUMBNAIL_QUALITY)
        buffer.seek(0)
        
        # Encode to base64
        image_bytes = buffer.getvalue()
        base64_string = base64.b64encode(image_bytes).decode('utf-8')
        
        return base64_string
    
    def get_thumbnail_url(self, thumbnail_path: str) -> str:
        """Get URL for thumbnail."""
        # Extract filename from path
        filename = Path(thumbnail_path).name
        return f"/static/thumbnails/{filename}"
    
    def resize_thumbnail(self, frame: np.ndarray, max_width: int = 400, max_height: int = 600) -> np.ndarray:
        """Resize thumbnail to specified dimensions."""
        height, width = frame.shape[:2]
        
        # Calculate scaling factor
        scale_x = max_width / width
        scale_y = max_height / height
        scale = min(scale_x, scale_y, 1.0)  # Don't upscale
        
        if scale < 1.0:
            new_width = int(width * scale)
            new_height = int(height * scale)
            frame = cv2.resize(frame, (new_width, new_height))
        
        return frame 