from __future__ import print_function
import time
from os import system
from winActivity import *
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

active_window_name = ""
activity_name = ""
start_time = datetime.datetime.now()
activeList = WinAcitivyList([])
first_time = True


def url_to_name(url):
    print(url)
    string_list = url.split('/')
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
        return edit.GetValuePattern().Value
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
    data = {"activities":[{'SOFTWARE':{}},{'WEBSITE TRACKING':{'Mozilla Firefox':{},'Google Chrome':{}}}]}
    activeList.initialize_me(data)
except Exception:
    print('No json')


try:
    count = 1
    while True:
        previous_site = ""
        if sys.platform not in ['linux', 'linux2']:
            new_window_name = get_active_window()
            if 'Google Chrome' in new_window_name:
                new_window_name = url_to_name(get_chrome_url())+" - Google Chrome"
            elif 'Mozilla Firefox' in new_window_name:
                new_window_name = url_to_name(get_chrome_url())+" - Mozilla Firefox"
        if sys.platform in ['linux', 'linux2']:
            new_window_name = l.get_active_window_x()
            if 'Google Chrome' in new_window_name or 'Mozilla Firefox' in new_window_name:
                new_window_name = l.get_chrome_url_x()


        if active_window_name != new_window_name:
            print(str(count)*50)
            print("Active window: ",active_window_name)
            activity_name = active_window_name

            if not first_time:
                end_time = datetime.datetime.now()
                time_entry = WinTimeEntry(start_time, end_time, 0, 0, 0, 0)
                time_entry._get_specific_times()

                exists = False
                i=-1
                for activity in activeList.activities:
                    i+=1
                    if activity.name == activity_name:
                        exists = True
                        activity.time_entries.append(time_entry)
                        break

                if i!=-1 and exists==True:
                    print("Activity:",activeList.activities[i].time_entries)
                print("Exists = ", exists)
                print("--------------------------------------------------------------")

                if not exists:
                    activity = WinActivity(activity_name, [time_entry])
                    activeList.activities.append(activity)
                data = activeList.serialize(activity)
                with open('activities.json', 'w') as json_file:
                    json.dump(data, json_file,
                              indent=4, sort_keys=True)
                    start_time = datetime.datetime.now()
            first_time = False
            active_window_name = new_window_name

            count+=1
        time.sleep(1)
    

except KeyboardInterrupt:
    # with open('activities.json', 'w') as json_file:
    #     json.dump(activeList.serialize(), json_file, indent=4, sort_keys=True)
    pass
