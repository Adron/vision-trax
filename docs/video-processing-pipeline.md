# Video Processing Pipeline for Activity Detection

This document describes how to build a processing pipeline for detecting specific activities in videos using the Vision Trax project.

## Overview

The pipeline uses YOLOv8 for object detection, combined with custom activity classification to identify:
- People loitering (standing or sitting)
- Specific activities (drinking, reading)
- Device usage (phone, computer)
- People in line at order counters

## Core Components

### 1. Basic Setup and Video Processing

```python
from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path

class ActivityDetector:
    def __init__(self):
        # Load YOLO model
        self.model = YOLO('yolov8n.pt')  # or a custom trained model
        
    def process_video(self, video_path):
        # Open video file
        cap = cv2.VideoCapture(str(video_path))
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # Run detection
            results = self.model(frame)
            
            # Process results
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get class and confidence
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    
                    # Process based on class
                    if cls == 0:  # person class
                        # Process person detection
                        self.process_person(box, frame)
                        
        cap.release()
```

### 2. Activity Detection

#### Loitering Detection
```python
def detect_loitering(self, person_tracks):
    # Track person position over time
    stationary_threshold = 30  # pixels
    time_threshold = 60  # frames (assuming 30fps = 2 seconds)
    
    stationary_frames = 0
    for i in range(1, len(person_tracks)):
        movement = np.linalg.norm(person_tracks[i] - person_tracks[i-1])
        if movement < stationary_threshold:
            stationary_frames += 1
        else:
            stationary_frames = 0
            
        if stationary_frames > time_threshold:
            return True
    return False
```

#### Activity Classification
```python
def classify_activity(self, frame, person_box):
    # Extract person region
    x1, y1, x2, y2 = person_box.xyxy[0]
    person_region = frame[int(y1):int(y2), int(x1):int(x2)]
    
    # Detect objects in person's region
    objects = self.model(person_region)
    
    # Check for specific objects
    has_phone = any(obj.cls == 67 for obj in objects)  # cell phone class
    has_computer = any(obj.cls == 63 for obj in objects)  # laptop class
    
    # Detect pose
    pose = self.pose_model(person_region)
    
    return {
        'has_phone': has_phone,
        'has_computer': has_computer,
        'is_sitting': self.is_sitting(pose),
        'is_standing': self.is_standing(pose)
    }
```

### 3. Line Detection
```python
def detect_line(self, frame):
    # Detect people
    results = self.model(frame)
    people = [box for box in results.boxes if box.cls == 0]
    
    # Group people by proximity
    line_groups = self.group_by_proximity(people)
    
    # Check if any group forms a line
    for group in line_groups:
        if self.is_line_formation(group):
            return True
    return False
```

## Integration with CVAT

The project includes CVAT integration for annotation and training:

```python
from cvat_sdk import make_client

def train_custom_model(self, annotated_data):
    # Upload annotated data to CVAT
    client = make_client()
    task = client.tasks.create_from_data(
        spec={
            'name': 'Activity Detection',
            'labels': [
                {'name': 'person_standing'},
                {'name': 'person_sitting'},
                {'name': 'person_with_phone'},
                {'name': 'person_in_line'}
            ]
        }
    )
    
    # Train custom model
    model = YOLO('yolov8n.pt')
    model.train(data='custom_dataset.yaml', epochs=100)
```

## Usage Example

```python
detector = ActivityDetector()

# Process a video
results = detector.process_video('input_video.mp4')

# Get specific detections
loitering_people = detector.get_loitering_detections()
people_with_phones = detector.get_phone_usage_detections()
people_in_line = detector.get_line_detections()
```

## Dependencies

The pipeline relies on several key dependencies:
- YOLOv8 (ultralytics) for object detection
- OpenCV (opencv-python) for video processing
- PyTorch (torch) for deep learning operations
- CVAT SDK for annotation and training data management
- MoviePy for video manipulation
- FFmpeg for video format handling

## Extending the Pipeline

The system can be extended by:
1. Adding more specific activity classifiers
2. Implementing temporal analysis for better activity detection
3. Adding custom object detection for specific items
4. Implementing tracking to follow people across frames
5. Adding pose estimation for better activity classification

## Best Practices

1. **Data Collection**
   - Collect diverse video samples
   - Include various lighting conditions
   - Capture different angles and perspectives

2. **Model Training**
   - Use transfer learning from pre-trained models
   - Implement data augmentation
   - Regular validation during training

3. **Performance Optimization**
   - Use GPU acceleration when available
   - Implement batch processing
   - Optimize frame sampling rate

4. **Error Handling**
   - Implement robust error checking
   - Add logging for debugging
   - Handle edge cases gracefully 