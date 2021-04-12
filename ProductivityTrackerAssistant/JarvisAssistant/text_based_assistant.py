import datetime

from .text_matching import TextMatching
from ..Database.FirebaseDatabase import retrieve_data
from .Constants.questions import *
from .q_and_a import QueAns
from .speak import speak



retrieve_user_data = retrieve_data.RetrieveUserData.getInstance()
retrieve_sw_data = retrieve_data.RetrieveSoftwareData.getInstance()
retrieve_web_data = retrieve_data.RetrieveWebsiteData.getInstance()

username = retrieve_user_data.get_firstname()

stop_assistant_texts = ["bye", "stop", "shutdown", "shut down"]

class TextAssistant:

	def __init__(self):

		pass


	def start_text_assistant(self):

		self.recognize_main()


	def stmt_contains_stop_texts(self, statement):
		for stop_text in stop_assistant_texts:
			if stop_text in statement:
				return 1

		return 0


	def recognize_main(self):

		# self.greet()

		print("\n1.Give List of Questions  2.Enter Input Question: ")

		choice = input("\nEnter a choice: ")


		if choice=="1":

			QUES_KEYS = list(map(str, list(QUES_SHOW.keys())))

			try:
				while True:

					for i,que in enumerate(QUES_SHOW.values()):
						print(i+1, ": ", que)

					choice = input("Enter Question number: ")
					choice = "q"+choice

					if choice in QUES_KEYS:

						self.ques_ans(map_show_to_actual[choice])

					else:

						speak('Your personal assistant Jarvis is shutting down,Good bye')
						print('Your personal assistant Jarvis is shutting down,Good bye')
						break
						
			except Exception as e:
				print(e)

		elif choice=="2":

			try:
				while True:

					ip_ques = input("Enter your question: ")

					if self.__is_statement_valid(ip_ques):

						if self.stmt_contains_stop_texts(ip_ques):

							speak('your personal assistant Jarvis is shutting down,Good bye')
							print('your personal assistant Jarvis is shutting down,Good bye')
							break

						ip_ques = ip_ques.lower()
						qm = TextMatching(list(QUES.values()))
						qm.match_text(ip_ques)
						que_ind = qm.get_matched_text_index()

						self.ques_ans(que_ind)
						
					else:
						print("\nEnter a valid question")
						continue
			except Exception as e:
				print(e)

		else:
			print("Invalid choice")


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


	def ques_ans(self, que_ind):
		print("QueInd: ",que_ind)
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