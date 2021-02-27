"""
DOCSTRINGS
"""

# Standard library imports
from collections import defaultdict
import datetime
import json
from json.decoder import JSONDecodeError


# Third party imports
from dateutil import parser


# Local application imports
from ...Constants.keys import *
from ...Database.JsonDatabase.jsonDB import JsonDB



jsondb = JsonDB.getInstance()
# print("Inside act", jsondb)
url_title_separator = "-*-"
storageFilename = "activities.json"


class WinAcitivyList:
    def __init__(self, activities):
        self.activities = activities


    def initialize_me(self, data):
        jsondb.store_data(data, storageFilename)


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
    def __init__(self, key, time_spent, prediction_results):
        self.key = key
        self.time_spent = time_spent
        self.category = prediction_results["category"]
        self.isProductive = prediction_results["isProductive"]


    def initWebsite(self, name, title):
        self.name = name
        self.title = title


    def initSoftware(self, name):
        self.name = name
        self.title = None


    def serialize_software(self):

        data = jsondb.retrieve_data(storageFilename)
        
        isProd = str(int(self.isProductive))
        cat = self.category
        print("isProd",CLASSES_STR[isProd]," cat",cat)

        if cat == OTHERS_STR:
            data[ACTIVITY_STR][2][cat].update({
                (self.key) : {TIME_SPENT_STR : self.time_spent}
            })
        else:
            # here key is appname
            stored_app_data = data[ACTIVITY_STR][0][SOFTWARE_STR][CLASSES_STR[isProd]][cat]
            stored_app_data = defaultdict(str, stored_app_data)
            if stored_app_data[self.key] != "":
                # 
                total_mutual_time = stored_app_data[self.key][TIME_SPENT_STR]
                print("Total mutual time: ",total_mutual_time)
                print("Time Spent: ",  self.time_spent)
                stored_app_data[self.key][TIME_SPENT_STR] = self.add_time(total_mutual_time, self.time_spent)

                # print("store_site_data::",store_site_data)
                data[ACTIVITY_STR][0][SOFTWARE_STR][CLASSES_STR[isProd]][cat] = stored_app_data

            else:

                data[ACTIVITY_STR][0][SOFTWARE_STR][CLASSES_STR[isProd]][cat].update({
                    (self.key) : {
                        TIME_SPENT_STR : self.time_spent
                    }
                })

        #print("::::::::::::::::::::::::\n",data['activities'][0]['SOFTWARE'],"\n::::::::::::::::::::::::::::")
        return data[ACTIVITY_STR]


    def serialize_browser(self):
        
        data = jsondb.retrieve_data('activities.json')
        
        isProd = str(int(self.isProductive))
        cat = self.category
        # print("Dattaaaaaaa: ",type(data))
        if cat == OTHERS_STR:
            data[ACTIVITY_STR][2][cat].update({
                (self.name) : {TIME_SPENT_STR : self.time_spent}
            })
        else:
            # here key is hostname
            url = self.name.split(' - ')[0]
            stored_site_data = data[ACTIVITY_STR][1][WEBSTIE_STR][CLASSES_STR[isProd]][cat]
            stored_site_data = defaultdict(str, stored_site_data)
            if stored_site_data[self.key] != "":

                # 
                total_mutual_time = stored_site_data[self.key][TIME_SPENT_STR]
                print("Total mutual time: ",total_mutual_time)
                print("Time Spent: ",  self.time_spent)
                stored_site_data[self.key] = self.__append_site_data(stored_site_data, url, total_mutual_time)

                # print("store_site_data::",store_site_data)
                data[ACTIVITY_STR][1][WEBSTIE_STR][CLASSES_STR[isProd]][cat] = stored_site_data

            else:

                data[ACTIVITY_STR][1][WEBSTIE_STR][CLASSES_STR[isProd]][cat].update({
                    (self.key) : {
                        # URL_STR : self.name.split(' - ')[0],
                        # TITLE_STR : self.title,
                        TIME_SPENT_STR : self.time_spent,
                        URL_STR+"+"+TITLE_STR : [url + url_title_separator + self.title]
                    }
                })

        return data[ACTIVITY_STR]


    def __append_site_data(self, stored_site_data, url, total_mutual_time):
        site_data = stored_site_data[self.key]
        # print("sitedata::",site_data)
        site_data[TIME_SPENT_STR] = self.add_time(self.time_spent, total_mutual_time)
        sites_list = set(site_data[URL_STR+"+"+TITLE_STR])
        sites_list.add(url+url_title_separator+self.title)
        sites_list = list(sites_list)
        # print("siteslist::",sites_list)
        site_data[URL_STR+"+"+TITLE_STR] = sites_list
        return site_data


    def add_time(self, t1, t2):  # time t1 and t2 will be in 'x-h x-m x-s' format
        t1_h, t1_m, t1_s = [int(t.split('-')[0]) for t in t1.split()]
        t2_h, t2_m, t2_s = [int(t.split('-')[0]) for t in t2.split()]
        secs = (t1_s + t2_s)
        mins = (t1_m + t2_m + secs//60)
        hrs = (t1_h + t2_h + mins//60)
        secs %= 60
        mins %= 60
        time_spent = str(hrs) + "-h " + str(mins) + "-m " + str(secs)+ "-s"

        return time_spent


    def set_time_spent(self, time_entry):
        # old_time = [int(t.split('-')[0]) for t in self.time_spent.split()]
        # old_hr, old_min, old_sec = old_time
        # new_hr, new_min, new_sec = time_entry.get_hours(),time_entry.get_minutes(),time_entry.get_seconds()
        # secs = (old_sec + new_sec)
        # mins = (old_min + new_min + secs//60)
        # hrs = (old_hr + new_hr + mins//60)
        # secs %= 60
        # mins %= 60
        # self.time_spent = str(hrs) + "-h " + str(mins) + "-m " + str(secs)+ "-s"
        hrs, mins, secs = time_entry.get_hours(),time_entry.get_minutes(),time_entry.get_seconds()
        self.time_spent = str(hrs) + "-h " + str(mins) + "-m " + str(secs)+ "-s"
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
        return str(self.hours) + "-h " + str(self.minutes) + "-m " + str(self.seconds)+ "-s"