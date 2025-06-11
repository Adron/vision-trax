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