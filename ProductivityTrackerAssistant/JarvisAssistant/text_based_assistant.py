import datetime

from .text_matching import TextMatching
from ..Database.FirebaseDatabase import retrieve_data
from .Constants.questions import QUES
from .q_and_a import QueAns
from .speak import speak



retrieve_user_data = retrieve_data.RetrieveUserData.getInstance()
retrieve_sw_data = retrieve_data.RetrieveSoftwareData.getInstance()
retrieve_web_data = retrieve_data.RetrieveWebsiteData.getInstance()

username = retrieve_user_data.get_firstname()


class TextAssistant:

	def __init__(self):

		pass


	def start_text_assistant(self):

		self.recognize_main()


	def recognize_main(self):

		self.greet()

		QUES_KEYS = list(map(str, list(QUES.keys())))

		try:
			while True:

				for i,que in enumerate(QUES.values()):
					print(i, ": ", que)

				choice = input("\nEnter Choice: ")

				if choice in QUES_KEYS:

					self.ques_ans(int(choice))

				else:

					speak('your personal assistant Jarvis is shutting down,Good bye')
					print('your personal assistant Jarvis is shutting down,Good bye')
					break
					
		except Exception as e:
			print(e)


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


	def ques_ans(self, que_ind):

		if que_ind == 0:  # user asking about a particular software application
			
			speak("Please provide the software name")
			print("Please provide the software name")

			print("\nEnter 'stop' to go back")

			while True:

				sw_app_name = input("Enter software name: ")

				if sw_app_name.lower() == "stop":
					speak("OK {} !".format(username))
					break
				else:
					QueAns.answer(que_ind, app_name=sw_app_name)

		elif que_ind == 1:  # user asking about a particular website application

			speak("Please provide the website name")
			print("Please provide the software name")

			print("\nEnter 'stop' to go back")

			while True:

				web_app_name = input("Enter website name: ")

				if web_app_name.lower() == "stop":
					speak("OK {} !".format(username))
					break
				else:
					QueAns.answer(que_ind, app_name=web_app_name)

		else:
			QueAns.answer(que_ind)