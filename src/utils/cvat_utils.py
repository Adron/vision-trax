#!/usr/bin/env python3

import os
from pathlib import Path
from cvat_sdk import make_client
from dotenv import load_dotenv

class CVATClient:
    def __init__(self):
        """Initialize CVAT client with credentials from environment variables."""
        load_dotenv()
        
        self.host = os.getenv('CVAT_HOST', 'http://localhost:8080')
        self.username = os.getenv('CVAT_USERNAME')
        self.password = os.getenv('CVAT_PASSWORD')
        
        if not all([self.username, self.password]):
            raise ValueError("CVAT credentials not found in environment variables")
            
        self.client = make_client(self.host, credentials=(self.username, self.password))
        
    def create_task(self, name, labels):
        """Create a new CVAT task."""
        return self.client.tasks.create_from_data(
            spec={
                'name': name,
                'labels': labels,
            }
        )
        
    def upload_video(self, task_id, video_path):
        """Upload a video file to a CVAT task."""
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        return self.client.tasks.upload_data(
            task_id,
            resources=[str(video_path)],
            resource_type='video'
        )
        
    def export_annotations(self, task_id, output_path):
        """Export annotations from a CVAT task."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        return self.client.tasks.export_data(
            task_id,
            output_path,
            format='CVAT 1.1'
        )

def main():
    """Example usage of CVAT client."""
    try:
        client = CVATClient()
        
        # Example labels for object detection
        labels = [
            {'name': 'person', 'attributes': []},
            {'name': 'car', 'attributes': []},
            {'name': 'bicycle', 'attributes': []}
        ]
        
        # Create a new task
        task = client.create_task('Video Analysis Task', labels)
        print(f"Created task with ID: {task.id}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 