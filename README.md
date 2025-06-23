DriveSafe: Real-Time Drowsiness Alert
A Python-based system to detect driver drowsiness in real-time using computer vision. Monitors eye closure, yawning, head tilting, and frequent blinking via webcam, displaying status on a GUI and issuing audio alerts for road safety.
Features

Real-time facial expression detection with MediaPipe.
Tracks Eye Aspect Ratio (EAR) and Mouth Aspect Ratio (MAR).
Detects head tilt and frequent blinking for enhanced drowsiness analysis.
Tkinter GUI for status and event logging.
Audio alerts via text-to-speech (pyttsx3).
Modular code with error handling.

Tech Stack

Python 3.9
Libraries: OpenCV, MediaPipe, NumPy, Pillow, pyttsx3, scikit-learn
Hardware: Webcam

Installation

Clone the repository:git clone https://github.com/your-username/DriveSafe-Drowsiness-Alert.git
cd DriveSafe-Drowsiness-Alert


Create and activate a virtual environment (optional):python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate


Install dependencies:pip install -r requirements.txt


Linux only: Install espeak for audio alerts:sudo apt-get install espeak



Usage

Ensure a webcam is connected.
Run the application:python main.py


The GUI displays the webcam feed, drowsiness status, and event log. Audio alerts trigger for detected drowsiness.

How It Works

Face Detection: MediaPipe Face Mesh tracks facial landmarks.
Drowsiness Analysis: Calculates EAR for eye closure, MAR for yawning, head tilt angle, and blink frequency.
Alerts: Issues audio warnings for prolonged eye closure, yawning, head tilting, or frequent blinking.

Testing

Closed Eyes: Close eyes for ~1 second → “Drowsy: Eyes Closed”.
Yawning: Open mouth wide for ~1 second → “Drowsy: Yawning”.
Head Tilting: Tilt head >30° for ~1 second → “Drowsy: Head Tilted”.
Frequent Blinking: Blink 3+ times in ~0.33 seconds → “Drowsy: Frequent Blinking”.

Calibration
Adjust thresholds in drowsiness_analyzer.py for sensitivity:
self.EYE_AR_THRESH = 0.3      # Eye closure
self.YAWN_THRESH = 0.4        # Yawning
self.HEAD_TILT_THRESH = 35    # Head tilt
self.BLINK_COUNT_THRESH = 2   # Blinking

Project Structure
DriveSafe-Drowsiness-Alert/
├── main.py               # Entry point
├── face_detector.py      # Face landmark detection
├── drowsiness_analyzer.py # Drowsiness logic
├── gui.py                # Tkinter GUI
├── alert_system.py       # Audio alerts
├── requirements.txt      # Dependencies
├── README.md             # Project documentation

License
MIT License
Author
[Your Name] - [Your LinkedIn Profile URL]
Acknowledgments

MediaPipe for facial landmark detection.
OpenCV for video processing.
