import speech_recognition as sr
import pyttsx3
import datetime
from random import randint

from .text_matching import TextMatching
from .voice_recognizer import VoiceRecognizer
from ..Database.FirebaseDatabase import retrieve_data
from .Constants.questions import QUES




retrieve_user_data = retrieve_data.RetrieveUserData().getInstance()
retrieve_sw_data = retrieve_data.RetrieveSoftwareData().getInstance()
retrieve_web_data = retrieve_data.RetrieveWebsiteData().getInstance()

username = retrieve_user_data.get_firstname()

random_speech = [
	"Any other app name {} ?".format(username),
	"Some other app name {} ?".format(username),
	"Give other app name {}".format(username),
]



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
		self.speak("Tell me how can I help you ?")
		try:
			while True:
				statement = self.recognize_voice()

				if self.__is_statement_valid(statement):
					if "good bye" in statement or "ok bye" in statement or "stop" in statement or "shutdown" in statement:
						self.speak('your personal assistant Jarvis is shutting down,Good bye')
						print('your personal assistant Jarvis is shutting down,Good bye')
						break

					self.ques_ans(statement)
					
				else:
					continue
		except Exception as e:
			print(e)


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
		print("Loading your AI personal assistant Jarvis")
		self.speak("Loading your AI personal assistant Jarvis")

		hour=datetime.datetime.now().hour
		if hour>=0 and hour<12:
			self.speak("Hello,Good Morning Rohan")
			print("Hello,Good Morning Rohan")
		elif hour>=12 and hour<18:
			self.speak("Hello,Good Afternoon Rohan")
			print("Hello,Good Afternoon Rohan")
		else:
			self.speak("Hello,Good Evening Rohan")
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
			self.speak("Please ask a valid Question")

		else:

			if que_ind == 0:  # user asking about a particular software application
				self.start_software_app_session()

			elif que_ind == 1:  # user asking about a particular website application
				self.start_web_app_session()

			elif que_ind == 2:  # user asking total app or all app or desktop tracking time
				ttt = retrieve_user_data.get_total_tracking_time()
				ttt = VoiceAssistant.get_readable_time(ttt)
				print("You have spent {} on your desktop".format(ttt))
				self.speak("You have spent {} time on your desktop".format(ttt))

			elif que_ind == 3:  # user asking total software tracking time
				tstt = retrieve_sw_data.get_total_tracking_time()
				tstt = VoiceAssistant.get_readable_time(tstt)
				print("You have spent {} on all software application".format(tstt))
				self.speak("You have spent {} on all software application".format(tstt))

			elif que_ind == 4:
				twtt = retrieve_web_data.get_total_tracking_time()
				twtt = VoiceAssistant.get_readable_time(twtt)
				print("You have spent {} on all website application".format(twtt))
				self.speak("You have spent {} on all website application".format(twtt))

			elif que_ind in [5, 6, 7]:  # user asking time spent on all apps
				print("Preparing your response {}".format(username))
				self.speak("Preparing your response {}".format(username))
				#  open the electron app where and show the required ans to the user

			elif que_ind == 8:
				mostly_used_sw_apps, max_time_spent = retrieve_sw_data.get_mostly_used_apps()
				max_time_spent = VoiceAssistant.get_readable_time(max_time_spent)

				if len(mostly_used_sw_apps) == 0:
					print("No software application used")
					self.speak("You have not used any software application")

				else:
					print("Maximum used software app/'s is/are: {}".format(' '.join(mostly_used_sw_apps)))
					print("And max time spent is: {}".format(max_time_spent))
					self.speak("You have spent maximum time on {} and {}".format(' '.join(mostly_used_sw_apps[-1:0:-1]), mostly_used_sw_apps[0]))
					self.speak("And maximum time spent is {}".format(max_time_spent))

			elif que_ind == 9:

				mostly_used_web_apps, max_time_spent = retrieve_web_data.get_mostly_used_apps()
				max_time_spent = VoiceAssistant.get_readable_time(max_time_spent)

				if len(mostly_used_web_apps) == 0:
					print("No software application used")
					self.speak("You have not used any software application")

				else:
					print("Maximum used software app/'s is/are: {}".format(' '.join(mostly_used_web_apps)))
					print("And max time spent is: {}".format(max_time_spent))
					self.speak("You have spent maximum time on {} and {}".format(' '.join(mostly_used_web_apps[-1:0:-1]), mostly_used_web_apps[0]))
					self.speak("And maximum time spent is {}".format(max_time_spent))

			elif que_ind in [10, 11, 12]:
				tspt = retrieve_sw_data.get_total_productive_time()
				twpt = retrieve_web_data.get_total_productive_time()
				tpt = VoiceAssistant.add_time(tspt, twpt)
				tpt = VoiceAssistant.get_readable_time(tpt)
				print("Total productive time spent: {}".format(tpt))
				self.speak("{username}, you have spent {tpt} productively".format(username=username, tpt=tpt))

			elif que_ind in [13, 14, 15]:
				tsupt = retrieve_sw_data.get_total_unproductive_time()
				twupt = retrieve_web_data.get_total_unproductive_time()
				tupt = VoiceAssistant.add_time(tsupt, twupt)
				tupt = VoiceAssistant.get_readable_time(tupt)
				print("Total unproductive time spent: {}".format(tupt))
				self.speak("{username}, you have spent {tpt} unproductively".format(username=username, tpt=tupt))

			elif que_ind == 12:
				print("Show the electron app")
				self.speak("Showing the elelctron app")
					

	@staticmethod
	def add_time(t1, t2):  # time t1 and t2 will be in 'x-h x-m x-s' format
		t1_h, t1_m, t1_s = [int(t.split('-')[0]) for t in t1.split()]
		t2_h, t2_m, t2_s = [int(t.split('-')[0]) for t in t2.split()]
		secs = (t1_s + t2_s)
		mins = (t1_m + t2_m + secs//60)
		hrs = (t1_h + t2_h + mins//60)
		secs %= 60
		mins %= 60
		time_spent = str(hrs) + "-h " + str(mins) + "-m " + str(secs)+ "-s"

		return time_spent


	@staticmethod
	def get_readable_time(time):  # time will be in 'x-h x-m x-s' format
		t_h, t_m, t_s = [t.split('-')[0] for t in time.split()]
		readable_time = None
		if t_h == "0":
			readable_time = "{} minutes {} seconds".format(t_m, t_s)
		else:
			readable_time = "{} hours {} minutes {} seconds".format(t_h, t_m, t_s)

		return readable_time


	def __replace_dashes_with_spaces(self, text):
		return ' '.join(text.split('-'))


	def __replace_spaces_with_dashes(self, text):
		return '-'.join(text.split())


	def start_software_app_session(self):
		self.speak("Please tell the software names one by one")

		from random import randint

		while True:
			app_name = self.recognize_voice()
			# app_name = input("Enter app name: ")

			if self.__is_statement_valid(app_name):

				if "stop" in app_name or "done" in app_name:
					print("Software App Session Stopped...")
					return

				# in case if app_name to be matched has no spaces
				app_name_without_spaces = ''.join(app_name.split())

				# get software apps list from firebase
				stored_app_list = retrieve_sw_data.get_app_list()
				stored_app_list = list(map(self.__replace_dashes_with_spaces, stored_app_list))
				print(stored_app_list)

				# check if app_name exists in the stored firebase db
				app_matching = TextMatching(stored_app_list)
				app_matching.match_text(app_name)
				app_matched_index = app_matching.get_matched_text_index()
				
				if app_matched_index == -1:
					app_matching.match_text(app_name_without_spaces)
					app_matched_index = app_matching.get_matched_text_index()

				if app_matched_index == -1:

					print("No such software exists")
					self.speak("Please provide a valid app name")

				else:
					print("Software exists")
					stored_app_name = self.__replace_spaces_with_dashes(stored_app_list[app_matched_index])
					time_spent = retrieve_sw_data.get_individual_app_tracking_time(stored_app_list[app_matched_index])
					time_spent = VoiceAssistant.get_readable_time(time_spent)
					print("Time spent on {app_name} is {time}".format(app_name=stored_app_name, time=time_spent))
					stmt = "You have spent {time} on {app_name}".format(time=time_spent, app_name=stored_app_name)
					self.speak(stmt)

					self.speak(random_speech[randint(0,len(random_speech)-1)])
				

	def start_web_app_session(self):
		self.speak("Please tell the website names one by one")

		while True:
			hostname = self.recognize_voice()
			# hostname = input("Enter hostname: ")

			if self.__is_statement_valid(hostname):

				if "stop" in hostname or "done" in hostname:
					print("Website App Session Stopped...")
					return

				# in case if hostname to be matched has no spaces
				hostname_without_spaces = ''.join(hostname.split())

				# get software apps list from firebase
				stored_app_list = retrieve_web_data.get_app_list()
				stored_app_list = list(map(self.__replace_dashes_with_spaces, stored_app_list))
				print(stored_app_list)

				# check if hostname exists in the stored firebase db
				app_matching = TextMatching(stored_app_list)
				app_matching.match_text(hostname)
				app_matched_index = app_matching.get_matched_text_index()

				if app_matched_index == -1:
					app_matching.match_text(hostname_without_spaces)
					app_matched_index = app_matching.get_matched_text_index()

				if app_matched_index == -1:

					print("No such website exists")
					self.speak("Please provide a valid site name")

				else:
					print("Website exists")
					stored_hostname = self.__replace_spaces_with_dashes(stored_app_list[app_matched_index])
					time_spent = retrieve_web_data.get_individual_app_tracking_time(stored_hostname)
					time_spent = VoiceAssistant.get_readable_time(time_spent)
					print("Time spent on {hostname} is {time}".format(hostname=stored_hostname, time=time_spent))
					stmt = "You have spent {time} on {hostname}".format(time=time_spent, hostname=stored_hostname)
					self.speak(stmt)

					self.speak(random_speech[randint(0,len(random_speech)-1)])