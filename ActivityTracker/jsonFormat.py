from keys import *

def get_json_format():
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

