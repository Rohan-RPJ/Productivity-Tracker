
import datetime
import json
from dateutil import parser
from json.decoder import JSONDecodeError
class AcitivyList:
    def __init__(self, activities):
        self.activities = activities
#        json.dumps(self.activities)
    def initialize_me(self):
            activity_list = AcitivyList([])
            with open('activities.json', 'r') as f:
                #data = json.load(f)
                #rint("type: ",type(data))
                #print("dict:", data)
                activity_list = AcitivyList(
                    activities = self.get_activities_from_json(data)
                )
            return activity_list

    def get_activities_from_json(self, data):
        return_list = []
        for activity in data['activities']:
            return_list.append(
                Activity(
                    name = activity['name'],
                    time_entries = self.get_time_entires_from_json(activity),
                )
            )
        self.activities = return_list
        return return_list

    def get_time_entires_from_json(self, data):
        return_list = []
        for entry in data['time_entries']:
            return_list.append(
                TimeEntry(
                    start_time = parser.parse(entry['start_time']),
                    end_time = parser.parse(entry['end_time']),
                    days = entry['days'],
                    hours = entry['hours'],
                    minutes = entry['minutes'],
                    seconds = entry['seconds'],
                )
            )
        self.time_entries = return_list
        return return_list

    def serialize(self):
        return {
            'activities' : self.activities_to_json()
        }

    def activities_to_json(self):
        activities_ = [{'SOFTWARE':{}},{'WEBSITE TRACKING':{'Mozilla Firefox':{},'Google Chrome':{}}}]
        for activity in self.activities:
            full_detail = activity.name
            if full_detail == None:
                continue
            else:
                detail_list = full_detail.split(' - ')
                new_window_name = detail_list[-1]
            if new_window_name == 'Mozilla Firefox\'' or new_window_name == 'Google Chrome\'':
                #print('Inside activity: ', new_window_name)
                activities_ = activity.serialize_browser(new_window_name)
            else:
                activities_ = activity.serialize()
        return activities_


class Activity:
    def __init__(self, name, time_entries):
        self.name = name
        self.time_entries = time_entries

    def serialize(self):
        f = open('activities.json', 'r+')
        data = json.load(f)
        f.close()
        #print(data['activities'][0]['SOFTWARE'])
        data['activities'][0]['SOFTWARE'].update({
                (self.name) : {'time_entries' : self.make_time_entires_to_json()}
            })
        #print(data['activities'][0]['SOFTWARE'])

        '''f1 = open('activities.json', 'w+')
        json.dump(data, f1,
            indent=4, sort_keys=True)
        #return{
        #    "SOFTWARE":{
        #        'name' : self.name,
        #        'time_entries' : self.make_time_entires_to_json()
        #    }
        #}
        f1.close()
        return '''
        return data['activities']

    def serialize_browser(self, new_window_name):
        f = open('activities.json', 'r+')
        data = json.load(f)
        f.close()
        #print(data)
        if new_window_name == 'Mozilla Firefox\'':
            data['activities'][1]['WEBSITE TRACKING']['Mozilla Firefox'].update({
                (self.name) : {'time_entries' : self.make_time_entires_to_json()}
            })

        if new_window_name == 'Google Chrome\'':
            data['activities'][1]['WEBSITE TRACKING']['Google Chrome'].update({
                (self.name) : {'time_entries' : self.make_time_entires_to_json()}
            })
        '''f1 = open('activities.json', 'w+')
        json.dump(data, f1,
            indent=4, sort_keys=True)
        f1.close()'''
        return data['activities']

        #print("SERIALIZE_BROWSER: ",new_window_name)

    def make_time_entires_to_json(self):
        time_list = []
        for time in self.time_entries:
            time_list.append(time.serialize())
        return time_list


class TimeEntry:
    def __init__(self, start_time, end_time, days, hours, minutes, seconds):
        self.start_time = start_time
        self.end_time = end_time
        self.total_time = end_time - start_time
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def _get_specific_times(self):
        self.days, self.seconds = self.total_time.days, self.total_time.seconds
        self.hours = self.days * 24 + self.seconds // 3600
        self.minutes = (self.seconds % 3600) // 60
        self.seconds = self.seconds % 60

    def serialize(self):
        return {
            'start_time' : self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time' : self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'days' : self.days,
            'hours' : self.hours,
            'minutes' : self.minutes,
            'seconds' : self.seconds
        }
