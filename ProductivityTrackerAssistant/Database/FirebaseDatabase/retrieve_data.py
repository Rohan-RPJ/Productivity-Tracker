"""
DOCSTRINGS
"""


# Standard library imports


# Third party imports
from . import db


# Local application imports
from ...Constants.keys import *
from ...time_arithmetic import TimeArithmetic



time_arith = TimeArithmetic()

initial_time = time_arith.initial_time
url_title_separator = "-*-"

# A list of class into which websites are categorized
productive=[c for i,c in PRODUCTIVE_STR.items()]
unproductive=[c for i,c in UNPRODUCTIVE_STR.items()]


class user:
	uid = 123
uid = user.uid


def get_max_time_indexes(time_list):
		time_list = time_list.copy()

		# convert str time('x-h y-m z-s') to int time(xyz). The ones with greatest value of xyz will be maximum
		for i in range(len(time_list)):
			time_list[i] = list(map(lambda s: s.split('-')[0], time_list[i].split()))  # OP=>['x', 'y', 'z']
			time_list[i] = int(''.join(time_list[i]))  # OP=> xyz

		max_time = time_list[0]
		max_indexes = [0]

		for i in range(1, len(time_list)):
			if time_list[i] > max_time:
				max_indexes = [i]
				max_time = time_list[i]
			elif time_list[i] == max_time:
				max_indexes.append(i)

		return max_indexes


def get_p_up_str(isProductive):

		if isProductive:
			return "p"
		else:
			return "up"


class RetrieveUserData:
	"""Singleton RetrieveUserData class"""

	__instance = None

	@staticmethod
	def getInstance():
		""" Static access method. """
		if RetrieveUserData.__instance == None:
			RetrieveUserData()
		return RetrieveUserData.__instance


	def __init__(self):  # firebase authenticated user fetched from frontend
		""" Virtually private costructor """

		if RetrieveUserData.__instance != None:
			raise Exception("RetrieveUserData is a Singleton Class!")
		else:
			RetrieveUserData.__instance = self


	def get_firstname(self):
		return db.child("users").child(uid).child("fn").get().val()


	def get_lastname(self):
		return db.child("users").child(uid).child("ln").get().val()


	def get_total_tracking_time(self):
		return db.child("users").child(uid).child("ttt").get().val()


	def get_isDBCleared_val(self):
		return db.child("users").child(uid).child("isDBCleared").get().val()


	def get_last_tracking_date(self):
		return db.child("users").child(uid).child("ltd").get().val()


	def get_total_productive_time(self):
		tspt = retrieve_sw_data.get_total_productive_time()
		twpt = retrieve_web_data.get_total_productive_time()
		tpt = time_arith.add_time(tspt, twpt)
		
		return tpt


	def get_total_unproductive_time(self):
		tsupt = retrieve_sw_data.get_total_unproductive_time()
		twupt = retrieve_web_data.get_total_unproductive_time()
		tupt = time_arith.add_time(tsupt, twupt)
		
		return tupt



class RetrieveSoftwareData:
	"""Singleton RetrieveSoftwareData class"""

	__instance = None

	@staticmethod
	def getInstance():
		""" Static access method. """
		if RetrieveSoftwareData.__instance == None:
			RetrieveSoftwareData()
		return RetrieveSoftwareData.__instance


	def __init__(self):  # firebase authenticated user fetched from frontend
		""" Virtually private costructor """

		if RetrieveSoftwareData.__instance != None:
			raise Exception("RetrieveSoftwareData is a Singleton Class!")
		else:
			RetrieveSoftwareData.__instance = self


	def get_app_list(self):  # returns sw apps list

		# shallow() returns all keys under given path(here istt/uid/)
		dict_keys = db.child("istt").child(uid).shallow().get().val()

		return list(dict_keys)


	def get_total_tracking_time(self):  # returns total software tracking time
		return db.child("sa").child(uid).child("tstt").get().val()


	def get_total_productive_time(self):  # returns total software productive time
		return db.child("sa").child(uid).child("p").child("tspt").get().val()


	def get_total_unproductive_time(self):  # returns total software unproductive time
		return db.child("sa").child(uid).child("up").child("tsupt").get().val()
 	

	def get_total_category_time(self, category, isProductive):  # returns software total category time

		p_up_str = get_p_up_str(isProductive)

		return db.child("sa").child(uid).child(p_up_str).child(category).child("tct").get().val()


	def get_total_mutual_time_in_category(self, app_name, category, isProductive):  # software total mutual time in given category
		
		p_up_str = get_p_up_str(isProductive)
		
		try:
			val = db.child("sa").child(uid).child(p_up_str).child(category).child(app_name).child("tmt").get().val()
		except Exception as e:
			print("Error while retrieving software tmt: ", e)
			val = None

		return val 


	def get_individual_app_tracking_time(self, app_name):  # returns individual software app tracking time
		# get the sw app data stored under every possible category

		try:
			val = db.child("istt").child(uid).child(app_name).get().val()
		except Exception as e:
			print("Error while retrieving software data: ", e)
			val = None

		return val


	def get_app_data_from_cat(self, app_name, category):  # returns the sw app data stored under given input category

		p_up_str = get_p_up_str(isProductive)
		
		try:
			val = db.child("sa").child(uid).childp(p_up_str).child(category).child(app_name).child("data").get().val()
		except Exception as e:
			print("Error while retrieving software data: ", e)
			val = None

		return val


	def get_mostly_used_apps(self):  # returns mostly used software app names(can be more then one if having same time spent)

		apps_with_time = db.child("istt").child(uid).get().val()  # Oredered Dict
		app_list, time_list = list(apps_with_time.keys()), list(apps_with_time.values())
		
		max_indexes = get_max_time_indexes(time_list)

		max_time_spent = time_list[max_indexes[0]]
		mostly_used_apps = []

		for max_index in max_indexes:
			mostly_used_apps.append(app_list[max_index])

		return mostly_used_apps, max_time_spent



