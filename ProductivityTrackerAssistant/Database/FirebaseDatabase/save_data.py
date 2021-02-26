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

		self.__initIdsFromDB()

		isDBCleared = db.child("users").child(self.uid).child("isDBCleared").get().val()

		if isDBCleared == "f":
			# to initialize (web and sw)+(prod and unprod) data ids from db
			self.__init_application_data_ids_from_db()

			return "Database already initialized"

		# Initialize data in database - START #

		# to initialize (web and sw)+(prod and unprod) data ids in db
		self.__init_application_data_ids_in_db()

		# to initialize all tracking times in db
		self.__init_tracking_times_in_db()

		# Initialize data in database - END #

		isDBCleared = db.child("users").child(self.uid).child("isDBCleared").set("f")

		return "Database initialized successfully"


	def __initIdsFromDB(self):
		# Initialize ids from database - START #

		# sid and wid will be stored in electron js.. so no need of if stmt
		# if db.child("users").child(self.uid).child("sid").get().val() == None:
		# 	self.sid = db.child("users").child(self.uid).child("sid").set(self.__get_timestamp())
		# else:
		self.sid = db.child("users").child(self.uid).child("sid").get().val()

		# if db.child("users").child(self.uid).child("wid").get().val() == None:
		# 	self.wid = db.child("users").child(self.uid).child("wid").set(self.__get_timestamp())
		# else:
		self.wid = db.child("users").child(self.uid).child("wid").get().val()

		# Initialize ids from database - END #


	def __init_application_data_ids_in_db(self):

		# initialize productive software data id
		self.psdid = db.child("sa").child(self.sid).child("p").child("psdid").set(self.__get_timestamp())

		# initialize unproductive software data id
		self.upsdid = db.child("sa").child(self.sid).child("up").child("upsdid").set(self.__get_timestamp())

		# initialize productive website data id
		self.pwdid = db.child("wa").child(self.wid).child("p").child("pwdid").set(self.__get_timestamp())

		# initialize unproductive website data id
		self.upwdid = db.child("wa").child(self.wid).child("up").child("upwdid").set(self.__get_timestamp())


	def __init_application_data_ids_from_db(self):

		# initialize productive software data id
		self.psdid = db.child("sa").child(self.sid).child("p").child("psdid").get().val()

		# initialize unproductive software data id
		self.upsdid = db.child("sa").child(self.sid).child("up").child("upsdid").get().val()

		# initialize productive website data id
		self.pwdid = db.child("wa").child(self.wid).child("p").child("pwdid").get().val()

		# initialize unproductive website data id
		self.upwdid = db.child("wa").child(self.wid).child("up").child("upwdid").get().val()


	def __init_tracking_times_in_db(self):

		# initialize total tracking time
		db.child("users").child(self.uid).child("ttt").set(initial_time)

		# initialize total software tracking time
		db.child("sa").child(self.sid).child("tstt").set(initial_time)

		# initialize total website tracking time
		db.child("wa").child(self.wid).child("twtt").set(initial_time)

		# initialize total software productive time
		db.child("sa").child(self.sid).child("p").child("tspt").set(initial_time)

		# initialize total software unproductive time
		db.child("sa").child(self.sid).child("up").child("tsupt").set(initial_time)

		# initialize total website productive time
		db.child("wa").child(self.wid).child("p").child("twpt").set(initial_time)

		# initialize total website unproductive time
		db.child("wa").child(self.wid).child("up").child("twupt").set(initial_time)

		# initialize total category time for all productive category
		for p_cat in productive:
			db.child("sd").child(self.psdid).child(p_cat).child("tct").set(initial_time)
			db.child("wd").child(self.pwdid).child(p_cat).child("tct").set(initial_time)

		# initialize total category time for all unproductive category
		for up_cat in unproductive:
			db.child("sd").child(self.upsdid).child(up_cat).child("tct").set(initial_time)
			db.child("wd").child(self.upwdid).child(up_cat).child("tct").set(initial_time)


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
		web_sw_id = None
		p_up_web_sw_did = None
		
		# storing web or software data
		# here self.activity.key is hostname for website and app_name for software
		if self.activity.isBrowser:

			if self.store_web_data() == 0:
				return

			web_sw_str = "w"
			web_sw_id = self.wid
			if self.activity.isProductive:
				p_up_web_sw_did = self.pwdid
			else:
				p_up_web_sw_did = self.upwdid

		else:

			if self.store_sw_data() == 0:
				return

			web_sw_str = "s"
			web_sw_id = self.sid
			if self.activity.isProductive:
				p_up_web_sw_did = self.psdid
			else:
				p_up_web_sw_did = self.upsdid

		if self.activity.isProductive:
			p_up_str = "p" 
		else:
			p_up_str = "up"

		# get total mutual time
		try:
			tmt = db.child("{}d".format(web_sw_str)).child(p_up_web_sw_did).child(self.activity.category).child(self.activity.key).child("tmt").get().val()
		except Exception as e:
			print("Exception while getting tmt value in SaveData: ", e)
			return
			
		if tmt == None:
			tmt = self.activity.add_time(self.activity.time_spent, initial_time)
		else:
			tmt = self.activity.add_time(self.activity.time_spent, tmt)
		
		# update total mutual time
		db.child("{}d".format(web_sw_str)).child(p_up_web_sw_did).child(self.activity.category).child(self.activity.key).update({"tmt": tmt})

    	# get total category time
		tct = db.child("{}d".format(web_sw_str)).child(p_up_web_sw_did).child(self.activity.category).child("tct").get().val()
		tct = self.activity.add_time(self.activity.time_spent, tct)
		
		# update total category time
		db.child("{}d".format(web_sw_str)).child(p_up_web_sw_did).child(self.activity.category).update({"tct": tct})

		# update rest of the tracking times
		self.update_tracking_times(p_up_str, web_sw_str, web_sw_id)


	def store_web_data(self):
		if not self.activity.is_website_stored:
			url = self.activity.name.split(' - ')[0]

			# add url + title to db
			try:
				if self.activity.isProductive:
					db.child("wd").child(self.pwdid).child(self.activity.category).child(self.activity.key).child("url+title").child(self.__get_timestamp()).set(url + url_title_separator + self.activity.title)
				else:
					db.child("wd").child(self.upwdid).child(self.activity.category).child(self.activity.key).child("url+title").child(self.__get_timestamp()).set(url + url_title_separator + self.activity.title)
			except Exception as e:
				print("Exception while storing web data: ", e)
				return 0
		return 1


	def store_sw_data(self):

		if not self.activity.is_software_stored:

			# add app_data to db
			try:
				if self.activity.isProductive:
					db.child("sd").child(self.psdid).child(self.activity.category).child(self.activity.key).child("data").set(self.activity.name)
				else:
					db.child("sd").child(self.upsdid).child(self.activity.category).child(self.activity.key).child("data").set(self.activity.name)
			except Exception as e:
				print("Exception while storing software data: ", e)
				return 0
		return 1


	def update_tracking_times(self, p_up_str, web_sw_str, web_sw_id):

		# website_or_software_activities("wa" or "sa") string stored in db
		wa_sa_str = "{}a".format(web_sw_str)

		# total app prod or unprod time str("twpt" or "twupt" or "tspt" or "tsupt"). here app can be website or software
		tot_app_p_up_time_str = "t{}{}t".format(web_sw_str, p_up_str)

		# total app tracking time. Here app can be website or a software
		tot_app_tracking_time_str = "t{}tt".format(web_sw_str)

		# total tracking time
		tot_tracking_time_str = "ttt"

		# print(tot_app_tracking_time_str, tot_app_p_up_time_str, tot_tracking_time_str)
		# raise Exception

		# get total web or sw p or up time
		tot_app_p_up_time = db.child(wa_sa_str).child(web_sw_id).child(p_up_str).child(tot_app_p_up_time_str).get().val()

		# get total web or sw tracking time
		tot_app_tracking_time = db.child(wa_sa_str).child(web_sw_id).child(tot_app_tracking_time_str).get().val()

		# get total tracking time
		tot_tracking_time = db.child("users").child(self.uid).child(tot_tracking_time_str).get().val()
		  
		# print(tot_app_p_up_time, tot_app_tracking_time, tot_tracking_time)
		# raise Exception

		# print(self.activity.add_time(self.activity.time_spent, tot_app_p_up_time))
		# print(self.activity.add_time(self.activity.time_spent, tot_app_tracking_time))
		# print(self.activity.add_time(self.activity.time_spent, tot_tracking_time))
		# raise Exception

		db.update({
		    wa_sa_str+'/'+str(web_sw_id)+'/'+tot_app_tracking_time_str: self.activity.add_time(self.activity.time_spent, tot_app_tracking_time)
		})

		db.update({
		    wa_sa_str+'/'+str(web_sw_id)+'/'+p_up_str+'/'+tot_app_p_up_time_str: self.activity.add_time(self.activity.time_spent, tot_app_p_up_time)
		})

		db.update({
		    "users/"+str(user.uid)+'/'+tot_tracking_time_str: self.activity.add_time(self.activity.time_spent, tot_tracking_time)
		})