"""
DOCSTRINGS
"""


# Standard library imports


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

class RetrieveData:
	"""Singleton RetrieveData class"""

	__instance = None

	@staticmethod
	def getInstance():
		""" Static access method. """
		if RetrieveData.__instance == None:
			RetrieveData()
		return RetrieveData.__instance


	def __init__(self):  # firebase authenticated user fetched from frontend
		""" Virtually private costructor """
		self.uid = user.uid
		self.sid = db.child("users").child(self.uid).child("sid").get().val()
		self.wid =  db.child("users").child(self.uid).child("sid").get().val()

		if RetrieveData.__instance != None:
			raise Exception("RetrieveData is a Singleton Class!")
		else:
			RetrieveData.__instance = self


	def get_total_tracking_time(self):
		return db.child("users").child(self.uid).child("ttt").get().val()


	############### Get Software Information - START ###############

	def get_total_software_tracking_time(self):
		return db.child("sa").child(self.sid).child("tstt").get().val()


	def get_total_software_productive_time(self):
		return db.child("sa").child(self.sid).child("p").child("tspt").get().val()


	def get_total_software_unproductive_time(self):
		return db.child("sa").child(self.sid).child("up").child("tsupt").get().val()
 

	def __get_productive_software_data_id(self):
		return db.child("sa").child(self.sid).child("p").child("psdid").get().val()


	def __get_unproductive_software_data_id(self):
		return db.child("sa").child(self.sid).child("up").child("upsdid").get().val()
		

	def get_total_software_category_time(self, category):
		p_up_sdid = None
		if category in productive:
			p_up_sdid = self.__get_productive_software_data_id()
		else:
			p_up_sdid = self.__get_unproductive_software_data_id()


		return db.child("sd").child(p_up_sdid).child(category).child("tct").get().val()


	def get_software_app_total_mutual_time(self, app_name, category):
		p_up_sdid = None
		if category in productive:
			p_up_sdid = self.__get_productive_software_data_id()
		else:
			p_up_sdid = self.__get_unproductive_software_data_id()
			
		try:
			val = db.child("sd").child(p_up_sdid).child(category).child(app_name).child("tmt").get().val()
		except Exception as e:
			print("Error while retrieving software tmt: ", e)
			val = None

		return val 


	def get_software_app_data_from_cat(self, app_name, category):
		# get the sw app data stored under given input category

		p_up_sdid = None
		if category in productive:
			p_up_sdid = self.__get_productive_software_data_id()
		else:
			p_up_sdid = self.__get_unproductive_software_data_id()
			
		try:
			val = db.child("sd").child(p_up_sdid).child(category).child(app_name).child("data").get().val()
		except Exception as e:
			print("Error while retrieving software data: ", e)
			val = None

		return val


	# def get_software_app_data(self, app_name):
	# 	# get the sw app data stored under every possible category
		
	# 	p_up_sdid = None
	# 	if category in productive:
	# 		p_up_sdid = self.__get_productive_software_data_id()
	# 	else:
	# 		p_up_sdid = self.__get_unproductive_software_data_id()
			
	# 	try:
	# 		val = db.child("sd").child(p_up_sdid).child(category).child(app_name).child("data").get().val()
	# 	except Exception as e:
	# 		print("Error while retrieving software data: ", e)
	# 		val = None

	# 	return val


	############### Get Software Information - END ###############



	############### Get Website Information - START ###############

	def get_total_website_tracking_time(self):
		return db.child("wa").child(self.wid).child("twtt").get().val()


	def get_total_website_productive_time(self):
		return db.child("wa").child(self.wid).child("p").child("twpt").get().val()


	def get_total_website_unproductive_time(self):
		return db.child("wa").child(self.wid).child("up").child("twupt").get().val()
 

	def __get_productive_website_data_id(self):
		return db.child("wa").child(self.wid).child("p").child("pwdid").get().val()


	def __get_unproductive_website_data_id(self):
		return db.child("wa").child(self.wid).child("up").child("upwdid").get().val()
		

	def get_total_website_category_time(self, category):
		p_up_wdid = None
		if category in productive:
			p_up_wdid = self.__get_productive_website_data_id()
		else:
			p_up_wdid = self.__get_unproductive_website_data_id()


		return db.child("wd").child(p_up_wdid).child(category).child("tct").get().val()


	def get_website_total_mutual_time(self, hostname, category):
		p_up_wdid = None
		if category in productive:
			p_up_wdid = self.__get_productive_webiste_data_id()
		else:
			p_up_wdid = self.__get_unproductive_website_data_id()
			
		try:
			val = db.child("wd").child(p_up_wdid).child(category).child(hostname).child("tmt").get().val()
		except Exception as e:
			print("Error while retrieving website tmt: ", e)
			val = None

		return val


	def get_website_data(self, hostname, category):
		p_up_wdid = None
		if category in productive:
			p_up_wdid = self.__get_productive_website_data_id()
		else:
			p_up_wdid = self.__get_unproductive_website_id()
			
		try:
			val = db.child("wd").child(p_up_wdid).child(category).child(hostname).child("url+title").get().val()
		except Exception as e:
			print("Error while retrieving website data: ", e)
			val = None

		return val

	############### Get Website Information - END ###############


	def get_isDBCleared_val(self):
		return db.child("users").child(self.uid).child("isDBCleared").get().val()
