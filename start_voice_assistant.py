from ProductivityTrackerAssistant.VoiceAssistant import voice_assistant

from signal import *
import time


class StartVoiceAssistant:

	def __init__(self):
		pass

		
	def start(self):
		try:
			va = voice_assistant.VoiceAssistant()
			va.start_voice_assistant()
		except Exception as e:
			print(e)



start_va = StartVoiceAssistant()
start_va.start()