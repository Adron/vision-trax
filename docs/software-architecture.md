# Vision Trax Software Architecture

This document outlines the software architecture of Vision Trax using UML diagrams to illustrate the key components and their relationships.

## Class Diagram

```mermaid
classDiagram
    class VideoProcessor {
        -YOLO model
        -PoseEstimator pose_model
        -ActivityClassifier activity_classifier
        +process_video(video_path)
        +process_frame(frame)
        -extract_frames(video)
        -detect_objects(frame)
    }

    class ActivityDetector {
        -float stationary_threshold
        -int time_threshold
        +detect_loitering(person_tracks)
        +classify_activity(frame, person_box)
        +detect_line(frame)
        -is_sitting(pose)
        -is_standing(pose)
    }

    class CVATClient {
        -str host
        -str username
        -str password
        +create_task(name, labels)
        +upload_video(task_id, video_path)
        +export_annotations(task_id, output_path)
        -authenticate()
    }

    class ModelTrainer {
        -YOLO base_model
        -dict training_config
        +train_model(dataset_path)
        +validate_model(test_data)
        +export_model(output_path)
        -prepare_dataset()
        -optimize_model()
    }

    class ResultAggregator {
        -list activity_logs
        -dict statistics
        +add_activity(activity_data)
        +generate_report()
        +export_results(format)
        -calculate_statistics()
    }

    VideoProcessor --> ActivityDetector : uses
    VideoProcessor --> CVATClient : uses
    VideoProcessor --> ResultAggregator : uses
    ModelTrainer --> CVATClient : uses
```

## Component Diagram

```mermaid
graph TB
    subgraph Frontend
        UI[User Interface]
        API[API Layer]
    end

    subgraph Core
        VP[Video Processor]
        AD[Activity Detector]
        RA[Result Aggregator]
    end

    subgraph External
        CVAT[CVAT Service]
        YOLO[YOLO Model]
        DB[(Database)]
    end

    subgraph Training
        MT[Model Trainer]
        DS[Dataset Manager]
    end

    UI --> API
    API --> VP
    VP --> AD
    AD --> YOLO
    VP --> CVAT
    VP --> RA
    RA --> DB
    MT --> CVAT
    MT --> DS
    DS --> DB
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant VP as VideoProcessor
    participant AD as ActivityDetector
    participant YOLO
    participant CVAT
    participant RA as ResultAggregator

    User->>VP: process_video(video_path)
    VP->>VP: extract_frames()
    loop Each Frame
        VP->>YOLO: detect_objects(frame)
        YOLO-->>VP: detection_results
        VP->>AD: classify_activity(frame, detections)
        AD->>AD: analyze_pose()
        AD->>AD: detect_loitering()
        AD-->>VP: activity_results
        VP->>RA: add_activity(activity_data)
    end
    VP->>CVAT: export_annotations()
    VP->>RA: generate_report()
    RA-->>User: final_results
```

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: Start Video
    Processing --> Detecting: Frame Ready
    Detecting --> Classifying: Objects Found
    Classifying --> Aggregating: Activities Classified
    Aggregating --> Processing: Next Frame
    Processing --> [*]: Video Complete
    Processing --> Error: Exception
    Error --> Idle: Reset
```

## Key Components Description

### 1. VideoProcessor
- Main orchestrator of the video processing pipeline
- Manages frame extraction and processing
- Coordinates between different components

### 2. ActivityDetector
- Handles activity classification
- Manages loitering detection
- Processes pose estimation

### 3. CVATClient
- Manages communication with CVAT service
- Handles video upload and annotation export
- Manages authentication and session

### 4. ModelTrainer
- Handles model training and optimization
- Manages dataset preparation
- Controls model validation and export

### 5. ResultAggregator
- Collects and processes activity data
- Generates reports and statistics
- Manages data export

## Data Flow

1. **Input Processing**
   - Video file ingestion
   - Frame extraction
   - Preprocessing

2. **Detection Pipeline**
   - Object detection
   - Activity classification
   - Pose estimation

3. **Result Processing**
   - Data aggregation
   - Statistical analysis
   - Report generation

4. **Output Generation**
   - JSON/CSV export
   - Visualization
   - API responses

## Integration Points

### External Services
- CVAT for annotation
- YOLO for object detection
- Database for storage

### Internal Components
- Activity detection
- Result aggregation
- Model training

## Error Handling

1. **Video Processing**
   - Format validation
   - Frame extraction errors
   - Processing timeouts

2. **Model Operations**
   - Training failures
   - Inference errors
   - Resource constraints

3. **External Services**
   - API timeouts
   - Authentication failures
   - Network issues 