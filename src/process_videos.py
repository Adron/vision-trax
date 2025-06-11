#!/usr/bin/env python3

import os
import cv2
from pathlib import Path
from ultralytics import YOLO
from tqdm import tqdm

class VideoProcessor:
    def __init__(self, model_path=None):
        """Initialize the video processor with YOLO model."""
        self.model = YOLO(model_path) if model_path else YOLO('yolov8n.pt')
        
    def process_video(self, video_path, output_dir=None):
        """Process a single video file with YOLO detection."""
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        # Create output directory if specified
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
        # Open video file
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
            
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Process frames
        results = []
        for _ in tqdm(range(frame_count), desc=f"Processing {video_path.name}"):
            ret, frame = cap.read()
            if not ret:
                break
                
            # Run YOLO detection
            result = self.model(frame)
            results.append(result)
            
        cap.release()
        return results

def main():
    # Initialize video processor
    processor = VideoProcessor()
    
    # Process all videos in the videos directory
    video_dir = Path("videos")
    if not video_dir.exists():
        print(f"Creating videos directory: {video_dir}")
        video_dir.mkdir(parents=True, exist_ok=True)
        print("Please add video files to the videos directory and run again.")
        return
        
    # Process each video file
    for video_file in video_dir.glob("*.mp4"):
        print(f"\nProcessing video: {video_file.name}")
        try:
            results = processor.process_video(video_file)
            print(f"Successfully processed {video_file.name}")
        except Exception as e:
            print(f"Error processing {video_file.name}: {str(e)}")

if __name__ == "__main__":
    main() 