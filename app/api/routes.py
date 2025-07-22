import time
import uuid
from typing import List
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from ..core.config import settings
from ..core.exceptions import raise_video_processing_error
from ..models.request import VideoAngle, UserMetadata
from ..models.response import (
    VideoAnalysisResponse, MultiVideoAnalysisResponse, HealthResponse,
    Metadata
)
from ..services.pose_estimator import PoseEstimator
from ..services.angle_calculator import AngleCalculator
from ..services.thumbnail_generator import ThumbnailGenerator
from ..utils.file_utils import (
    validate_video_file, generate_unique_filename, save_uploaded_file,
    cleanup_temp_files
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0"
    )


@router.post("/analyze", response_model=MultiVideoAnalysisResponse)
async def analyze_posture(
    videos: List[UploadFile] = File(..., description="Video files to analyze (MP4, MOV, AVI, MKV)"),
    video_angle: str = Form(..., description="Comma-separated angles for each video (e.g., 'front,right,left')"),
    user_height: float = Form(None, description="User height in cm"),
    user_weight: float = Form(None, description="User weight in kg"),
    user_age: int = Form(None, description="User age"),
    camera_distance: float = Form(None, description="Camera distance in meters")
):
    """
    Analyze posture from uploaded videos.
    
    **Important**: Send video_angle as a comma-separated string:
    - For 1 video: `video_angle=front`
    - For 2 videos: `video_angle=front,left`
    - For 3 videos: `video_angle=front,right,left`
    
    **Parameters**:
    - **videos**: List of video files (MP4, MOV, AVI, MKV)
    - **video_angle**: Comma-separated angles for each video (front, left, right, back)
    - **user_height**: User height in centimeters (optional)
    - **user_weight**: User weight in kilograms (optional)
    - **user_age**: User age (optional)
    - **camera_distance**: Camera distance in meters (optional)
    
    **Valid angles**: front, left, right, back
    **Maximum videos**: 4
    """
    start_time = time.time()
    
    # Split video_angle string into list
    video_angles = [angle.strip() for angle in video_angle.split(',')]
    
    # Validate input
    if len(videos) != len(video_angles):
        raise HTTPException(
            status_code=400,
            detail="Number of videos must match number of video angles: " + str(len(videos)) + " != " + str(len(video_angles))
        )
    
    if len(videos) == 0:
        raise HTTPException(
            status_code=400,
            detail="At least one video must be provided"
        )
    
    if len(videos) > 4:
        raise HTTPException(
            status_code=400,
            detail="Maximum 4 videos allowed per request"
        )
    
    # Validate video angles
    valid_angles = [angle.value for angle in VideoAngle]
    for angle in video_angles:
        if angle not in valid_angles:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid video angle: {angle}. Valid angles: {valid_angles}"
            )
    
    # Check for duplicate angles
    if len(set(video_angles)) != len(video_angles):
        raise HTTPException(
            status_code=400,
            detail="Each video must have a unique angle"
        )
    
    # Initialize services
    pose_estimator = PoseEstimator()
    angle_calculator = AngleCalculator()
    thumbnail_generator = ThumbnailGenerator()
    
    analyses = []
    temp_files = []
    
    try:
        # Process each video
        for i, (video_file, angle) in enumerate(zip(videos, video_angles)):
            # Validate video file
            validate_video_file(video_file)
            
            # Generate unique filename and save file
            filename = generate_unique_filename(video_file.filename)
            video_path = save_uploaded_file(video_file, filename)
            temp_files.append(video_path)
            
            # Create user metadata
            user_metadata = UserMetadata(
                height_cm=user_height,
                weight_kg=user_weight,
                age=user_age,
                camera_distance_m=camera_distance
            )
            
            # Process video
            analysis = await _process_single_video(
                video_path=video_path,
                video_angle=VideoAngle(angle),
                user_metadata=user_metadata,
                pose_estimator=pose_estimator,
                angle_calculator=angle_calculator,
                thumbnail_generator=thumbnail_generator
            )
            
            analyses.append(analysis)
    
    except Exception as e:
        # Clean up temporary files
        cleanup_temp_files(temp_files)
        raise_video_processing_error(str(e))
    
    finally:
        # Clean up temporary files
        cleanup_temp_files(temp_files)
    
    # Calculate total processing time
    total_processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    return MultiVideoAnalysisResponse(
        analyses=analyses,
        total_processing_time_ms=total_processing_time
    )


async def _process_single_video(
    video_path: str,
    video_angle: VideoAngle,
    user_metadata: UserMetadata,
    pose_estimator: PoseEstimator,
    angle_calculator: AngleCalculator,
    thumbnail_generator: ThumbnailGenerator
) -> VideoAnalysisResponse:
    """Process a single video and return analysis results."""
    video_id = str(uuid.uuid4())
    
    # Extract landmarks from video
    landmarks_list, frame_count = pose_estimator.process_video(video_path)
    
    # Get average landmarks
    landmarks = pose_estimator.get_average_landmarks(landmarks_list)
    
    # Validate pose detection
    if not pose_estimator.validate_pose_detection(landmarks):
        raise_video_processing_error("Insufficient pose detection quality")
    
    # Calculate joint angles
    joint_angles = angle_calculator.calculate_joint_angles(landmarks)
    
    # Calculate alignment vectors
    alignment_vectors = angle_calculator.calculate_alignment_vectors(landmarks)
    
    # Calculate symmetry
    symmetry = angle_calculator.calculate_symmetry(landmarks)
    
    # Generate thumbnail
    thumbnail_path, thumbnail_base64 = thumbnail_generator.generate_thumbnail(
        video_path, landmarks
    )
    
    # Create metadata
    metadata = Metadata(
        video_id=video_id,
        video_angle=video_angle,
        frame_count=frame_count,
        user_height_cm=user_metadata.height_cm,
        user_weight_kg=user_metadata.weight_kg,
        user_age=user_metadata.age,
        camera_distance_m=user_metadata.camera_distance_m
    )
    
    return VideoAnalysisResponse(
        video_id=video_id,
        video_angle=video_angle,
        thumbnail_path=thumbnail_path,
        thumbnail_base64=thumbnail_base64,
        landmarks=landmarks,
        joint_angles=joint_angles,
        alignment_vectors=alignment_vectors,
        symmetry=symmetry,
        metadata=metadata
    ) 