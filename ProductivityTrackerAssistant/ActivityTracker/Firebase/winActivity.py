"""
DOCSTRINGS
"""

# Standard library imports
from collections import defaultdict
import datetime
import os


# Third party imports
from dateutil import parser


# Local application imports
from ...Constants.keys import *
from ...print_colored_text import *



class WinAcitivyList:
    def __init__(self):
        self.sw_activities = ()
        self.web_activities = ()


    def store_activity_list_in_file(self):

        print_local_text("Storing activity List in file...", "yellow")

        __filename = "ACTIVITY_LIST_JSON"

        if os.getenv("db_choice") == "1":
            __filename = "ACTIVITY_LIST_FB"

        try:
            with open(__filename, 'wb') as output_file:

                tot_sw_activities = len(self.sw_activities)
                tot_web_activities = len(self.web_activities)

                output_file.write(bytes(str(tot_sw_activities), encoding='utf-8'))
                output_file.write(bytes('\n', encoding='utf-8'))
                output_file.write(bytes(str(tot_web_activities), encoding='utf-8'))
                output_file.write(bytes('\n', encoding='utf-8'))

                for sw_activity in self.sw_activities:
                    attr_vals = sw_activity.get_class_attributes_values()
                    for data in attr_vals:
                        output_file.write(bytes(str(data).strip(), encoding='utf-8'))
                        output_file.write(bytes('\n', encoding='utf-8'))

                print_info_text("Software activities stored successfully", "green")

                for web_activity in self.web_activities:
                    attr_vals = web_activity.get_class_attributes_values()
                    for data in attr_vals:
                        output_file.write(bytes(str(data).strip(), encoding='utf-8'))
                        output_file.write(bytes('\n', encoding='utf-8'))

                print_info_text("Website activities stored successfully", "green")

        except Exception as e:
            print_exception_text("Exception occurred while storing activities locally: {}".format(e))
            try:
                os.remove(__filename)            
                pass
            except:
                pass


    def __bytes_list_to_str_list(self, bytes_list):
        str_list = []
        for byte_obj in bytes_list:
            str_list.append(byte_obj.decode('utf-8').strip())

        return str_list


    def load_activity_list_from_file(self):

        print_local_text("Loading activities from file...", "yellow")

        isLoadedSuccessfully = False

        __filename = "ACTIVITY_LIST_JSON"

        if os.getenv("db_choice") == "1":
            __filename = "ACTIVITY_LIST_FB"

        try:
            with open(__filename, 'rb') as input_file:

                data = input_file.readlines()

            tot_sw_activities = int(self.__bytes_list_to_str_list([data[0]])[0])
            tot_web_activities = int(self.__bytes_list_to_str_list([data[1]])[0])

            counter = 2

            for _ in range(tot_sw_activities):
                activity = WinActivity(None, None, None)
                attr_vals = self.__bytes_list_to_str_list(data[counter:counter+8])
                activity.load_class_attributes_values(attr_vals)
                self.sw_activities += (activity,)
                counter += 8

            for _ in range(tot_web_activities):
                activity = WinActivity(None, None, None)
                attr_vals = self.__bytes_list_to_str_list(data[counter:counter+8])
                activity.load_class_attributes_values(attr_vals)
                self.web_activities += (activity,)
                counter += 8

            isLoadedSuccessfully = True

            print_local_text("Activities loaded successfully", "green")

        except FileNotFoundError as e:
            print_local_text("{} file not found".format(__filename), "red")
        
        return isLoadedSuccessfully



class WinActivity:
    def __init__(self, key, time_spent, prediction_results):
        self.key = key
        self.time_spent = time_spent
        if prediction_results != None:
            self.category = prediction_results["category"]
            self.isProductive = prediction_results["isProductive"]
        else:
            self.category = None
            self.isProductive = None
        self.isBrowser = False


    def initWebsite(self, name, title):
        self.name = name
        self.title = title
        self.is_website_stored = False #  to know if url is already stored in firebase db
        self.isBrowser = True


    def initSoftware(self, name):
        self.name = name
        self.title = None
        self.is_software_stored = False


    def set_time_spent(self, time_entry):
        hrs, mins, secs = time_entry.get_hours(),time_entry.get_minutes(),time_entry.get_seconds()
        self.time_spent = str(hrs) + "-h " + str(mins) + "-m " + str(secs)+ "-s"
        return self.time_spent


    def get_class_attributes_values(self):
        #  store values of class attributes in tuple in alphabetical order of variable names.

        attr_vals = ()
        attr_vals += (self.category,)
        attr_vals += (self.isBrowser,)
        attr_vals += (self.isProductive,)

        if not self.isBrowser:
            attr_vals += (self.is_software_stored,)
        else:
            attr_vals += (self.is_website_stored,)

        attr_vals += (self.key,)
        attr_vals += (self.name,)
        attr_vals += (self.time_spent,)
        attr_vals += (self.title,)

        return attr_vals


    def load_class_attributes_values(self, attr_vals):  # from pickle file
        #  load values of class attributes in tuple from pickle file in alphabetical order of variable names.

        self.category = attr_vals[0]
        self.isBrowser = False if attr_vals[1]=='False' else True
        self.isProductive = False if attr_vals[2]=='False' else True

        if not self.isBrowser:
            self.is_software_stored = False if attr_vals[3]=='False' else True
        else:
            self.is_website_stored = False if attr_vals[3]=='False' else True

        self.key = attr_vals[4]
        self.name = None if attr_vals[5]=='None' else attr_vals[5]
        self.time_spent = attr_vals[6]
        self.title = None if attr_vals[7]=='None' else attr_vals[7]
        


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