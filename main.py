import tkinter as tk
from gui import DrowsinessGUI
from face_detector import FaceDetector
from drowsiness_analyzer import DrowsinessAnalyzer
from alert_system import AlertSystem

def main():
    # Initialize components
    root = tk.Tk()
    face_detector = FaceDetector()
    alert_system = AlertSystem()
    drowsiness_analyzer = DrowsinessAnalyzer()
    
    # Initialize GUI
    app = DrowsinessGUI(root, face_detector, drowsiness_analyzer, alert_system)
    
    # Start the application
    try:
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
    except Exception as e:
        print(f"Error in main loop: {e}")
    finally:
        app.cleanup()

if __name__ == "__main__":
    main()
