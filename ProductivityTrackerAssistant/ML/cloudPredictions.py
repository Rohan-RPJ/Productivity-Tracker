"""
The text classifier model is deployed and hosted on a cloud service platform called Algorithmia,
which specializes AAAS i.e. Algorithm As A Service.
An algorithm is running on the cloud platform Algorithmia which loads the saved text classifier model
and makes predictions using that classifer model.

To make predictions from remote:
1. Run this file
2. For other methods: https://teams.algorithmia.com/algorithms/textclassifier

"""


# Standard library imports


# Third party imports
import Algorithmia

# Local application imports
from ..Constants.keys import OTHERS_STR



class CloudPrediction:

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CloudPrediction.__instance == None:
            CloudPrediction()
        return CloudPrediction.__instance


    def __init__(self):
        """ Virtually private costructor """

        if CloudPrediction.__instance != None:
            raise Exception("CloudPrediction is a Singleton Class!")
        else:
            print("############## RUNNING CLOUD PREDICTIONS ##############")
            CloudPrediction.__instance = self
            # Authenticate with your API key
            self.__apiKey = "simq9Ll7v5kyBNOciWBu2d1A/PH1"

            # Create the Algorithmia client object
            self.__client = Algorithmia.client(self.__apiKey)


    def predict(self, input_text):
        # Create the algorithm object using the Summarizer algorithm
        algo = self.__client.algo('ProductivityTrackerAssistant/textclassifier/1.0.0')
        result = OTHERS_STR
        try:
            # Get the result
            result = algo.pipe(input_text).result
        except Exception as error:
            # Algorithm error if, for example, the input is not correctly formatted
            print(error)

        return result