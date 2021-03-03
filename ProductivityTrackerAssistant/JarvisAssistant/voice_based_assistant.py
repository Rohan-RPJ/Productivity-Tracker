import speech_recognition as sr
import datetime
import random

from .text_matching import TextMatching
from .voice_recognizer import VoiceRecognizer
from ..Database.FirebaseDatabase import retrieve_data
from .Constants.questions import QUES
from .q_and_a import QueAns
from .speak import speak



retrieve_user_data = retrieve_data.RetrieveUserData.getInstance()
retrieve_sw_data = retrieve_data.RetrieveSoftwareData.getInstance()
retrieve_web_data = retrieve_data.RetrieveWebsiteData.getInstance()

username = retrieve_user_data.get_firstname()

random_asking_text = [
	"Any other app name {} ?".format(username),
	"Some other app name {} ?".format(username),
	"Give other app name {}".format(username),
]

stop_assistant_texts = ["bye", "stop", "shutdown", "shut down"]


class VoiceAssistant(VoiceRecognizer):

	def __init__(self):

		VoiceRecognizer.__init__(self)


	def start_voice_assistant(self):

		va_activated = self.start_recognizer()
		if va_activated:
			self.recognize_main()


	def stmt_contains_stop_texts(self, statement):
		for stop_text in stop_assistant_texts:
			if stop_text in statement:
				return 1

		return 0


	def recognize_main(self):

		self.greet()

		try:
			while True:

				speak("Tell me how can I help you?")

				statement = self.recognize_voice()

				if self.__is_statement_valid(statement):

					if self.stmt_contains_stop_texts(statement):

						speak('your personal assistant Jarvis is shutting down,Good bye')
						print('your personal assistant Jarvis is shutting down,Good bye')
						break

					self.ques_ans(statement)
					
				else:
					continue
		except Exception as e:
			print(e)


	def __is_statement_valid(self, statement):
		if statement == -1:
			speak("Pardon me, please say that again")
		elif statement == -2:
			speak("Please check your internet connection")
		else:
			return 1
		return 0


	def greet(self):
		print("Loading your AI personal assistant Jarvis")
		speak("Loading your AI personal assistant Jarvis")

		hour=datetime.datetime.now().hour
		if hour>=0 and hour<12:
			speak("Hello,Good Morning Rohan")
			print("Hello,Good Morning Rohan")
		elif hour>=12 and hour<18:
			speak("Hello,Good Afternoon Rohan")
			print("Hello,Good Afternoon Rohan")
		else:
			speak("Hello,Good Evening Rohan")
			print("Hello,Good Evening Rohan")


	def ques_ans(self, statement):
		#speak(statement)
		statement = statement.lower()
		qm = TextMatching(list(QUES.values()))
		qm.match_text(statement)
		que_ind = qm.get_matched_text_index()
		print("Matched Question: ", que_ind)

		if que_ind == -1:

			print("Invalid Question")
			speak("Please ask a valid Question")

		else:

			if que_ind == 0:  # user asking about a particular software application
				
				speak("Please provide the software name")

				while True:

					sw_app_name, exit_code = self.get_sw_app_name()

					if exit_code == 1:
						speak("OK {} !".format(username))
						break
					else:
						if sw_app_name is None:
							speak("Please provide a valid software name")
						else:
							QueAns.answer(que_ind, app_name=sw_app_name)

							speak(random.choice(random_asking_text))

			elif que_ind == 1:  # user asking about a particular website application

				speak("Please provide the website name")

				while True:

					web_app_name, exit_code = self.get_sw_app_name()

					if exit_code == 1:
						speak("OK {} !".format(username))
						break
					else:
						if web_app_name is None:
							speak("Please provide a valid website name")
						else:
							QueAns.answer(que_ind, app_name=web_app_name)

							speak(random.choice(random_asking_text))

			else:
				QueAns.answer(que_ind)


	def get_sw_app_name(self):  # returns sw_app_name, exit_code(1 if user is done, 0 if not done)

		sw_app_name = self.recognize_voice()

		if self.__is_statement_valid(sw_app_name):

			if "stop" in sw_app_name or "done" in sw_app_name:
				return None, 1

			return sw_app_name, 0
		else:
			return None, 0


	def get_web_app_name(self):  # returns web_app_name, exit_code(1 if user is done, 0 if not done)

		web_app_name = self.recognize_voice()

		if self.__is_statement_valid(web_app_name):

			if "stop" in web_app_name or "done" in web_app_name:
				return None, 1

			return web_app_name, 0

		else:
			return None, 0