# Project Dependencies

This document describes each dependency used in the Vision Trax project and its purpose.

## Core Dependencies

### numpy (>=1.21.0)
- **Purpose**: Fundamental package for scientific computing in Python
- **Use in Project**: 
  - Array operations and numerical computations
  - Data manipulation for image processing
  - Integration with other scientific computing libraries

### opencv-python (>=4.5.3)
- **Purpose**: Computer vision library for image and video processing
- **Use in Project**:
  - Video file reading and writing
  - Image processing operations
  - Frame extraction and manipulation
  - Basic computer vision operations

### torch (>=1.9.0)
- **Purpose**: Deep learning framework
- **Use in Project**:
  - GPU acceleration for YOLO model
  - Tensor operations
  - Neural network computations

### torchvision (>=0.10.0)
- **Purpose**: Computer vision utilities for PyTorch
- **Use in Project**:
  - Image transformations
  - Dataset handling
  - Model utilities

## YOLO Dependencies

### ultralytics (>=8.0.0)
- **Purpose**: YOLOv8 implementation
- **Use in Project**:
  - Object detection in videos
  - Model loading and inference
  - Pre-trained model access

## CVAT Integration

### cvat-sdk (>=2.0.0)
- **Purpose**: Python SDK for CVAT (Computer Vision Annotation Tool)
- **Use in Project**:
  - Video upload to CVAT
  - Annotation export
  - Task management
  - API integration

## Video Processing

### moviepy (>=1.0.3)
- **Purpose**: Video editing library
- **Use in Project**:
  - Video file manipulation
  - Frame extraction
  - Video composition

### ffmpeg-python (>=0.2.0)
- **Purpose**: Python bindings for FFmpeg
- **Use in Project**:
  - Video format conversion
  - Video compression
  - Stream handling

## Utilities

### tqdm (>=4.62.0)
- **Purpose**: Progress bar library
- **Use in Project**:
  - Progress tracking for long operations
  - User feedback during processing

### PyYAML (>=6.0)
- **Purpose**: YAML parser and emitter
- **Use in Project**:
  - Configuration file handling
  - Model parameter storage

### python-dotenv (>=0.19.0)
- **Purpose**: Environment variable management
- **Use in Project**:
  - Secure credential management
  - Configuration loading

### requests (>=2.26.0)
- **Purpose**: HTTP library
- **Use in Project**:
  - API communication
  - File downloads
  - Web requests

## Development Dependencies

### pytest (>=6.2.5)
- **Purpose**: Testing framework
- **Use in Project**:
  - Unit testing
  - Integration testing
  - Test automation

### black (>=21.9b0)
- **Purpose**: Code formatter
- **Use in Project**:
  - Code style enforcement
  - Consistent formatting

### flake8 (>=3.9.2)
- **Purpose**: Code linter
- **Use in Project**:
  - Code quality checks
  - Style guide enforcement
  - Error detection 