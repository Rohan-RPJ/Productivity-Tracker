import speech_recognition as sr
import pyttsx3
import datetime

from string_matching import QuestionMatching
from voice_recognizer import VoiceRecognizer


class VoiceAssistant(VoiceRecognizer):

	def __init__(self):
		VoiceRecognizer.__init__(self)
		
		self.engine=pyttsx3.init('sapi5')
		self.voices=self.engine.getProperty('voices')
		self.engine.setProperty('voice',self.voices[0].id)
		self.speech_as_text = None

		va_activated = self.start_recognizer()
		if va_activated:
			self.recognize_main()


	def recognize_main(self):
		self.greet()
		while True:
			self.speak("Tell me how can I help you Sir?")
			statement = self.recognize_voice()

			if self.__is_statement_valid(statement):
				if "good bye" in statement or "ok bye" in statement or "stop" in statement:
					self.speak('your personal assistant G-one is shutting down,Good bye')
					print('your personal assistant G-one is shutting down,Good bye')
					break

				self.ques_ans(statement)
				
			else:
				continue


	def __is_statement_valid(self, statement):
		if statement == -1:
			self.speak("Pardon me, please say that again")
		elif statement == -2:
			self.speak("Please check your internet connection")
		else:
			return 1
		return 0


	def speak(self, text):
		self.engine.say(text)
		self.engine.runAndWait()


	def greet(self):
		print("Loading your AI personal assistant G-One")
		self.speak("Loading your AI personal assistant G-One")

		hour=datetime.datetime.now().hour
		if hour>=0 and hour<12:
			self.speak("Hello,Good Morning Sir")
			print("Hello,Good Morning Sir")
		elif hour>=12 and hour<18:
			self.speak("Hello,Good Afternoon Sir")
			print("Hello,Good Afternoon Sir")
		else:
			self.speak("Hello,Good Evening Sir")
			print("Hello,Good Evening Sir")


	def ques_ans(self, statement):
		#speak(statement)
		statement = statement.lower()
		qm = QuestionMatching(statement)
		qm.match_question()
		que_ind = qm.get_question_index()
		if que_ind == -1:
			print("Invalid Question")
			self.speak("Please ask a valid Question")
		else:
			ans = qm.get_matched_ans()
			print("Answer: ",ans)
			self.speak(ans)
			# if que_ind == 0:  # user asking about a particular software application
			# 	self.start_software_app_session()
			# elif que_ind == 1:  # user asking about a particular website application
			# 	self.start_web_app_session()
			# else:
			# 	pass


	def start_software_app_session(self):
		self.speak("Please tell the software names one by one")

		from random import randint
		random_speech = ["Any other app", "Next app", "Another app"]

		while True:
			app_name = self.recognize_voice()

			if "stop" in statement or "done" in statement:
				print("Software App Session Stopped...")
				return

			if self.__is_statement_valid(app_name):
				# check if app_name exists in the stored json file
				if app_name_exists in json_file:

					app_data = get_app_data()
					print("Time spent on {app_name} is {time}".format(app_name, app_data["time_spent"]))
					stmt = "You have spent "+time_spent+" in "+app_name
					self.speak(stmt)

					self.speak("Want more information about {app_name} ?".format(app_name))
					yes_or_no = self.recognize_voice()
					if self.__is_statement_valid(yes_or_no):
						if yes_or_no in ["yes", "yup", "yeah", "yo"]:
							# Give rest of the info about the application
							pass
					self.speak(random_speech[randint(0,len(random_speech)-1)])
				else:
					print("Invalid app name")
					self.speak("Please provide a valid app name")

			else:
				continue

		pass


	def start_web_app_session(self):
		pass


va = VoiceAssistant()
va.start_recognizer()
