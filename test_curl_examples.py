#!/usr/bin/env python3
"""
Test script with correct curl examples for the Posture Extractor API.
This demonstrates the proper way to send multiple video_angle parameters.
"""

import subprocess
import sys
import json

def test_health_endpoint():
    """Test the health endpoint."""
    print("🔍 Testing health endpoint...")
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:8000/api/v1/health"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Health endpoint working")
            print(f"Response: {result.stdout}")
        else:
            print("❌ Health endpoint failed")
            print(f"Error: {result.stderr}")
    except FileNotFoundError:
        print("❌ curl not found. Please install curl or use PowerShell/Invoke-WebRequest")

def print_curl_examples():
    """Print correct curl examples."""
    print("\n" + "="*80)
    print("📋 CORRECT CURL EXAMPLES FOR POSTURE EXTRACTOR API")
    print("="*80)
    
    print("\n🔧 SINGLE VIDEO ANALYSIS:")
    print("-" * 50)
    print("""curl -X 'POST' \\
  'http://localhost:8000/api/v1/analyze' \\
  -H 'accept: application/json' \\
  -H 'Content-Type: multipart/form-data' \\
  -F 'videos=@video.mp4' \\
  -F 'video_angle=front' \\
  -F 'user_height=175' \\
  -F 'user_weight=70' \\
  -F 'user_age=30'""")
    
    print("\n🔧 TWO VIDEO ANALYSIS:")
    print("-" * 50)
    print("""curl -X 'POST' \\
  'http://localhost:8000/api/v1/analyze' \\
  -H 'accept: application/json' \\
  -H 'Content-Type: multipart/form-data' \\
  -F 'videos=@front.mp4' \\
  -F 'videos=@left.mp4' \\
  -F 'video_angle=front,left' \\
  -F 'user_height=175'""")
    
    print("\n🔧 THREE VIDEO ANALYSIS:")
    print("-" * 50)
    print("""curl -X 'POST' \\
  'http://localhost:8000/api/v1/analyze' \\
  -H 'accept: application/json' \\
  -H 'Content-Type: multipart/form-data' \\
  -F 'videos=@IMG_1171.MOV' \\
  -F 'videos=@IMG_1172.MOV' \\
  -F 'videos=@IMG_1173.MOV' \\
  -F 'video_angle=front,right,left' \\
  -F 'user_height=178' \\
  -F 'user_weight=95' \\
  -F 'user_age=33' \\
  -F 'camera_distance=2'""")
    
    print("\n🔧 POWERSHELL EXAMPLE:")
    print("-" * 50)
    print("""$uri = "http://localhost:8000/api/v1/analyze"
$form = @{
    videos = @(
        Get-Item "IMG_1171.MOV",
        Get-Item "IMG_1172.MOV", 
        Get-Item "IMG_1173.MOV"
    )
    video_angle = "front,right,left"
    user_height = 178
    user_weight = 95
    user_age = 33
    camera_distance = 2
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form""")
    
    print("\n" + "="*80)
    print("✅ CORRECT (Comma-separated format):")
    print("="*80)
    print("""curl -X 'POST' \\
  'http://localhost:8000/api/v1/analyze' \\
  -H 'accept: application/json' \\
  -H 'Content-Type: multipart/form-data' \\
  -F 'videos=@IMG_1171.MOV' \\
  -F 'videos=@IMG_1172.MOV' \\
  -F 'videos=@IMG_1173.MOV' \\
  -F 'video_angle=front,right,left'  # ✅ CORRECT - comma-separated
  -F 'user_height=178' \\
  -F 'user_weight=95' \\
  -F 'user_age=33' \\
  -F 'camera_distance=2'""")

def main():
    """Main function."""
    print("🚀 Posture Extractor API - Curl Examples")
    print("=" * 50)
    
    # Test if service is running
    test_health_endpoint()
    
    # Print examples
    print_curl_examples()
    
    print("\n" + "="*80)
    print("💡 UPDATED API FORMAT:")
    print("="*80)
    print("The API now accepts video_angle as a comma-separated string,")
    print("which matches what Swagger UI generates automatically.")
    print("\nThis makes the API more user-friendly and eliminates the")
    print("confusion between the documentation and actual usage.")
    print("\nFormat: video_angle=front,right,left")
    print("The API will split this into individual angles automatically.")

if __name__ == "__main__":
    main() 