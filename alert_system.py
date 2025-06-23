import pyttsx3
import time


class AlertSystem:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        self.last_alert_time = 0
        self.alert_cooldown = 5  # Seconds between alerts
        self.alert_messages = {
            "Drowsy: Eyes Closed": "Warning: Your eyes are closed. Stay alert!",
            "Drowsy: Yawning": "Warning: You are yawning. Stay awake!",
            "Drowsy: Head Tilted": "Warning: Your head is tilted. Focus on driving!",
            "Drowsy: Frequent Blinking": "Warning: You are blinking frequently. Stay alert!"
        }

    def alert(self, status):
        """Issue an audio alert if cooldown has passed."""
        current_time = time.time()
        if current_time - self.last_alert_time >= self.alert_cooldown:
            try:
                alert_message = self.alert_messages.get(status, "Warning: You appear drowsy. Stay alert!")
                self.engine.say(alert_message)
                self.engine.runAndWait()
                self.last_alert_time = current_time
            except Exception as e:
                print(f"Alert error: {e}")
