from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
from .request import VideoAngle


class LandmarkPoint(BaseModel):
    """2D landmark point."""
    x: float = Field(..., ge=0, le=1, description="Normalized x coordinate")
    y: float = Field(..., ge=0, le=1, description="Normalized y coordinate")
    confidence: Optional[float] = Field(None, ge=0, le=1, description="Detection confidence")


class Landmarks(BaseModel):
    """Body landmarks."""
    nose: Optional[LandmarkPoint] = None
    left_eye: Optional[LandmarkPoint] = None
    right_eye: Optional[LandmarkPoint] = None
    left_ear: Optional[LandmarkPoint] = None
    right_ear: Optional[LandmarkPoint] = None
    left_shoulder: Optional[LandmarkPoint] = None
    right_shoulder: Optional[LandmarkPoint] = None
    left_elbow: Optional[LandmarkPoint] = None
    right_elbow: Optional[LandmarkPoint] = None
    left_wrist: Optional[LandmarkPoint] = None
    right_wrist: Optional[LandmarkPoint] = None
    left_hip: Optional[LandmarkPoint] = None
    right_hip: Optional[LandmarkPoint] = None
    left_knee: Optional[LandmarkPoint] = None
    right_knee: Optional[LandmarkPoint] = None
    left_ankle: Optional[LandmarkPoint] = None
    right_ankle: Optional[LandmarkPoint] = None


class JointAngles(BaseModel):
    """Calculated joint angles."""
    neck_angle: Optional[float] = Field(None, ge=0, le=180, description="Neck angle in degrees")
    spine_angle: Optional[float] = Field(None, ge=0, le=180, description="Spine angle in degrees")
    left_shoulder_angle: Optional[float] = Field(None, ge=0, le=180, description="Left shoulder angle in degrees")
    right_shoulder_angle: Optional[float] = Field(None, ge=0, le=180, description="Right shoulder angle in degrees")
    left_elbow_angle: Optional[float] = Field(None, ge=0, le=180, description="Left elbow angle in degrees")
    right_elbow_angle: Optional[float] = Field(None, ge=0, le=180, description="Right elbow angle in degrees")
    left_hip_angle: Optional[float] = Field(None, ge=0, le=180, description="Left hip angle in degrees")
    right_hip_angle: Optional[float] = Field(None, ge=0, le=180, description="Right hip angle in degrees")
    left_knee_angle: Optional[float] = Field(None, ge=0, le=180, description="Left knee angle in degrees")
    right_knee_angle: Optional[float] = Field(None, ge=0, le=180, description="Right knee angle in degrees")


class AlignmentVector(BaseModel):
    """Alignment vector between two points."""
    dx: float = Field(..., description="X component of the vector")
    dy: float = Field(..., description="Y component of the vector")
    magnitude: float = Field(..., description="Magnitude of the vector")
    angle_degrees: float = Field(..., ge=0, le=360, description="Angle of the vector in degrees")


class AlignmentVectors(BaseModel):
    """Postural alignment vectors."""
    ear_to_shoulder: Optional[AlignmentVector] = None
    shoulder_to_hip: Optional[AlignmentVector] = None
    hip_to_knee: Optional[AlignmentVector] = None
    knee_to_ankle: Optional[AlignmentVector] = None


class Symmetry(BaseModel):
    """Symmetry analysis."""
    shoulder_height_diff: Optional[float] = Field(None, ge=0, le=1, description="Shoulder height difference")
    hip_height_diff: Optional[float] = Field(None, ge=0, le=1, description="Hip height difference")
    shoulder_width_ratio: Optional[float] = Field(None, ge=0, le=5, description="Shoulder width ratio")
    hip_width_ratio: Optional[float] = Field(None, ge=0, le=5, description="Hip width ratio")


class Metadata(BaseModel):
    """Analysis metadata."""
    video_id: str = Field(..., description="Unique video identifier")
    video_angle: VideoAngle = Field(..., description="Video angle")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")
    frame_count: Optional[int] = Field(None, description="Number of frames processed")
    user_height_cm: Optional[float] = Field(None, description="User height in cm")
    user_weight_kg: Optional[float] = Field(None, description="User weight in kg")
    user_age: Optional[int] = Field(None, description="User age")
    camera_distance_m: Optional[float] = Field(None, description="Camera distance in meters")


class VideoAnalysisResponse(BaseModel):
    """Response for single video analysis."""
    video_id: str = Field(..., description="Unique video identifier")
    video_angle: VideoAngle = Field(..., description="Video angle")
    thumbnail_path: Optional[str] = Field(None, description="Path to thumbnail image")
    thumbnail_base64: Optional[str] = Field(None, description="Base64 encoded thumbnail")
    landmarks: Landmarks = Field(..., description="Detected body landmarks")
    joint_angles: JointAngles = Field(..., description="Calculated joint angles")
    alignment_vectors: AlignmentVectors = Field(..., description="Postural alignment vectors")
    symmetry: Symmetry = Field(..., description="Symmetry analysis")
    metadata: Metadata = Field(..., description="Analysis metadata")


class MultiVideoAnalysisResponse(BaseModel):
    """Response for multiple video analysis."""
    analyses: List[VideoAnalysisResponse] = Field(..., description="List of video analyses")
    total_processing_time_ms: float = Field(..., description="Total processing time in milliseconds")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Health check timestamp")
    version: str = Field(..., description="Service version") 