import os
import cv2
import numpy as np

class FaceDetector:
    def __init__(self):
        # Use OpenCV's built-in Haar cascade for face detection
        # This is more robust across Python versions and environments than MediaPipe
        haar_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(haar_cascade_path)
        if self.face_cascade.empty():
            print("Error: Could not load face cascade xml")

    def process_frame(self, frame):
        """
        Detects faces in a given BGR image frame.
        Returns a list of dicts: [{"bbox": (x, y, w, h), "score": 1.0, "orientation": "front"}]
        """
        if frame is None or frame.size == 0:
            return []

        # Convert to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        # scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))

        detections = []
        for (x, y, w, h) in faces:
            # Estimate orientation / attention based on face position and aspect ratio
            aspect_ratio = float(w) / float(h)
            orientation = "center" if 0.8 <= aspect_ratio <= 1.25 else ("turned_left" if aspect_ratio > 1.25 else "turned_right")
            
            # Format to match project requirements: bbox (x, y, w, h), score (1.0 placeholder)
            detections.append({
                "bbox": (int(x), int(y), int(w), int(h)),
                "score": 1.0,
                "orientation": orientation
            })

        return detections
