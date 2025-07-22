import os
import uuid
import base64
from typing import Optional, Tuple
from pathlib import Path
from fastapi import UploadFile
from ..core.config import settings
from ..core.exceptions import raise_invalid_format_error, raise_file_too_large_error


def validate_video_file(file: UploadFile) -> None:
    """Validate uploaded video file."""
    # Check file extension
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise_invalid_format_error()
    
    # Check file size (if available)
    if hasattr(file, 'size') and file.size and file.size > settings.MAX_FILE_SIZE:
        raise_file_too_large_error()


def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename for uploaded files."""
    file_extension = Path(original_filename).suffix
    unique_id = str(uuid.uuid4())
    return f"{unique_id}{file_extension}"


def save_uploaded_file(file: UploadFile, filename: str) -> str:
    """Save uploaded file to disk."""
    # Create upload directory if it doesn't exist
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(exist_ok=True)
    
    # Save file
    file_path = upload_dir / filename
    with open(file_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    return str(file_path)


def ensure_thumbnail_directory() -> Path:
    """Ensure thumbnail directory exists."""
    thumbnail_dir = Path(settings.THUMBNAIL_DIR)
    thumbnail_dir.mkdir(parents=True, exist_ok=True)
    return thumbnail_dir


def save_thumbnail(image_data: bytes, filename: str) -> str:
    """Save thumbnail image to disk."""
    thumbnail_dir = ensure_thumbnail_directory()
    thumbnail_path = thumbnail_dir / filename
    
    with open(thumbnail_path, "wb") as f:
        f.write(image_data)
    
    return str(thumbnail_path)


def encode_image_to_base64(image_path: str) -> Optional[str]:
    """Encode image to base64 string."""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string
    except Exception:
        return None


def get_file_info(file_path: str) -> Tuple[int, int, float]:
    """Get basic file information."""
    try:
        stat = os.stat(file_path)
        file_size = stat.st_size
        creation_time = stat.st_ctime
        modification_time = stat.st_mtime
        return file_size, creation_time, modification_time
    except Exception:
        return 0, 0, 0


def cleanup_temp_files(file_paths: list) -> None:
    """Clean up temporary files."""
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass  # Ignore cleanup errors


def is_valid_video_format(filename: str) -> bool:
    """Check if filename has valid video extension."""
    return Path(filename).suffix.lower() in settings.ALLOWED_EXTENSIONS


def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return Path(filename).suffix.lower()


def create_temp_file_path(extension: str = ".mp4") -> str:
    """Create a temporary file path."""
    unique_id = str(uuid.uuid4())
    temp_dir = Path(settings.UPLOAD_DIR)
    temp_dir.mkdir(exist_ok=True)
    return str(temp_dir / f"temp_{unique_id}{extension}")


def get_relative_path(absolute_path: str, base_dir: str) -> str:
    """Get relative path from absolute path."""
    try:
        return os.path.relpath(absolute_path, base_dir)
    except ValueError:
        return absolute_path 