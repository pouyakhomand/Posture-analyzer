from typing import List, Optional
from pydantic import BaseModel, Field, validator
from enum import Enum


class VideoAngle(str, Enum):
    """Supported video angles."""
    FRONT = "front"
    LEFT = "left"
    RIGHT = "right"
    BACK = "back"


class UserMetadata(BaseModel):
    """User metadata for analysis."""
    height_cm: Optional[float] = Field(None, ge=50, le=250, description="User height in cm")
    weight_kg: Optional[float] = Field(None, ge=20, le=300, description="User weight in kg")
    age: Optional[int] = Field(None, ge=1, le=120, description="User age")
    camera_distance_m: Optional[float] = Field(None, ge=0.5, le=10.0, description="Camera distance in meters")


class VideoAnalysisRequest(BaseModel):
    """Request model for single video analysis."""
    video_angle: VideoAngle = Field(..., description="Angle of the video")
    user_metadata: Optional[UserMetadata] = Field(None, description="User metadata")
    
    @validator('video_angle')
    def validate_video_angle(cls, v):
        if v not in VideoAngle:
            raise ValueError(f"Invalid video angle. Must be one of: {list(VideoAngle)}")
        return v


class MultiVideoAnalysisRequest(BaseModel):
    """Request model for multiple video analysis."""
    videos: List[VideoAnalysisRequest] = Field(..., min_items=1, max_items=4, description="List of videos to analyze")
    
    @validator('videos')
    def validate_unique_angles(cls, v):
        angles = [video.video_angle for video in v]
        if len(angles) != len(set(angles)):
            raise ValueError("Each video must have a unique angle")
        return v 