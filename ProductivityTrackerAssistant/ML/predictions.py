"""
DOCSTRINGS
"""


# Standard library imports
from __future__ import print_function
import json
import os


# Third party imports
import requests


# Local application imports
from ..Constants.keys import *

# Any one of the two below classes(DockerPrediction or CloudPrediction) can be used to make predictions.
from .cloudPredictions import CloudPrediction
from .dockerPredictions import DockerPrediction
from ..print_colored_text import *


# A list of class into which websites are categorized
productive=[c for i,c in PRODUCTIVE_STR.items()]
unproductive=[c for i,c in UNPRODUCTIVE_STR.items()]


class Prediction:

	__instance = None

	@staticmethod
	def getInstance():
		""" Static access method. """

		if Prediction.__instance == None:
			Prediction()
		return Prediction.__instance


	def __init__(self):
		""" Virtually private costructor """

		if Prediction.__instance != None:
			raise Exception("Prediction is a Singleton Class")
		else:
			Prediction.__instance = self


	def set_prediction_class(self):
		predictor = None
		if os.getenv("prediction_mode") == "1":
			predictor = CloudPrediction.getInstance()
		else:
			predictor = DockerPrediction.getInstance()  # default predictor
		return predictor


class WebsitePrediction(Prediction):

	def __init__(self, url):
		self.predictor = Prediction.getInstance().set_prediction_class()
		self.url = url


	def get_website_prediction(self, webInfoObject):

		title, description = webInfoObject.get_title_and_desc()
		try:
			# print("title:",title)
			# print("description:",description)
			pass
		except Exception as e:
			print_exception_text(e)

		input_text = webInfoObject.get_text()
		input_text = webInfoObject.clean_text(input_text)
		result = None
		if input_text == None:
			print_warning_text("Prediction: Others")
			result = OTHERS_STR
		else:  
			result = self.predictor.predict(input_text)

		return result


	def is_productive(self, class_val):

		isProductive = class_val in productive
		print_info_text("isProductive: {}".format(isProductive))

		return isProductive


class SoftwarePrediction(Prediction):

	def __init__(self, text):
		self.predictor = Prediction.getInstance().set_prediction_class()
		self.text = text


	def get_software_prediction(self):
		result = None
		if self.text == None or self.text == "":
			print_warning_text("Prediction: Others")
			result = OTHERS_STR
		else:  
			# print("Text: ", self.text)
			result = self.predictor.predict(self.text)
			# print("Result: ", result)

		return result
        

	def is_productive(self,class_val):
		isProductive = class_val in productive
		print_info_text("isProductive: {}".format(isProductive))
		
		return isProductive

