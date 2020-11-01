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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep


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


def get_chrome_url_x():
        '''
        instead of url the name of the website and the title of the page is returned seperated by '/'
        '''

        detail_full = get_active_window_raw()
        detail_list = detail_full.decode().split(' - ')
        detail_list.pop()
        detail_list = detail_list[::-1]
        _active_window_name = 'Google Chrome -> ' + " / ".join(detail_list)
        return _active_window_name



'''
this file alone can be run without importing other files
uncomment the below lines for linux - works - but activities won't be dumped in json file
(may be it works for other OS also, not sure)
'''

def get_active_window_x():
    full_detail = get_active_window_raw()
    if full_detail == None:
        return None
    else:
        detail_list = full_detail.decode().split(' - ')
        new_window_name = detail_list[-1]
        return new_window_name



activeList = AcitivyList([])

def run():
     new_window = None
     #new_window = get_chrome_url_x()
     #print("new_window: ",new_window)
     current_window = get_active_window_raw()
     #print("current_window",current_window)
     #active_window_name = ""
     #activity_name = ""

     #b = webdriver.Firefox(executable_path='/home/shubham/Envs/cv/share/geckodriver')
     #b.get('https://vcet.edu.in/')
     #print("current_url",b.current_url)
     start_time = datetime.datetime.now()
     first_time = True
     while(True):
         if new_window != current_window:
                if current_window != None:

                    current_window = str(current_window)
                    #main_window = b.current_window_handle
                    #b.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
                    #b.switch_to_window(main_window)
                    #sleep(2)
                    #b.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
                    #b.switch_to_window(main_window)
                    print(current_window[1:],'\n')
                    #print("loop-url:",b.current_url)
                    current_window = current_window[1:]
                if not first_time:
                    end_time = datetime.datetime.now()
                    time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0)
                    time_entry._get_specific_times()
                    #print(time_entry)
                    exists = False
                    #print(activeList.activities)
                    for activity in activeList.activities:
                        if activity.name == current_window:
                            exists = True
                            activity.time_entries.append(time_entry)

                    if not exists:
                        browser_name = get_active_window_x()
                        #if browser_name == 'Mozilla Firefox' or browser_name == 'Google Chrome':
                        #   print("USING: ",browser_name)
                        activity = Activity(current_window, [time_entry])
                        activeList.activities.append(activity)
                        #activeList.initialize_me()
                    json_file = open('activities.json', 'w+')
                    json.dump(activeList.serialize(), json_file,
                                  indent=4, sort_keys=True)
                    start_time = datetime.datetime.now()
                first_time = False


                 #print(type(current_window))

                current_window = new_window
         time.sleep(0.5)
         new_window = get_active_window_raw()


run()
