#!/usr/bin/env python3
"""
Startup script for Posture Extractor Microservice
"""

import uvicorn
import os
from pathlib import Path

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("static/thumbnails", exist_ok=True)
    
    print("🚀 Starting Posture Extractor Microservice...")
    print("📚 API Documentation will be available at: http://localhost:8000/docs")
    print("🔍 Health check: http://localhost:8000/api/v1/health")
    
    # Run the application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 