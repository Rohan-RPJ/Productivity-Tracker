"""
DOCSTRINGS
"""


# Standard library imports
import calendar  # to generate unix time stamp from gmt
import time  # to get gmt time


# Third party imports
from . import db


# Local application imports
from ...Constants.keys import *



initial_time = "0-h 0-m 0-s"
url_title_separator = "-*-"

# A list of class into which websites are categorized
productive=[c for i,c in PRODUCTIVE_STR.items()]
unproductive=[c for i,c in UNPRODUCTIVE_STR.items()]


class user:
	uid = 123

class SaveData:
	"""Singleton SaveData class"""

	__instance = None

	@staticmethod
	def getInstance():
		""" Static access method. """
		if SaveData.__instance == None:
			SaveData()
		return SaveData.__instance


	def __init__(self):  # firebase authenticated user fetched from frontend
		""" Virtually private costructor """
		
		if SaveData.__instance != None:
			raise Exception("SaveData is a Singleton Class!")
		else:
			SaveData.__instance = self

			self.uid = user.uid
			self.activity = None


	def __get_timestamp(self): 
		time.sleep(1)
		# gmt stores current gmtime 
		gmt = time.gmtime() 
		# print("gmt:-", gmt) 

		# ts stores timestamp 
		ts = calendar.timegm(gmt) 
		# print("timestamp:-", ts) 

		return ts

			
	def initDB(self):

		# self.__initIdsFromDB()

		isDBCleared = db.child("users").child(self.uid).child("isDBCleared").get().val()

		if isDBCleared == "f":
			return "Database already initialized"

		# Initialize data in database - START #

		# to initialize all tracking times in db
		self.__init_tracking_times_in_db()

		# Initialize data in database - END #

		isDBCleared = db.child("users").child(self.uid).child("isDBCleared").set("f")

		return "Database initialized successfully"


	def __init_tracking_times_in_db(self):

		# initialize total tracking time
		db.child("users").child(self.uid).child("ttt").set(initial_time)

		# initialize total software tracking time
		db.child("sa").child(self.uid).child("tstt").set(initial_time)

		# initialize total website tracking time
		db.child("wa").child(self.uid).child("twtt").set(initial_time)

		# initialize total software productive time
		db.child("sa").child(self.uid).child("p").child("tspt").set(initial_time)

		# initialize total software unproductive time
		db.child("sa").child(self.uid).child("up").child("tsupt").set(initial_time)

		# initialize total website productive time
		db.child("wa").child(self.uid).child("p").child("twpt").set(initial_time)

		# initialize total website unproductive time
		db.child("wa").child(self.uid).child("up").child("twupt").set(initial_time)

		# initialize total category time for all productive category
		for p_cat in productive:
			db.child("sa").child(self.uid).child("p").child(p_cat).child("tct").set(initial_time)
			db.child("wa").child(self.uid).child("p").child(p_cat).child("tct").set(initial_time)

		# initialize total category time for all unproductive category
		for up_cat in unproductive:
			db.child("sa").child(self.uid).child("up").child(up_cat).child("tct").set(initial_time)
			db.child("wa").child(self.uid).child("up").child(up_cat).child("tct").set(initial_time)


	def set_activity(self, activity):
		self.activity = activity


	def save(self): # here activity represents the Activity object
		if self.activity.category == OTHERS_STR:
			return

		if self.activity.name == None:
			return

		self.store_data()


	def store_data(self):

		p_up_str = None
		web_sw_str = None

		if self.activity.isProductive:
			p_up_str = "p" 
		else:
			p_up_str = "up"
		
		# storing web or software data
		# here self.activity.key is hostname for website and app_name for software
		if self.activity.isBrowser:

			if self.store_web_data(p_up_str) == 0:
				return

			web_sw_str = "w"
			
		else:

			if self.store_sw_data(p_up_str) == 0:
				return

			web_sw_str = "s"

		# website_or_software_activities("wa" or "sa") string stored in db
		wa_sa_str = "{}a".format(web_sw_str)

		# get total mutual time
		try:
			tmt = db.child(wa_sa_str).child(self.uid).child(p_up_str).child(self.activity.category).child(self.activity.key).child("tmt").get().val()
		except Exception as e:
			print("Exception while getting tmt value in SaveData: ", e)
			return

		if tmt == None:
			tmt = self.activity.add_time(self.activity.time_spent, initial_time)
		else:
			tmt = self.activity.add_time(self.activity.time_spent, tmt)
		
		# update total mutual time
		db.child(wa_sa_str).child(self.uid).child(p_up_str).child(self.activity.category).child(self.activity.key).update({"tmt": tmt})

    	# get total category time
		tct = db.child(wa_sa_str).child(self.uid).child(p_up_str).child(self.activity.category).child("tct").get().val()
		tct = self.activity.add_time(self.activity.time_spent, tct)
		
		# update total category time
		db.child(wa_sa_str).child(self.uid).child(p_up_str).child(self.activity.category).update({"tct": tct})

		# update rest of the tracking times
		self.update_tracking_times(web_sw_str, p_up_str, wa_sa_str)


	def store_web_data(self, p_up_str):
		if not self.activity.is_website_stored:
			url = self.activity.name.split(' - ')[0]

			# add url + title to db
			try:
				db.child("wa").child(self.uid).child(p_up_str).child(self.activity.category).child(self.activity.key).child("url+title").child(self.__get_timestamp()).set(url + url_title_separator + self.activity.title)
			except Exception as e:
				print("Exception while storing web data: ", e)
				return 0
		return 1


	def store_sw_data(self, p_up_str):

		if not self.activity.is_software_stored:

			# add app_data to db
			try:
				db.child("sa").child(self.uid).child(p_up_str).child(self.activity.category).child(self.activity.key).child("data").set(self.activity.name)
			except Exception as e:
				print("Exception while storing software data: ", e)
				return 0
		return 1


	def update_tracking_times(self, web_sw_str, p_up_str, wa_sa_str):

		
		# total app prod or unprod time str("twpt" or "twupt" or "tspt" or "tsupt"). here app can be website or software
		tot_app_p_up_time_str = "t{}{}t".format(web_sw_str, p_up_str)

		# total app tracking time. Here app can be website or a software
		tot_app_tracking_time_str = "t{}tt".format(web_sw_str)

		# total tracking time
		tot_tracking_time_str = "ttt"

		# print(tot_app_tracking_time_str, tot_app_p_up_time_str, tot_tracking_time_str)
		# raise Exception

		# get total web or sw p or up time
		tot_app_p_up_time = db.child(wa_sa_str).child(self.uid).child(p_up_str).child(tot_app_p_up_time_str).get().val()

		# get total web or sw tracking time
		tot_app_tracking_time = db.child(wa_sa_str).child(self.uid).child(tot_app_tracking_time_str).get().val()

		# get total tracking time
		tot_tracking_time = db.child("users").child(self.uid).child(tot_tracking_time_str).get().val()
		  
		# print(tot_app_p_up_time, tot_app_tracking_time, tot_tracking_time)
		# raise Exception

		# print(self.activity.add_time(self.activity.time_spent, tot_app_p_up_time))
		# print(self.activity.add_time(self.activity.time_spent, tot_app_tracking_time))
		# print(self.activity.add_time(self.activity.time_spent, tot_tracking_time))
		# raise Exception

		db.update({
		    wa_sa_str+'/'+str(self.uid)+'/'+tot_app_tracking_time_str: self.activity.add_time(self.activity.time_spent, tot_app_tracking_time)
		})

		db.update({
		    wa_sa_str+'/'+str(self.uid)+'/'+p_up_str+'/'+tot_app_p_up_time_str: self.activity.add_time(self.activity.time_spent, tot_app_p_up_time)
		})

		db.update({
		    "users/"+str(self.uid)+'/'+tot_tracking_time_str: self.activity.add_time(self.activity.time_spent, tot_tracking_time)
		})

		self.update_individual_app_tracking_time(web_sw_str)


	def update_individual_app_tracking_time(self, web_sw_str):
		# individual website or software tracking time string
		i_w_s_tt_str = "i{}tt".format(web_sw_str)

		# individual website or software tracking time value
		ind_app_tracking_time = db.child(i_w_s_tt_str).child(self.uid).child(self.activity.key).get().val()

		if ind_app_tracking_time is None:
			ind_app_tracking_time = initial_time


		# update individual app(website or software) tracking time
		db.update({
			i_w_s_tt_str+'/'+str(self.uid)+'/'+self.activity.key: self.activity.add_time(self.activity.time_spent, ind_app_tracking_time)
		})