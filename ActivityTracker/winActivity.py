import datetime
import json
from dateutil import parser
from json.decoder import JSONDecodeError
from keys import *

class WinAcitivyList:
    def __init__(self, activities):
        self.activities = activities

    def initialize_me(self, data):
            with open('activities.json', 'w') as f:
                json.dump(data, f,indent=4, sort_keys=True)

    def get_activities_from_json(self, data):
        return_list = []
        for activity in data[ACTIVITY_STR]:
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

    def serialize(self, activity):
        return {
            ACTIVITY_STR : self.activities_to_json(activity)
        }

    def activities_to_json(self,activity):
        activities_ = []
        #activities_ = [{'SOFTWARE':{}},{'WEBSITE TRACKING':{'Mozilla Firefox':{},'Google Chrome':{}}}]
        #for activity in self.activities:
        full_detail = activity.name
        if full_detail == None:
            #continue
            return []
        else:
            detail_list = full_detail.split(' - ')
            new_window_name = detail_list[-1]
        if new_window_name == 'Mozilla Firefox' or new_window_name == 'Google Chrome' or new_window_name == 'Microsoft Edge':
            #print('Inside activity: ', new_window_name)
            activities_ = activity.serialize_browser()
        else:
            activities_ = activity.serialize_software()
        return activities_


class WinActivity:
    def __init__(self, name, time_spent, category, isProductive, **activity_info):
        self.name = name
        self.time_spent = time_spent
        self.category = category
        self.isProductive = isProductive
        self.title = activity_info["title"]

    def serialize_software(self):

        with open('activities.json', 'r') as f:
            data = json.load(f)
        
        isProd = str(int(self.isProductive))
        cat = self.category
        print("isProd",CLASSES_STR[isProd]," cat",cat)

        if cat == OTHERS_STR:
            data[ACTIVITY_STR][2][cat].update({
                (self.name) : {TIME_SPENT_STR : self.time_spent}
            })
        else:
            data[ACTIVITY_STR][0][SOFTWARE_STR][CLASSES_STR[isProd]][cat].update({
                (self.name) : {TIME_SPENT_STR : self.time_spent}
            })

        #print("::::::::::::::::::::::::\n",data['activities'][0]['SOFTWARE'],"\n::::::::::::::::::::::::::::")
        return data[ACTIVITY_STR]


    def serialize_browser(self):
        
        with open('activities.json', 'r') as f:
            data = json.load(f)
        
        isProd = str(int(self.isProductive))
        cat = self.category
        
        if cat == OTHERS_STR:
            data[ACTIVITY_STR][2][cat].update({
                (self.name) : {TIME_SPENT_STR : self.time_spent}
            })
        else:
            data[ACTIVITY_STR][1][WEBSTIE_STR][CLASSES_STR[isProd]][cat].update({
                (self.name.split(' - ')[0]) : {
                    TITLE_STR : self.title,
                    TIME_SPENT_STR : self.time_spent
                }
            })

        return data[ACTIVITY_STR]


    def make_time_entires_to_json(self, time_entry):
        old_time = [int(t[:len(t)-1]) for t in self.time_spent.split()]
        old_hr, old_min, old_sec = old_time[0],old_time[1],old_time[2]
        new_hr, new_min, new_sec = time_entry.get_hours(),time_entry.get_minutes(),time_entry.get_seconds()
        secs = (old_sec + new_sec)
        mins = (old_min + new_min + secs//60)
        hrs = (old_hr + new_hr + mins//60)
        secs %= 60
        mins %= 60
        self.time_spent = str(hrs) + "h " + str(mins) + "m " + str(secs)+ "s"
        return self.time_spent


class WinTimeEntry:
    def __init__(self, start_time, end_time, days, hours, minutes, seconds):
        self.start_time = start_time
        self.end_time = end_time
        self.total_time = end_time - start_time
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def _set_specific_times(self):
        self.days, self.seconds = self.total_time.days, self.total_time.seconds
        self.hours = self.days * 24 + self.seconds // 3600
        self.minutes = (self.seconds % 3600) // 60
        self.seconds = self.seconds % 60

    def get_days(self):
        return self.days

    def get_hours(self):
        return self.hours

    def get_minutes(self):
        return self.minutes

    def get_seconds(self):
        return self.seconds

    def serialize(self):
        # return {
        #     'start_time' : self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
        #     'end_time' : self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
        #     'days' : self.days,
        #     'hours' : self.hours,
        #     'minutes' : self.minutes,
        #     'seconds' : self.seconds
        # }
        return str(self.hours) + "h " + str(self.minutes) + "m " + str(self.seconds)+ "s"
        
