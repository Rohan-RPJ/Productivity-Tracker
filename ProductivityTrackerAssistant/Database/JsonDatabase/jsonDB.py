"""
DOCSTRINGS
"""


# Standard library imports
import json


# Third party imports
import ijson


# Local application imports
from ...Constants.keys import *



class JsonDB:
	"""Singleton JsonDB class"""

	__instance = None

	@staticmethod
	def getInstance():
		""" Static access method. """
		if JsonDB.__instance == None:
			JsonDB()
		return JsonDB.__instance


	def __init__(self):
		""" Virtually private costructor """

		if JsonDB.__instance != None:
			raise Exception("JsonDB is a Singleton Class!")
		else:
			JsonDB.__instance = self


	# def generate_folders(self):
		


	def get_json_format(self):
		prod_classes = [c for i,c in PRODUCTIVE_STR.items()]
		#print(prod_classes)
		unprod_classes = [c for i,c in UNPRODUCTIVE_STR.items()]
		prod_dict, unprod_dict = {},{}
		for c in prod_classes:
			#print(c)
			prod_dict.update({c: {}})
		for c in unprod_classes:
			unprod_dict.update({c: {}})

		inner_format={
			CLASSES_STR["1"]: prod_dict,
			CLASSES_STR["0"]: unprod_dict,
		}

		data_format = {
			ACTIVITY_STR: [
				{
					SOFTWARE_STR: inner_format
				},
				{
					WEBSTIE_STR: inner_format
				},
				{
					OTHERS_STR: {}
				}
			]
		}

		return data_format


	def store_data(self, json_data, filename):
		with open(filename, 'w', encoding="utf-8") as file_ptr:
			json.dump(json_data, file_ptr, indent=4, sort_keys=True, ensure_ascii=False)


	def retrieve_data(self, filename):
		data = None
		with open(filename, 'r', encoding="utf-8") as file_ptr:
			data = json.load(file_ptr)

		return data