"""DOCSTRINGS"""


# Standard library imports
from __future__ import print_function
from collections import defaultdict
import datetime
from os import system
import sys
import time
from urllib.parse import urlparse


# Local application import
from ...Constants.os_platforms import OS_PF as PF


# Third party imports
if sys.platform in PF[0]:
    import uiautomation as auto
    import win32gui
elif sys.platform in PF[1]:
        import linux
elif sys.platform in PF[2]:
    from AppKit import NSWorkspace
    from Foundation import *
import psutil  # (python system and process utilities) is a cross-platform library for retrieving information on running processes
               # and system utilization (CPU, memory, disks, network, sensors) 
import win32process  # to get foreground window thread process id  


# Local application imports
from ...ML.predictions import *
from ..webscrapper import *
from .winActivity import *



appFrameHostText = "ApplicationFrameHost"
storageFilename = "activities.json"


class WebWindow:

    def is_web_search(self, url):
        if '/search' in url:
            return True
        else:
            return False


    def is_valid_url(self, url):

        if self.is_web_search(url):
            return False

        url = url.split("://")
        if len(url) == 1:
            return False  
        else:
            if url[1].strip() == "":
                return False
            return True


    def get_web_url(self, browser_name):
        if sys.platform in PF[0]:
            url = None
            window = win32gui.GetForegroundWindow()
            browserControl = auto.ControlFromHandle(window)
            try:

                if browser_name == "chrome":
                    edit = browserControl.EditControl(Name="Address and search bar")
                else:
                    edit = browserControl.EditControl()

            except Exception as e:
                print("Exception while getting browser control {}".format(e))
                return url
            try:
                url = edit.GetValuePattern().Value
            except Exception:
                print("Exception while getting url")
                return None

            if "https://" not in url:
                url = "https://" + url
            print("URL: ", url)

            if self.is_valid_url(url):
                return url
            else:
                return None

        elif sys.platform in PF[2]:
            textOfMyScript = """tell app "google chrome " to get the url of the active tab of window 1"""
            s = NSAppleScript.initWithSource_(
                NSAppleScript.alloc(), textOfMyScript)
            results, err = s.executeAndReturnError_(None)
            return results.stringValue()
        else:
            print("sys.platform={platform} is not supported."
                  .format(platform=sys.platform))
            print(sys.version)
        return None


    def clean_hostname(self, hostname):
        if hostname == None or hostname.strip() == '':
            return hostname
        hl = hostname.split('.')
        if "www" in hl[0]:
            del hl[0]
        if hl[-1] in ["com", "net", "org", "in", "co", "us", "int", "edu", "gov", "mil", "arpa"]: 
            del hl[-1]
        return '.'.join(hl)


class Windows: # About the windows or applications or websites user opens

    def __init__(self, webWindow):
        self.webWindow = webWindow  # get info of web if window is a website
        self.webInfo = None
        self.active_window_name = None
        self.new_window_name = None
        self.url = None  # store url if window is a website 
        self.hostname = None  # to store hostname as key in db for website
        self.isBrowser = False  # check if the window is a browser
        self.software_app_detail = None


    def set_new_window(self):
        if sys.platform in PF[0]:
            self.new_window_name = self.get_active_window()
            self.isBrowser = True
            self.url = None
            self.hostname = None
            app_name = self.new_window_name
            if app_name == None or app_name.strip() == '':
                return
            app_name = self.new_window_name.split()[-1].lower()
            browser_name = None
            if 'chrome' in app_name:
                app_name = " - Google Chrome"
                browser_name = "chrome"
            elif 'firefox' in app_name:
                app_name = " - Mozilla Firefox"
                browser_name = "firefox"
            elif 'edge' in app_name:
                app_name = " - Microsoft Edge"
                browser_name = "edge"
            else:
                self.isBrowser = False
            if self.isBrowser:
                self.url = self.webWindow.get_web_url(browser_name)
                print(self.url)
                if self.url == None:
                    self.new_window_name = None
                    return

                self.hostname = self.webWindow.clean_hostname(urlparse(self.url).hostname)
                self.webInfo = WebsiteInfo(self.url)
                self.title, _ = self.webInfo.get_title_and_desc()  # returns title and description
                self.new_window_name = self.url + app_name

        elif sys.platform in PF[1]:
            self.new_window_name = linux.get_active_window_x()
            if 'Google Chrome' in self.new_window_name or 'Mozilla Firefox' in self.new_window_name:
                self.new_window_name = linux.get_web_url_x()


    def get_active_window(self):
        _active_window_name = None
        if sys.platform in PF[0]:
            window = win32gui.GetForegroundWindow()
            # print("Window text",win32gui.GetWindowText(window))
            tid, pid = win32process.GetWindowThreadProcessId(window)

            if tid == 0:
                return None

            _active_window_name = psutil.Process(pid).name().split('.')[0]
            # print(_active_window_name)
            if _active_window_name in ['firefox', 'chrome', 'msedge']:
                # print("Its browser--------\n")
                _active_window_name = win32gui.GetWindowText(window)
            else:
                # print("Its software---------\n")
                # for software: abc.exe + "***" + current window name(for classification)
                if _active_window_name == appFrameHostText:
                    _active_window_name = win32gui.GetWindowText(window).split('-')[-1].strip() 
                    self.software_app_detail = _active_window_name
                else:
                    _active_window_name = _active_window_name 
                    self.software_app_detail =  win32gui.GetWindowText(window) 

        elif sys.platform in PF[2]:
            _active_window_name = (NSWorkspace.sharedWorkspace()
                                   .activeApplication()['NSApplicationName'])
        else:
            print("sys.platform={platform} is not supported."
                  .format(platform=sys.platform))
            print(sys.version)
        return _active_window_name


    def is_window(self):
        if self.new_window_name != None and self.new_window_name.strip() != '':
            return 1
        return 0


