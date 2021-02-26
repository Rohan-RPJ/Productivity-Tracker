"""DOCSTRINGS"""


# Standard library imports
from __future__ import print_function
import sys, traceback
from signal import *
import os


# Third party imports


# Local application imports
from ..Database.JsonDatabase.jsonDB import JsonDB
from ..Database.FirebaseDatabase.save_data import SaveData as FbSaveData
from ..Database.FirebaseDatabase.retrieve_data import RetrieveData as FbRetrieveData
from .Json import winActivity as jwa
from .Json import winAutoTimer as jwat
from .Firebase import winActivity as fwa
from .Firebase import winAutoTimer as fwat



# sys.setrecursionlimit(10000)

class Backend:

    def __init__(self):
        self.activityList = fwa.WinAcitivyList()

        # if the tracking process terminates, then call the __store_activity_list_in_pickle to store activityList object in .pkl fie
        for sig in (SIGABRT, SIGBREAK, SIGILL, SIGINT, SIGSEGV, SIGTERM):
            signal(sig, self.__store_data_to_file)


    def main(self):
        
        if os.getenv("db_choice") == "1":
            # Firebase DB selected
            self.__cloud_firebase_db()
        else:
            # Json DB selected
            self.__local_json_db()


    def __local_json_db(self):
        tb = None
        try:
            jsondb = JsonDB.getInstance()
            # print("Inside auto", jsondb)
            format = jsondb.get_json_format()
            self.activityList =  jwa.WinAcitivyList([])
            self.activityList.initialize_me(format)
            autoTimer = jwat.AutoTimer(jsondb, self.activityList)
            autoTimer.start_execution()
        except Exception as e:
            print("Exception Caught:", e)
            ex_type, ex, tb = sys.exc_info()
            print("Exception traceback:")
            traceback.print_tb(tb)
        finally:
            del tb


    def __cloud_firebase_db(self):
        tb = None
        try:
            retrieve_data = FbRetrieveData.getInstance()
            isDBCleared = retrieve_data.get_isDBCleared_val()

            # Initialize firebase db - START #
            save_data = FbSaveData.getInstance()
            op_text = save_data.initDB()  # initializes db in firebase if not already initialized and returns corresponding text.
            print(op_text)
            # Initialize firebase db - END #

            if isDBCleared == 'f':
                print("Firebase DB not cleared\n")
                print("Trying to load activityList object from file...")
                # load the activityList object from .pkl file
                isLoadedSuccessfully = self.activityList.load_activity_list_from_pickle()
                if not isLoadedSuccessfully:
                    print("Initializing activityList object...")
                    self.activityList = fwa.WinAcitivyList()
                    print("activityList object initialized successfully")
                else:
                    print("Loaded activityList object from file successfully")
            else:
                print("Firebase DB cleared")
                # initialize the activityList object
                print("Initializing activityList object...")
                self.activityList = fwa.WinAcitivyList()
                print("activityList object initialized successfully")

            autoTimer = fwat.AutoTimer(self.activityList)
            autoTimer.start_execution()
        except Exception as e:
            print("Exception Caught:", e)
            ex_type, ex, tb = sys.exc_info()
            print("Exception traceback:")
            traceback.print_tb(tb)
        finally:
            del tb


    def __store_data_to_file(self, sig, frame):
        self.activityList.store_activity_list_in_pickle()

