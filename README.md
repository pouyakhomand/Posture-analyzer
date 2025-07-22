# Posture Extractor Microservice

A Python-based microservice for extracting posture-related features from videos using MediaPipe pose estimation.

## Overview

The Posture Extractor Microservice analyzes posture-related data from videos captured from multiple angles (front, left, right, back). It extracts critical posture-relevant features and returns structured output that can be consumed by downstream services such as posture assessment, risk analysis, or LLM-based evaluators.

**Note**: This microservice is strictly for feature extraction, not for posture classification or disease diagnosis.

## Features

- **Multi-angle video support**: front, left, right, back
- **Pose estimation**: Using MediaPipe for accurate landmark detection
- **Joint angle calculations**: Neck, spine, shoulder, hip, knee, ankle angles
- **Alignment vectors**: Ear-to-shoulder, shoulder-to-hip alignments
- **Symmetry analysis**: Shoulder and hip height differences
- **Thumbnail generation**: Representative frames from videos
- **Structured JSON output**: Comprehensive posture data

## API Endpoints

- `POST /analyze` - Analyze posture from video(s)
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

## Installation

### Option 1: Using Python 3.12 with MediaPipe (Recommended)

1. Clone the repository:

```bash
git clone <repository-url>
cd posture-extractor-service
```

2. Install Python 3.12 (if not already installed):

```bash
# On Windows using winget:
winget install Python.Python.3.12

# Or download from: https://www.python.org/downloads/
```

3. Create a virtual environment with Python 3.12:

```bash
py -3.12 -m venv venv312
```

4. Activate the virtual environment:

```bash
# On Windows:
venv312\Scripts\activate
# or use the provided script:
activate_venv.bat
# or for PowerShell:
.\activate_venv.ps1

# On macOS/Linux:
source venv312/bin/activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

### Option 2: Using Python 3.13 (Mock Mode)

If you're using Python 3.13, MediaPipe is not available. The service will run in mock mode:

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies (MediaPipe will be skipped):

```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

1. **Activate the virtual environment:**

   ```bash
   # Windows Command Prompt:
   activate_venv.bat

   # PowerShell:
   .\activate_venv.ps1

   # Manual activation:
   venv312\Scripts\activate
   ```

2. **Start the service:**

   ```bash
   python start.py
   # or
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the API:**
   - **Health Check**: http://localhost:8000/api/v1/health
   - **API Documentation**: http://localhost:8000/docs
   - **Root Endpoint**: http://localhost:8000/

### API Usage

#### Single Video Analysis

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "videos=@video.mp4" \
  -F "video_angle=front" \
  -F "user_height=175" \
  -F "user_weight=70" \
  -F "user_age=30"
```

#### Multiple Video Analysis

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "videos=@front.mp4" \
  -F "videos=@left.mp4" \
  -F "videos=@right.mp4" \
  -F "video_angle=front,left,right" \
  -F "user_height=175"
```

**Important**: Send video_angle as a comma-separated string (e.g., `front,left,right`).

#### PowerShell Example

```powershell
$uri = "http://localhost:8000/api/v1/analyze"
$form = @{
    videos = Get-Item "video.mp4"
    video_angle = "front"
    user_height = "175"
    user_weight = "70"
    user_age = "30"
}
Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

### Testing the Installation

Run the test scripts to verify everything is working:

```bash
# Test package installation and MediaPipe
python test_installation.py

# Test application modules and functionality
python test_app.py
```

## Project Structure

```
posture-extractor-service/
├── venv312/                    # Python 3.12 virtual environment
├── app/
│   ├── main.py                 # FastAPI application
│   ├── api/
│   │   └── routes.py           # API endpoints
│   ├── core/
│   │   └── config.py           # Configuration
│   ├── models/
│   │   └── response.py         # Response models
│   ├── services/
│   │   ├── pose_estimator.py   # MediaPipe integration
│   │   ├── angle_calculator.py # Joint angle calculations
│   │   └── thumbnail_generator.py # Thumbnail creation
│   └── utils/
│       └── geometry.py         # Geometric calculations
├── static/
│   └── thumbnails/             # Generated thumbnails
├── activate_venv.bat           # Windows activation script
├── activate_venv.ps1           # PowerShell activation script
├── test_installation.py        # Installation test script
├── test_app.py                 # Application test script
├── start.py                    # Startup script
├── requirements.txt            # Dependencies (includes MediaPipe)
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose setup
├── .gitignore                  # Git ignore rules
├── SETUP.md                    # Setup instructions
└── README.md                   # This file
```

