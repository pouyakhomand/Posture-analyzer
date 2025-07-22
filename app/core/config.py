import os
from typing import List
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Posture Extractor Microservice"
    
    # File Upload Settings
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: List[str] = [".mp4", ".mov", ".avi", ".mkv"]
    UPLOAD_DIR: str = "uploads"
    
    # Thumbnail Settings
    THUMBNAIL_QUALITY: int = 85
    THUMBNAIL_DIR: str = "static/thumbnails"
    
    # MediaPipe Settings
    MIN_DETECTION_CONFIDENCE: float = 0.5
    MIN_TRACKING_CONFIDENCE: float = 0.5
    
    # Processing Settings
    FRAME_SAMPLE_RATE: int = 30  # Process every 30th frame
    MIN_FRAMES_FOR_ANALYSIS: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 