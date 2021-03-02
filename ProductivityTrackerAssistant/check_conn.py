import requests
import json



def checkInternetConn(url='http://www.google.com/', timeout=3):
    
    try:
        #r = requests.get(url, timeout=timeout)
        r = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError as ex:
        return False


def checkDockerConn():
	
	SERVER_URL = 'http://localhost:8501/v1/models/model:predict'

	data = json.dumps({"instances" : ["sample_input"]})
	headers = {"content-type": "application/json"}

	try:
		json_response = requests.post(SERVER_URL, data=data, headers=headers)
	except requests.ConnectionError as e:
		return False

	return True