class AutoTimer(Windows):
    def __init__(self, jsondb, activityList):
        Windows.__init__(self, WebWindow())

        self.jsondb = jsondb
        self.new_activity = ""
        self.activity = ""
        self.start_time = datetime.datetime.now()
        self.end_time = None
        self.activityList = activityList
        self.first_time = True
        self.title = ""
        self.activityExists = False
        self.webPrediction = None
        self.softwarePrediction = None
        self.prediction_results = defaultdict()
        self.time_entry = None
        self.json_data = None

        
    def get_activity(self):
        win_name = None
        x=''
        if self.isBrowser:
            print("Hostname: ",self.hostname)
            print("Title: ", self.title)

            if self.hostname == None:
                print("Invalid Browser activity")
                return -1

            if self.title == None:
                x=''
            else:
                x=self.title
            win_name = self.hostname + x
            for activity in self.activityList.activities:
                if str(activity.key)+str(activity.title) == win_name:
                    return activity
        else:
            win_name = self.new_window_name

            if win_name == None:
                print("Invalid Software activity")
                return -1

            for activity in self.activityList.activities:
                if activity.key == win_name:
                    return activity
        
        return None


    def set_prediction_results(self):
        if self.isBrowser:
            self.webPrediction = WebsitePrediction(self.url)
            self.prediction_results["category"] = self.webPrediction.get_website_prediction(self.webInfo)
            self.prediction_results["isProductive"] = self.webPrediction.is_productive(self.prediction_results["category"])
        else:
            self.softwarePrediction = SoftwarePrediction(self.new_window_name)
            self.prediction_results["category"] = self.softwarePrediction.get_software_prediction()
            self.prediction_results["isProductive"] = self.softwarePrediction.is_productive(self.prediction_results["category"])


    def set_time_entry(self, start_time, end_time):
        self.time_entry = WinTimeEntry(start_time, end_time, 0, 0, 0, 0)
        self.time_entry._set_specific_times()


    def start_execution(self):
        print("{} EXECUTION STARTED {}".format("#"*50, "#"*50))
        try:
            while True:
                print("\n\n"+("**")*50)

                self.set_new_window()
                print("\nNew Window: ", self.new_window_name)
                print("Active Window: ", self.active_window_name)

                if self.active_window_name != self.new_window_name  and self.is_window():
                    print("\n---New Window not equal to active window---")

                    self.activityExists = True
                    self.activity = self.get_activity()

                    if self.activity == -1:
                        continue

                    if self.activity == None:
                        self.activityExists = False

                    if not self.activityExists:
                        print("\nActivity does not exists in ActivityList: ", self.new_window_name)
                        
                        self.set_time_entry(self.start_time, self.start_time)

                        print("\nMaking predictions for activity: ", self.new_window_name)
                        self.set_prediction_results()

                        if self.isBrowser:
                            self.new_activity = WinActivity(self.hostname, self.time_entry.serialize(), self.prediction_results)
                            self.new_activity.initWebsite(self.new_window_name, self.title)
                        else:
                            self.new_activity = WinActivity(self.new_window_name, self.time_entry.serialize(), self.prediction_results)
                            self.new_activity.initSoftware(self.new_window_name)
                        self.activityList.activities.append(self.new_activity)
                    else:
                        print("\nActivity already exists in ActivityList: ", self.activity.key)
                        self.new_activity = self.activity

                    if not self.first_time:
                        self.end_time = datetime.datetime.now()
                        self.set_time_entry(self.start_time, self.end_time) 
                       
                        self.active_activity.set_time_spent(self.time_entry)
                        self.json_data = self.activityList.serialize(self.active_activity)

                        self.jsondb.store_data(self.json_data, storageFilename)

                        self.start_time = datetime.datetime.now()
                    self.first_time = False
                    self.active_window_name = self.new_window_name
                    self.active_activity = self.new_activity

                time.sleep(1)
        except KeyboardInterrupt:
           pass