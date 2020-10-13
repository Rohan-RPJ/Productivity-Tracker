'''
This file gives the linux support for this repo
'''
import sys
import os
import subprocess
import re
import time
#from os import system
from dateutil import parser
import datetime
import json
from activity import *





def get_active_window_raw():
    '''
    returns the details about the window not just the title
    '''
    root = subprocess.Popen(
        ['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()
    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m != None:
        window_id = m.group(1)
        window = subprocess.Popen(
            ['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None
    match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
    if match != None:
        ret = match.group("name").strip(b'"')
        #print(type(ret))
        '''
        ret is str for python2
        ret is bytes for python3 (- gives error while calling in other file)
        be careful
        '''
        return ret
    return None

'''
this file alone can be run without importing other files
uncomment the below lines for linux - works - but activities won't be dumped in json file
(may be it works for other OS also, not sure)
'''


activeList = AcitivyList([])
def run():
     new_window = None
     current_window = get_active_window_raw()

     #active_window_name = ""
     #activity_name = ""
     start_time = datetime.datetime.now()
     first_time = True
     while(True):
         if new_window != current_window:
                if current_window != None:
                    current_window = str(current_window)
                    print(current_window[1:])
                    current_window = current_window[1:]
                if not first_time:
                    end_time = datetime.datetime.now()
                    time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0)
                    time_entry._get_specific_times()
                    #print(time_entry.seconds)

                    exists = False
                    for activity in activeList.activities:
                        if activity.name == current_window:
                            exists = True
                            activity.time_entries.append(time_entry)

                    if not exists:
                        activity = Activity(current_window, [time_entry])
                        activeList.activities.append(activity)
                    json_file = open('activities.json', 'w')
                    json.dump(activeList.serialize(), json_file,
                                  indent=4, sort_keys=True)
                    start_time = datetime.datetime.now()
                first_time = False


                 #print(type(current_window))
                current_window = new_window
         time.sleep(1)
         new_window = get_active_window_raw()


run()
def get_chrome_url_x():
        '''
        instead of url the name of the website and the title of the page is returned seperated by '/'
        '''
        detail_full = get_active_window_raw()
        detail_list = detail_full.split(' - ')
        detail_list.pop()
        detail_list = detail_list[::-1]
        _active_window_name = 'Google Chrome -> ' + " / ".join(detail_list)
        return _active_window_name

def get_active_window_x():
    full_detail = get_active_window_raw()

    detail_list = None if None else full_detail.split(" - ")
    new_window_name = detail_list[-1]
    return new_window_name
