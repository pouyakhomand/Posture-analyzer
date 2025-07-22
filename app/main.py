from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
import os
from pathlib import Path

from .core.config import settings
from .api.routes import router
from .core.exceptions import PostureExtractorException

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A microservice for extracting posture-related features from videos using MediaPipe pose estimation.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for thumbnails
static_dir = Path(settings.THUMBNAIL_DIR)
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["posture-analysis"])


def custom_openapi():
    """Custom OpenAPI schema with better multipart form documentation."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add custom documentation for the analyze endpoint
    if "/api/v1/analyze" in openapi_schema["paths"]:
        analyze_path = openapi_schema["paths"]["/api/v1/analyze"]
        if "post" in analyze_path:
            post_op = analyze_path["post"]
            
            # Add better description for video_angle parameter
            for param in post_op.get("parameters", []):
                if param.get("name") == "video_angle":
                    param["description"] = (
                        "Angle for each video. **IMPORTANT**: Send as separate form fields, not comma-separated. "
                        "Example: For 3 videos, send: video_angle=front&video_angle=right&video_angle=left"
                    )
                    break
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.exception_handler(PostureExtractorException)
async def posture_extractor_exception_handler(request, exc):
    """Handle custom exceptions."""
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": settings.PROJECT_NAME,
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/api/v1/health",
            "analyze": "/api/v1/analyze",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    # Create necessary directories
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.THUMBNAIL_DIR, exist_ok=True)
    
    print(f"🚀 {settings.PROJECT_NAME} started successfully!")
    print(f"📁 Upload directory: {settings.UPLOAD_DIR}")
    print(f"🖼️  Thumbnail directory: {settings.THUMBNAIL_DIR}")
    print(f"📚 API Documentation: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    print(f"🛑 {settings.PROJECT_NAME} shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 