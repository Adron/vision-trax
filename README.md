# Vision Trax

A computer vision project for video analysis using YOLO and CVAT integration.

## Project Structure

```
vision-trax/
├── docs/           # Documentation and guides
├── experiments/    # Experimental results and configurations
├── videos/         # Input video files for processing
└── src/           # Source code
```

## Documentation

- [Software Architecture](docs/software-architecture.md) - UML diagrams and component descriptions
- [Application Process Flow](docs/application-flow.md) - Detailed explanation of the application workflow and model training process
- [Video Processing Pipeline](docs/video-processing-pipeline.md) - Guide to the video processing pipeline implementation
- [Dependencies](docs/dependency-descriptions.md) - Description of project dependencies and their purposes
- [Server Operations](docs/server-operations.md) - Comprehensive guide for deploying and operating on GPU-enabled servers with multiple processors
- [SSH Setup and File Sharing](docs/ssh-setup-and-file-sharing.md) - Guide for setting up SSH access with private PEM keys and configuring Samba file sharing for Windows/macOS integration

## Setup

1. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your video files in the `videos/` directory
2. Run the video processing script:
```bash
python src/process_videos.py
```

## Features

- Video processing with YOLO object detection
- CVAT integration for video labeling
- Custom video analysis pipelines
- Experiment tracking and results storage

## Requirements

- Python 3.8+
- CUDA-capable GPU (recommended)
- CVAT account and API access 