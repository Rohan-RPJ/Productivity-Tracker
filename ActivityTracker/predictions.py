from __future__ import print_function
import json
import requests

from data import *
from keys import *

# The server URL specifies the endpoint of your server running the ResNet
# model with the name "model" and using the predict interface.
SERVER_URL = 'http://localhost:8501/v1/models/model:predict'

# A list of class into which websites are categorized
classes=[c for i,c in SUBCLASSES_STR.items()]
productive=[c for i,c in PRODUCTIVE_STR.items()]
unproductive=[c for i,c in UNPRODUCTIVE_STR.items()]


class WebsitePrediction:

    def __init__(self, url):
        self.url = url
        # get input data or input text i.e. title+desc
        self.webInfo = WebsiteInfo(self.url)

    def get_website_prediction(self):

        title, description = self.webInfo.get_title_and_desc()
        try:
          print("title:",title)
          print("description:",description)
        except Exception as e:
          print(e)

        input_text = self.webInfo.get_text()
        input_text = self.webInfo.clean_text(input_text)
        if input_text == None:
            print("Prediction: Others")

            return OTHERS_STR
        else:  
          # Compose a JSON Predict request (send title+desc of webpage).
          data = json.dumps({"instances" : [input_text]})

          json_response = requests.post(SERVER_URL, data=data)

          # Extract text from JSON
          response_text = json.loads(json_response.text)

          # get prediction values for each class
          predicted_values = response_text["predictions"][0]
          #print(predicted_values)

          max_value_index = predicted_values.index(max(predicted_values))
          prediction1 = classes[max_value_index]
          print("Predction1:", prediction1)

          predicted_values[max_value_index] = -100
          sec_max_val_index = predicted_values.index(max(predicted_values))
          prediction2 = classes[sec_max_val_index]
          print("Predction2:", prediction2)

          return prediction1

    def is_productive(self,class_val):
        isProductive = class_val in productive
        print("isProductive", isProductive)
        return isProductive


class SoftwarePrediction:

    def __init__(self, text):
        self.text = text

    def get_software_prediction(self):
        if self.text == None or self.text == "":
            print("Prediction: Others")

            return OTHERS_STR
        else:  
          # Compose a JSON Predict request (send title+desc of webpage).
          data = json.dumps({"instances" : [self.text]})

          json_response = requests.post(SERVER_URL, data=data)

          # Extract text from JSON
          response_text = json.loads(json_response.text)

          # get prediction values for each class
          predicted_values = response_text["predictions"][0]
          #print(predicted_values)

          max_value_index = predicted_values.index(max(predicted_values))
          prediction1 = classes[max_value_index]
          print("Predction1:", prediction1)

          predicted_values[max_value_index] = -1
          sec_max_val_index = predicted_values.index(max(predicted_values))
          prediction2 = classes[sec_max_val_index]
          print("Predction2:", prediction2)

          return prediction1

        return prediction1

        

    def is_productive(self,class_val):
        isProductive = class_val in productive
        print("isProductive", isProductive)
        return isProductive

