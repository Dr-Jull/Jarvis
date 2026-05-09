import os

class VoiceInterface:
    def __init__(self, enabled=False):
        self.enabled = enabled
        if self.enabled:
            try:
                import speech_recognition as sr
                import pyttsx3
                self.recognizer = sr.Recognizer()
                self.engine = pyttsx3.init()
            except ImportError:
                print("[Voice] Warning: 'speech_recognition' or 'pyttsx3' not installed. Voice disabled.")
                self.enabled = False

    def listen_for_speech(self) -> str:
        if not self.enabled:
            return ""

        import speech_recognition as sr
        with sr.Microphone() as source:
            print("[Voice] Listening...")
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"[Voice] You said: {text}")
                return text
            except Exception:
                print("[Voice] Could not understand audio.")
                return ""

    def speak_text(self, text: str):
        if not self.enabled:
            return

        print(f"[Voice] JARVIS: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