## Current Status

✅ **Fully Operational with Python 3.12 and MediaPipe**

- **Python 3.12**: Active virtual environment with all dependencies
- **MediaPipe 0.10.21**: Real pose estimation working
- **FastAPI**: Service running and responding
- **All Tests**: Passing (5/5 tests successful)
- **API Endpoints**: All functional and documented

### Key Features Available

1. **Real Pose Estimation**: Using MediaPipe for accurate landmark detection
2. **Joint Angle Calculations**: Mathematical calculations for posture analysis
3. **Alignment Vectors**: Postural alignment measurements
4. **Symmetry Analysis**: Left-right symmetry calculations
5. **Thumbnail Generation**: Representative frames with landmark visualization
6. **Multi-angle Support**: Front, left, right, back video analysis
7. **Structured JSON Output**: Comprehensive posture data

## Configuration

The service can be configured using environment variables:

- `MAX_FILE_SIZE`: Maximum file size in bytes (default: 100MB)
- `ALLOWED_EXTENSIONS`: Comma-separated list of allowed video extensions
- `THUMBNAIL_QUALITY`: JPEG quality for thumbnails (default: 85)

## Testing

### Automated Tests

Run the provided test scripts to verify installation and functionality:

```bash
# Test package installation and MediaPipe
python test_installation.py

# Test application modules and functionality
python test_app.py
```

### Manual Testing

Test the API endpoints:

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Root endpoint
curl http://localhost:8000/

# API documentation
# Open http://localhost:8000/docs in your browser
```

## Troubleshooting

### Common Issues

1. **MediaPipe Import Error**:

   - Ensure you're using Python 3.12 (not 3.13)
   - Activate the virtual environment: `venv312\Scripts\activate`
   - Reinstall dependencies: `pip install -r requirements.txt`

2. **Service Won't Start**:

   - Check if port 8000 is available
   - Ensure virtual environment is activated
   - Verify all dependencies are installed

3. **Video Processing Errors**:

   - Check video format (MP4, AVI, MOV supported)
   - Ensure video file is not corrupted
   - Verify file size is within limits (100MB default)

4. **Memory Issues**:
   - Close other applications using GPU
   - Reduce video resolution if needed
   - Restart the service

### Getting Help

- Check the API documentation at http://localhost:8000/docs
- Review the test output for specific error messages
- Ensure all dependencies are correctly installed

## Docker Deployment

```bash
docker-compose up -d
```

## Output Format

The service returns structured JSON with comprehensive posture analysis:

### Response Structure

```json
{
  "status": "success",
  "data": {
    "landmarks": {
      "nose": { "x": 100, "y": 200 },
      "left_shoulder": { "x": 80, "y": 180 },
      "right_shoulder": { "x": 120, "y": 180 }
      // ... 33 MediaPipe landmarks
    },
    "joint_angles": {
      "neck_angle": 15.2,
      "spine_angle": 2.1,
      "left_shoulder_angle": 85.3,
      "right_shoulder_angle": 87.1,
      "left_hip_angle": 175.8,
      "right_hip_angle": 176.2,
      "left_knee_angle": 165.4,
      "right_knee_angle": 166.1,
      "left_ankle_angle": 85.2,
      "right_ankle_angle": 84.8
    },
    "alignment_vectors": {
      "ear_to_shoulder": { "dx": 0.1, "dy": 0.05 },
      "shoulder_to_hip": { "dx": 0.02, "dy": 0.01 },
      "hip_to_knee": { "dx": 0.03, "dy": 0.02 }
    },
    "symmetry": {
      "shoulder_height_diff": 0.8,
      "hip_height_diff": 0.3,
      "overall_symmetry_score": 0.92
    },
    "metadata": {
      "user_height": 175,
      "user_weight": 70,
      "user_age": 30,
      "video_angle": "front",
      "processing_time": 2.34,
      "frames_processed": 150
    },
    "thumbnail": "base64_encoded_image_data"
  }
}
```

### Key Components

- **Landmarks**: 2D coordinates of 33 MediaPipe body keypoints
- **Joint angles**: Calculated angles between body segments (degrees)
- **Alignment vectors**: Postural alignment measurements (normalized)
- **Symmetry**: Left-right symmetry analysis and scoring
- **Metadata**: User information and processing details
- **Thumbnail**: Base64 encoded representative frame with landmarks drawn

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
