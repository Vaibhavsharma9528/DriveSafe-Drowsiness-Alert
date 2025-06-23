import numpy as np
from scipy.spatial import distance as dist


class DrowsinessAnalyzer:
    def __init__(self):
        self.EYE_AR_THRESH = 0.25  # Eye Aspect Ratio threshold for closed eyes
        self.EYE_AR_CONSEC_FRAMES = 20  # Frames for continuous eye closure
        self.YAWN_THRESH = 0.5  # Mouth aspect ratio for yawn
        self.YAWN_CONSEC_FRAMES = 15  # Frames for continuous yawn
        self.HEAD_TILT_THRESH = 30  # Degrees for head tilt
        self.HEAD_TILT_CONSEC_FRAMES = 20  # Frames for continuous head tilt
        self.BLINK_THRESH = 0.25  # EAR threshold for a blink
        self.BLINK_INTERVAL = 10  # Frames to count blinks (e.g., ~0.33 seconds)
        self.BLINK_COUNT_THRESH = 3  # Blinks per interval for frequent blinking
        self.eye_counter = 0
        self.yawn_counter = 0
        self.head_counter = 0
        self.blink_counter = 0
        self.blink_history = []
        self.EYE_INDICES = [33, 160, 158, 133, 153, 144]  # Left eye landmarks
        self.MOUTH_INDICES = [61, 291, 0, 17]  # Mouth landmarks
        self.HEAD_INDICES = [1, 11, 12]  # Nose, left shoulder, right shoulder

    def _eye_aspect_ratio(self, eye_points):
        """Calculate Eye Aspect Ratio."""
        A = dist.euclidean(eye_points[1], eye_points[5])
        B = dist.euclidean(eye_points[2], eye_points[4])
        C = dist.euclidean(eye_points[0], eye_points[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def _mouth_aspect_ratio(self, mouth_points):
        """Calculate Mouth Aspect Ratio."""
        A = dist.euclidean(mouth_points[0], mouth_points[1])
        B = dist.euclidean(mouth_points[2], mouth_points[3])
        mar = B / A
        return mar

    def _head_tilt_angle(self, landmarks):
        """Calculate head tilt angle in degrees."""
        nose = np.array([landmarks[self.HEAD_INDICES[0]].x, landmarks[self.HEAD_INDICES[0]].y])
        left_shoulder = np.array([landmarks[self.HEAD_INDICES[1]].x, landmarks[self.HEAD_INDICES[1]].y])
        right_shoulder = np.array([landmarks[self.HEAD_INDICES[2]].x, landmarks[self.HEAD_INDICES[2]].y])
        shoulder_mid = (left_shoulder + right_shoulder) / 2
        angle = np.arctan2(nose[1] - shoulder_mid[1], nose[0] - shoulder_mid[0])
        return np.abs(np.degrees(angle))

    def _detect_blink(self, ear):
        """Detect a single blink."""
        if ear < self.BLINK_THRESH:
            return True
        return False

    def analyze(self, landmarks):
        """Analyze landmarks for drowsiness."""
        if not landmarks:
            self.eye_counter = 0
            self.yawn_counter = 0
            self.head_counter = 0
            self.blink_counter = 0
            self.blink_history = []
            return "No Face Detected", False

        # Extract eye and mouth points
        eye_points = np.array([(landmarks[i].x, landmarks[i].y) for i in self.EYE_INDICES])
        mouth_points = np.array([(landmarks[i].x, landmarks[i].y) for i in self.MOUTH_INDICES])

        # Calculate EAR
        ear = self._eye_aspect_ratio(eye_points)
        if ear < self.EYE_AR_THRESH:
            self.eye_counter += 1
        else:
            self.eye_counter = 0

        # Calculate MAR
        mar = self._mouth_aspect_ratio(mouth_points)
        if mar > self.YAWN_THRESH:
            self.yawn_counter += 1
        else:
            self.yawn_counter = 0

        # Calculate head tilt
        tilt_angle = self._head_tilt_angle(landmarks)
        if tilt_angle > self.HEAD_TILT_THRESH:
            self.head_counter += 1
        else:
            self.head_counter = 0

        # Detect frequent blinking
        is_blink = self._detect_blink(ear)
        self.blink_history.append(is_blink)
        if len(self.blink_history) > self.BLINK_INTERVAL:
            self.blink_history.pop(0)
        blink_count = sum(self.blink_history)
        if blink_count >= self.BLINK_COUNT_THRESH:
            self.blink_counter += 1
        else:
            self.blink_counter = 0

        # Check for drowsiness
        if self.eye_counter >= self.EYE_AR_CONSEC_FRAMES:
            return "Drowsy: Eyes Closed", True
        if self.yawn_counter >= self.YAWN_CONSEC_FRAMES:
            return "Drowsy: Yawning", True
        if self.head_counter >= self.HEAD_TILT_CONSEC_FRAMES:
            return "Drowsy: Head Tilted", True
        if self.blink_counter >= self.BLINK_INTERVAL:
            return "Drowsy: Frequent Blinking", True

        return "Alert", False
