from fastapi import HTTPException, status


class PostureExtractorException(Exception):
    """Base exception for posture extractor."""
    pass


class VideoProcessingError(PostureExtractorException):
    """Raised when video processing fails."""
    pass


class InvalidVideoFormatError(PostureExtractorException):
    """Raised when video format is not supported."""
    pass


class PoseDetectionError(PostureExtractorException):
    """Raised when pose detection fails."""
    pass


class FileTooLargeError(PostureExtractorException):
    """Raised when uploaded file exceeds size limit."""
    pass


def raise_video_processing_error(message: str):
    """Raise HTTP exception for video processing errors."""
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=f"Video processing error: {message}"
    )


def raise_invalid_format_error():
    """Raise HTTP exception for invalid video format."""
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid video format. Supported formats: MP4, MOV, AVI, MKV"
    )


def raise_file_too_large_error():
    """Raise HTTP exception for file too large."""
    raise HTTPException(
        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        detail="File too large. Maximum size is 100MB"
    ) 