
from .text_matching import TextMatching
from ..Database.FirebaseDatabase import retrieve_data
from .speak import speak



retrieve_user_data = retrieve_data.RetrieveUserData().getInstance()
retrieve_sw_data = retrieve_data.RetrieveSoftwareData().getInstance()
retrieve_web_data = retrieve_data.RetrieveWebsiteData().getInstance()

username = retrieve_user_data.get_firstname()

random_speech = [
	"Any other app name {} ?".format(username),
	"Some other app name {} ?".format(username),
	"Give other app name {}".format(username),
]



class QueAns():

	@staticmethod
	def answer(que_index, app_name=None):

		que_ind = que_index

		if que_ind == 0:  # user asking about a particular software application

			time_spent, stored_app_name = QueAns.get_software_time_spent(app_name)

			if time_spent is None:

				speak("Please provide a valid app name")

			else:
				print("Time spent on {app_name} is {time}".format(app_name=stored_app_name, time=time_spent))
				stmt = "You have spent {time} on {app_name}".format(time=time_spent, app_name=stored_app_name)

				speak(stmt)

		elif que_ind == 1:  # user asking about a particular website application

			time_spent, stored_hostname = QueAns.get_website_time_spent(app_name)

			if time_spent is None:

				speak("Please provide a valid stie name")

			else:

				print("Time spent on {hostname} is {time}".format(hostname=stored_hostname, time=time_spent))
				stmt = "You have spent {time} on {hostname}".format(time=time_spent, hostname=stored_hostname)

				speak(stmt)

		elif que_ind in [2,3]:  # user asking total app or all app or desktop tracking time
			ttt = retrieve_user_data.get_total_tracking_time()
			ttt = QueAns.get_readable_time(ttt)
			print("You have spent {} on your desktop".format(ttt))
			speak("You have spent {} on your desktop".format(ttt))

		elif que_ind == 4:  # user asking total software tracking time
			tstt = retrieve_sw_data.get_total_tracking_time()
			tstt = QueAns.get_readable_time(tstt)
			print("You have spent {} on all software application".format(tstt))
			speak("You have spent {} on all software application".format(tstt))

		elif que_ind == 5:
			twtt = retrieve_web_data.get_total_tracking_time()
			twtt = QueAns.get_readable_time(twtt)
			print("You have spent {} on all website application".format(twtt))
			speak("You have spent {} on all website application".format(twtt))

		elif que_ind in [6, 7, 8]:  # user asking time spent on all apps
			print("Preparing your response {}".format(username))
			speak("Preparing your response {}".format(username))
			#  open the electron app where and show the required ans to the user

		elif que_ind == 9:
			mostly_used_sw_apps, max_time_spent = retrieve_sw_data.get_mostly_used_apps()
			max_time_spent = QueAns.get_readable_time(max_time_spent)

			if len(mostly_used_sw_apps) == 0:
				print("No software application used")
				speak("You have not used any software application")

			else:
				print("Maximum used software app/'s is/are: {}".format(' '.join(mostly_used_sw_apps)))
				print("And max time spent is: {}".format(max_time_spent))
				speak("You have spent maximum time on {} and {}".format(' '.join(mostly_used_sw_apps[-1:0:-1]), mostly_used_sw_apps[0]))
				speak("And maximum time spent is {}".format(max_time_spent))

		elif que_ind == 10:

			mostly_used_web_apps, max_time_spent = retrieve_web_data.get_mostly_used_apps()
			max_time_spent = QueAns.get_readable_time(max_time_spent)

			if len(mostly_used_web_apps) == 0:
				print("No software application used")
				speak("You have not used any software application")

			else:
				print("Maximum used web app/'s is/are: {}".format(' '.join(mostly_used_web_apps)))
				print("And max time spent is: {}".format(max_time_spent))
				speak("You have spent maximum time on {} and {}".format(' '.join(mostly_used_web_apps[-1:0:-1]), mostly_used_web_apps[0]))
				speak("And maximum time spent is {}".format(max_time_spent))

		elif que_ind in [11, 12, 13]:
			tpt = retrieve_user_data.get_total_productive_time()
			tpt = QueAns.get_readable_time(tpt)
			print("Total productive time spent: {}".format(tpt))
			speak("{username}, you have spent {tpt} productively".format(username=username, tpt=tpt))

		elif que_ind in [14, 15, 16]:
			tupt = retrieve_user_data.get_total_unproductive_time()
			tupt = QueAns.get_readable_time(tupt)
			print("Total unproductive time spent: {}".format(tupt))
			speak("{username}, you have spent {tpt} unproductively".format(username=username, tpt=tupt))

		elif que_ind == 17:
			print("Show the electron app")
			speak("Showing the elelctron app")
				

	@staticmethod
	def get_readable_time(time):  # time will be in 'x-h x-m x-s' format
		t_h, t_m, t_s = [t.split('-')[0] for t in time.split()]
		readable_time = None
		if t_h == "0":
			readable_time = "{} minutes {} seconds".format(t_m, t_s)
		else:
			readable_time = "{} hours {} minutes {} seconds".format(t_h, t_m, t_s)

		return readable_time


	@staticmethod
	def __replace_dashes_with_spaces(text):
		return ' '.join(text.split('-'))


	@staticmethod
	def __replace_spaces_with_dashes(text):
		return '-'.join(text.split())


	@staticmethod
	def get_software_time_spent(sw_app_name):

		# in case if sw_app_name to be matched has no spaces
		sw_app_name_without_spaces = ''.join(sw_app_name.split())

		# get software apps list from firebase
		stored_app_list = retrieve_sw_data.get_app_list()
		stored_app_list = list(map(QueAns.__replace_dashes_with_spaces, stored_app_list))
		print(stored_app_list)

		# check if sw_app_name exists in the stored firebase db
		app_matching = TextMatching(stored_app_list)
		app_matching.match_text(sw_app_name)
		app_matched_index = app_matching.get_matched_text_index()
		
		if app_matched_index == -1:
			app_matching.match_text(sw_app_name_without_spaces)
			app_matched_index = app_matching.get_matched_text_index()

		if app_matched_index == -1:

			print("No such software exists")
			return None, None

		else:

			print("Software exists")

			stored_app_name = QueAns.__replace_spaces_with_dashes(stored_app_list[app_matched_index])
			time_spent = retrieve_sw_data.get_individual_app_tracking_time(stored_app_list[app_matched_index])
			time_spent = QueAns.get_readable_time(time_spent)
			
			return time_spent, stored_app_name
		

	@staticmethod
	def get_website_time_spent(web_app_name):

		# in case if web_app_name to be matched has no spaces
		web_app_name_without_spaces = ''.join(web_app_name.split())

		# get software apps list from firebase
		stored_app_list = retrieve_web_data.get_app_list()
		stored_app_list = list(map(QueAns.__replace_dashes_with_spaces, stored_app_list))
		print(stored_app_list)

		# check if web_app_name exists in the stored firebase db
		app_matching = TextMatching(stored_app_list)
		app_matching.match_text(web_app_name)
		app_matched_index = app_matching.get_matched_text_index()

		if app_matched_index == -1:
			app_matching.match_text(web_app_name_without_spaces)
			app_matched_index = app_matching.get_matched_text_index()

		if app_matched_index == -1:

			print("No such website exists")
			return None, None

		else:

			print("Website exists")

			stored_hostname = QueAns.__replace_spaces_with_dashes(stored_app_list[app_matched_index])
			time_spent = retrieve_web_data.get_individual_app_tracking_time(stored_hostname)
			time_spent = QueAns.get_readable_time(time_spent)

			return time_spent, stored_hostname