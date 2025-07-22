# Posture Extractor Microservice - Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Test Installation

```bash
python test_installation.py
```

### 3. Start the Service

```bash
# Option 1: Using the startup script
python start.py

# Option 2: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the Service

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **Root Endpoint**: http://localhost:8000/

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### Using Docker directly

```bash
# Build the image
docker build -t posture-extractor .

# Run the container
docker run -p 8000:8000 -v $(pwd)/uploads:/app/uploads -v $(pwd)/static:/app/static posture-extractor
```

## API Usage

### Single Video Analysis

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "videos=@video.mp4" \
  -F "video_angle=front" \
  -F "user_height=175" \
  -F "user_weight=70" \
  -F "user_age=30"
```

### Multiple Video Analysis

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "videos=@front.mp4" \
  -F "videos=@left.mp4" \
  -F "video_angle=front" \
  -F "video_angle=left" \
  -F "user_height=175"
```

## Testing

### Run Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Manual Testing

1. Start the service
2. Open http://localhost:8000/docs
3. Use the interactive API documentation to test endpoints
4. Upload a test video file

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
MAX_FILE_SIZE=104857600
THUMBNAIL_QUALITY=85
MIN_DETECTION_CONFIDENCE=0.5
MIN_TRACKING_CONFIDENCE=0.5
FRAME_SAMPLE_RATE=30
```

### Supported Video Formats

- MP4
- MOV
- AVI
- MKV

### File Size Limits

- Default: 100MB per video
- Configurable via `MAX_FILE_SIZE` environment variable

## Troubleshooting

### Common Issues

1. **MediaPipe Import Error**

   - Ensure you have Python 3.8+ installed
   - Reinstall MediaPipe: `pip install --upgrade mediapipe`

2. **OpenCV Import Error**

   - Install system dependencies (see Dockerfile for reference)
   - On Ubuntu: `sudo apt-get install libgl1-mesa-glx libglib2.0-0`

3. **Port Already in Use**

   - Change port: `uvicorn app.main:app --port 8001`
   - Or kill existing process: `lsof -ti:8000 | xargs kill -9`

4. **Permission Errors**
   - Ensure write permissions for `uploads/` and `static/thumbnails/` directories

### Logs

Check logs for detailed error information:

```bash
# If using uvicorn directly
uvicorn app.main:app --log-level debug

# If using Docker
docker-compose logs -f
```

## Development

### Project Structure

```
posture-extractor-service/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── api/routes.py           # API endpoints
│   ├── core/                   # Configuration and exceptions
│   ├── models/                 # Pydantic models
│   ├── services/               # Business logic
│   └── utils/                  # Utility functions
├── static/thumbnails/          # Generated thumbnails
├── tests/                      # Test files
├── uploads/                    # Temporary video storage
└── requirements.txt            # Dependencies
```

### Adding New Features

1. Create new service in `app/services/`
2. Add corresponding tests in `tests/`
3. Update API routes in `app/api/routes.py`
4. Update documentation

## Production Deployment

### Security Considerations

1. Configure CORS properly for production
2. Set up proper authentication/authorization
3. Use HTTPS in production
4. Configure rate limiting
5. Set up proper logging and monitoring

### Performance Optimization

1. Use GPU acceleration for MediaPipe (if available)
2. Implement caching for repeated requests
3. Use async processing for large videos
4. Consider using a CDN for thumbnail storage

### Monitoring

1. Set up health checks
2. Monitor API response times
3. Track error rates
4. Monitor disk usage for uploads/thumbnails
