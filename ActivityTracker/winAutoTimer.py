from __future__ import print_function
import time
from os import system
import json
import datetime
import sys
if sys.platform in ['Windows', 'win32', 'cygwin']:
    import win32gui
    import uiautomation as auto
elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
    from AppKit import NSWorkspace
    from Foundation import *
elif sys.platform in ['linux', 'linux2']:
        import linux as l

from winActivity import *
from jsonFormat import *
from predictions import *

active_window_name = ""
activity_name = ""
start_time = datetime.datetime.now()
activeList = WinAcitivyList([])
first_time = True

def isWebSearch(a_w):
    if '/search' in a_w:
        return '0'
    else:
        return a_w

def url_to_name(url):
    print(url)
    #string_list = url.split('/')
    return url


def get_active_window():
    _active_window_name = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        _active_window_name = win32gui.GetWindowText(window)
    elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        _active_window_name = (NSWorkspace.sharedWorkspace()
                               .activeApplication()['NSApplicationName'])
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)
    return _active_window_name


def get_chrome_url():
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        chromeControl = auto.ControlFromHandle(window)
        edit = chromeControl.EditControl()
        strChrome = edit.GetValuePattern().Value
        strChrome = 'http://'+strChrome
        return isWebSearch(strChrome)
    elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        textOfMyScript = """tell app "google chrome " to get the url of the active tab of window 1"""
        s = NSAppleScript.initWithSource_(
            NSAppleScript.alloc(), textOfMyScript)
        results, err = s.executeAndReturnError_(None)
        return results.stringValue()
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)
    return _active_window_name
try:
    format = get_json_format()
    activeList.initialize_me(format)
except Exception:
    print('No json')

def get_web_url():
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        chromeControl = auto.ControlFromHandle(window)
        edit = chromeControl.EditControl()
        return isWebSearch(edit.GetValuePattern().Value)
    elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        textOfMyScript = """tell app "google chrome " to get the url of the active tab of window 1"""
        s = NSAppleScript.initWithSource_(
            NSAppleScript.alloc(), textOfMyScript)
        results, err = s.executeAndReturnError_(None)
        return results.stringValue()
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)
    return _active_window_name

try:
    format = get_json_format()
    activeList.initialize_me(format)
except Exception:
    print('No json')


try:
    count = 1
    while True:

        url = ""
        text = ""
        isBrowser = False

        if sys.platform not in ['linux', 'linux2']:
            new_window_name = get_active_window()
            if 'Google Chrome' in new_window_name:
                url = url_to_name(get_chrome_url())
                new_window_name = url+" - Google Chrome"
                isBrowser = True
            elif 'Mozilla Firefox' in new_window_name:
                url = url_to_name(get_web_url())
                new_window_name = url+" - Mozilla Firefox"
                isBrowser = True
            elif 'Microsoft Edge' in new_window_name:
                url = url_to_name(get_web_url())
                new_window_name = url+" - Microsoft Edge"
                isBrowser = True
        if sys.platform in ['linux', 'linux2']:
            new_window_name = l.get_active_window_x()
            if 'Google Chrome' in new_window_name or 'Mozilla Firefox' in new_window_name:
                new_window_name = l.get_chrome_url_x()


        if active_window_name != new_window_name  and new_window_name.split(' - ')[0].strip() != '0':
            print(str(count)*25)
            print("Active window: ",active_window_name)
            print("New window: ",new_window_name)
            activity_name = active_window_name

            exists = False
            for activity in activeList.activities:
                if activity.name == new_window_name:
                    exists = True
                    break

            if not exists:
                #print(isBrowser)
                title = "None"
                if isBrowser:
                    webPrediction = WebsitePrediction(url)
                    prediction = webPrediction.get_website_prediction()
                    isProductive = webPrediction.is_productive(prediction)
                    title = webPrediction.webInfo.title
                else:
                    text = new_window_name
                    softwarePrediction = SoftwarePrediction(text)
                    prediction = softwarePrediction.get_software_prediction()
                    isProductive = softwarePrediction.is_productive(prediction)

                time_entry = WinTimeEntry(start_time, start_time, 0, 0, 0, 0)
                time_entry._set_specific_times()

                new_activity = WinActivity(new_window_name, time_entry.serialize(), prediction, isProductive, title=title)
                activeList.activities.append(new_activity)
            else:
                new_activity = activity

            if not first_time:
                end_time = datetime.datetime.now()
                time_entry = WinTimeEntry(start_time, end_time, 0, 0, 0, 0)
                time_entry._set_specific_times()

                # exists = False
                # for activity in activeList.activities:
                #     if activity.name == activity_name:
                #         exists = True
                #         old_activity = activity
                #         break

                # if exists:
                #     old_activity.time_entries.append(time_entry)
                #     activity = old_activity
                # else:
                #     print(isBrowser)
                #     if isBrowser:
                #         webPrediction = WebsitePrediction(url)
                #         prediction = webPrediction.get_website_prediction()
                #         isProductive = webPrediction.is_productive(prediction)
                #     else:
                #         text = activity_name
                #         softwarePrediction = SoftwarePrediction(text)
                #         prediction = softwarePrediction.get_software_prediction()
                #         isProductive = softwarePrediction.is_productive(prediction)

                #     activity = WinActivity(activity_name, [time_entry], prediction, isProductive)
                #     activeList.activities.append(activity)

                active_activity.make_time_entires_to_json(time_entry)
                data = activeList.serialize(active_activity)
                with open('activities.json', 'w') as json_file:
                    json.dump(data, json_file,
                              indent=4, sort_keys=True)
                    start_time = datetime.datetime.now()
            first_time = False
            active_window_name = new_window_name
            active_activity = new_activity

            count+=1
        time.sleep(1)


except KeyboardInterrupt:
    # with open('activities.json', 'w') as json_file:
    #     json.dump(activeList.serialize(), json_file, indent=4, sort_keys=True)
    pass
