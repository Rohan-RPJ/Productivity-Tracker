import speech_recognition as sr

from string_matching import QuestionMatching


class VoiceRecognizer:
    """docstring for VoiceRecognizer"""

    def __init__(self):
        self.r=sr.Recognizer()
        '''
        This is basically how sensitive the recognizer is to when recognition should start. Higher values 
        mean that it will be less sensitive, which is useful if you are in a loud room. This value depends
        entirely on your microphone or audio data. There is no one-size-fits-all value, 
        but good values typically range from 50 to 4000.
        '''
        self.r.energy_threshold = 1500 
        #print(r.energy_threshold)


    def start_recognizer(self):
        print("Listening in background")
        while True:
            keyword_in_audio = self.recognize_keyword()
            if keyword_in_audio:
                return 1
                

    def recognize_keyword(self):
        
        self.speech_as_text = self.recognize_voice()

        print(self.speech_as_text)

        # Look for your "Ok Google" keyword in speech_as_text
        if type(self.speech_as_text) == int:
            return False
        if self.speech_as_text and ("Google" in self.speech_as_text or "hey Google" in self.speech_as_text):
            print("Stop listening for keywords...\n")
            print("Starting your Voice Assistant...\n")
            return True
        return False


    def recognize_voice(self):  # speech to text
        statement = None
        audio = self.capture_audio()
        try:
            print("Recognition started")
            statement=self.r.recognize_google(audio,language='en-us')
            print("Recognition ended")
            print(f"user said:{statement}\n")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return -1
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return -2
        return statement


    def capture_audio(self):
        audio = None
        # with sr.Microphone() as source:

        '''
        To set the energy_threshold to a good value automatically.
        '''
        #audio = self.r.adjust_for_ambient_noise(self.source)
        #print("Energy Threshold after adjusting for ambient noise: ",r.energy_threshold)

        print("Listening...")
        try:
            with sr.Microphone() as source:
                #audio=r.listen(self.source, timeout=3)
                self.r.energy_threshold = 1500
                print(self.r.energy_threshold)
                audio=self.r.listen(source)
                print("Audio Captured")
        except Exception as e:
            print(e)
            self.speak("please say something")
        return audio
