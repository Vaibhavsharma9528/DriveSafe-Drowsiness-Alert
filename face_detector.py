import cv2
import mediapipe as mp
import numpy as np

class FaceDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5
        )
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Error: Could not open webcam.")
    
    def process_frame(self):
        """Process a video frame and return landmarks and annotated frame."""
        ret, frame = self.cap.read()
        if not ret:
            return None, None
        
        # Convert frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)
        
        # Extract landmarks
        landmarks = None
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
        
        # Draw landmarks
        frame_annotated = frame_rgb.copy()
        if results.multi_face_landmarks:
            self.mp_drawing.draw_landmarks(
                frame_annotated,
                results.multi_face_landmarks[0],
                self.mp_face_mesh.FACEMESH_TESSELATION,
                self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1)
            )
        
        return landmarks, frame_annotated
    
    def cleanup(self):
        """Release resources."""
        self.cap.release()
        self.face_mesh.close()