class RetrieveWebsiteData:
	"""Singleton RetrieveWebsiteData class"""

	__instance = None

	@staticmethod
	def getInstance():
		""" Static access method. """
		if RetrieveWebsiteData.__instance == None:
			RetrieveWebsiteData()
		return RetrieveWebsiteData.__instance


	def __init__(self):  # firebase authenticated user fetched from frontend
		""" Virtually private costructor """

		if RetrieveWebsiteData.__instance != None:
			raise Exception("RetrieveWebsiteData is a Singleton Class!")
		else:
			RetrieveWebsiteData.__instance = self


	def get_app_list(self):  # returns web apps list

		# shallow() returns all keys under given path(here iwtt/uid/)
		dict_keys = db.child("iwtt").child(uid).shallow().get().val()

		return list(dict_keys)


	def get_total_tracking_time(self):  # returns total website tracking time
		return db.child("wa").child(uid).child("twtt").get().val()


	def get_total_productive_time(self):  # returns total website productive time
		return db.child("wa").child(uid).child("p").child("twpt").get().val()


	def get_total_unproductive_time(self):  # returns total website unproductive time
		return db.child("wa").child(uid).child("up").child("twupt").get().val()
 		

	def get_total_category_time(self, category):  # returns website total category time

		p_up_str = get_p_up_str(isProductive)
		
		return db.child("wa").child(uid).child(p_up_str).child(category).child("tct").get().val()


	def get_total_mutual_time_in_category(self, hostname, category, isProductive):  # returns website total mutual time in given category
		
		p_up_str = get_p_up_str(isProductive)
			
		try:
			val = db.child("wa").child(uid).child(p_up_str).child(category).child(hostname).child("tmt").get().val()
		except Exception as e:
			print("Error while retrieving website tmt: ", e)
			val = None

		return val


	def get_individual_app_tracking_time(self, hostname):  # ireturns ndividual website app tracking time
		# get the sw app data stored under every possible category

		try:
			val = db.child("iwtt").child(uid).child(hostname).get().val()
		except Exception as e:
			print("Error while retrieving website data: ", e)
			val = None

		return val


	def get_data(self, hostname, category):  # returns web app data stored under given input category
		
		p_up_str = get_p_up_str(isProductive)
			
		try:
			val = db.child("wa").child(uid).child(p_up_str).child(category).child(hostname).child("url+title").get().val()
		except Exception as e:
			print("Error while retrieving website data: ", e)
			val = None

		return val


	def get_mostly_used_apps(self):  # returns mostly used software app names(can be more then one if having same time spent)

		apps_with_time = db.child("iwtt").child(uid).get().val()  # Oredered Dict
		app_list, time_list = list(apps_with_time.keys()), list(apps_with_time.values())
		
		max_indexes = get_max_time_indexes(time_list)

		max_time_spent = time_list[max_indexes[0]]
		mostly_used_apps = []
		for max_index in max_indexes:
			mostly_used_apps.append(app_list[max_index])

		return mostly_used_apps, max_time_spent


class RetrieveTrackingHistory:
	"""docstring for RetrieveTrackingHistory"""

	def __init__(self):
		"""Singleton RetrieveTrackingHistory class"""

	__instance = None

	@staticmethod
	def getInstance():
		""" Static access method. """
		if RetrieveTrackingHistory.__instance == None:
			RetrieveTrackingHistory()
		return RetrieveTrackingHistory.__instance


	def __init__(self):  # firebase authenticated user fetched from frontend
		""" Virtually private costructor """

		if RetrieveTrackingHistory.__instance != None:
			raise Exception("RetrieveTrackingHistory is a Singleton Class!")
		else:
			RetrieveTrackingHistory.__instance = self


	def get_all_ind_day_tracking_dates(self):  # returns all individual day tracking dates
		return db.child("uth").child(uid).child("id").shallow().get().val()


	def get_ind_day_tracking_times(self, date):  # returns particular individual day tracking times
		return db.child("uth").child(uid).child("id").child(date).get().val()

	
	def get_all_days_tracking_times(self):  # returns tracking times stored in all_days
		return db.child("uth").child(uid).child("ads").get().val()


	def get_oldest_tracking_date(self):  # returns date of oldest day stored in tracking history
		return db.child("uth").child(uid).child("otd").get().val()


retrieve_sw_data = RetrieveSoftwareData.getInstance()
retrieve_web_data = RetrieveWebsiteData.getInstance()