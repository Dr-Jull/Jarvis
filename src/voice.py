class VoiceInterface:
    def __init__(self, enabled=False):
        self.enabled = enabled

    def listen_for_speech(self) -> str:
        if not self.enabled:
            return ""
        # In a real implementation, this would use a library like SpeechRecognition
        # example:
        # with sr.Microphone() as source:
        #     audio = self.recognizer.listen(source)
        #     return self.recognizer.recognize_google(audio)
        print("[Voice] Listening... (Stub)")
        return ""

    def speak_text(self, text: str):
        if not self.enabled:
            return
        # In a real implementation, this would use a library like pyttsx3 or gTTS
        # example:
        # self.engine.say(text)
        # self.engine.runAndWait()
        print(f"[Voice] JARVIS says: {text} (Stub)")
