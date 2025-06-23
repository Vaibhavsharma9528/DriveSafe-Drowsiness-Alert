import tkinter as tk
from PIL import Image, ImageTk
import time

class DrowsinessGUI:
    def __init__(self, root, face_detector, drowsiness_analyzer, alert_system):
        self.root = root
        self.face_detector = face_detector
        self.drowsiness_analyzer = drowsiness_analyzer
        self.alert_system = alert_system
        self.root.title("Real-Time Drowsiness Detection")
        self.root.geometry("800x600")
        
        # GUI components
        self.label_video = tk.Label(self.root)
        self.label_video.pack(pady=10)
        self.label_status = tk.Label(self.root, text="Status: None", font=("Arial", 16), fg="blue")
        self.label_status.pack(pady=10)
        self.log_frame = tk.Frame(self.root)
        self.log_frame.pack(pady=10)
        self.log_text = tk.Text(self.log_frame, height=5, width=50, font=("Arial", 12))
        self.log_text.pack()
        
        # Start video loop
        self.update_frame()
    
    def update_frame(self):
        """Update GUI with new video frame and status."""
        landmarks, frame_annotated = self.face_detector.process_frame()
        if frame_annotated is not None:
            # Update video feed
            img = Image.fromarray(frame_annotated)
            img = img.resize((640, 480), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(image=img)
            self.label_video.img_tk = img_tk
            self.label_video.config(image=img_tk)
            
            # Analyze drowsiness
            status, is_drowsy = self.drowsiness_analyzer.analyze(landmarks)
            self.label_status.config(text=f"Status: {status}")
            if is_drowsy:
                self.log_text.insert(tk.END, f"{time.strftime('%H:%M:%S')}: {status}\n")
                self.log_text.see(tk.END)
                self.alert_system.alert(status)
        
        self.root.after(33, self.update_frame)
    
    def cleanup(self):
        """Release resources."""
        self.face_detector.cleanup()
        self.root.destroy()
    
    def on_closing(self):
        """Handle window close event."""
        self.cleanup()
