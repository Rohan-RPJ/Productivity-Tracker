"""DOCSTRINGS"""


# Standard library imports
from __future__ import print_function
import os
import sys, traceback
from signal import *
import time


# Third party imports


# Local application imports
from ..Database.JsonDatabase.jsonDB import JsonDB
from ..Database.FirebaseDatabase.save_data import SaveData as FbSaveData
from ..Database.FirebaseDatabase.retrieve_data import RetrieveUserData as FbRetrieveUserData
from .Json import winActivity as jwa
from .Json import winAutoTimer as jwat
from ..print_colored_text import *
from .Firebase import winActivity as fwa
from .Firebase import winAutoTimer as fwat



# sys.setrecursionlimit(10000)

class Backend:

    def __init__(self):
        self.activityList = fwa.WinAcitivyList()

        # if the tracking process terminates, then call the __store_data_to_file to store activityList object in a file
        for sig in (SIGABRT, SIGBREAK, SIGILL, SIGINT, SIGSEGV, SIGTERM):
            signal(sig, self.__run_at_exit)
            

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

            print_text("{} {} {}".format("\n\n"+("*")*37, "LOADING AND INITIALIZING DATA", ("*")*36+"\n"), "yellow")

            retrieve_user_data = FbRetrieveUserData.getInstance()
            isDBCleared = retrieve_user_data.get_isDBCleared_val()

            if isDBCleared == "f":
                print_firebase_text("Database not cleared")
            else:
                print_firebase_text("Database is Cleared")

            # Initialize firebase db - START #
            save_data = FbSaveData.getInstance()
            op_text = save_data.initDB()  # initializes db in firebase if not already initialized and returns corresponding text.
            
            print_firebase_text(op_text, color="green")
            # Initialize firebase db - END #

            if isDBCleared == 'f':
                
                # load the activityList object from local file
                isLoadedSuccessfully = self.activityList.load_activity_list_from_file()
                
                if not isLoadedSuccessfully:

                    print_info_text("Initializing activityList object...", "yellow")

                    self.activityList = fwa.WinAcitivyList()

                    print_info_text("ActivityList object initialized successfully\n", "green")
            
            else:
                
                # initialize the activityList object
                print_info_text("Initializing activityList object...", "yellow")

                self.activityList = fwa.WinAcitivyList()
                
                print_info_text("ActivityList object initialized successfully", "green")

            print_text("{} {} {}".format("\n\n"+("*")*31, "DATA LOADED AND INITIALIZED SUCCESSFULLY", ("*")*31+"\n\n"), "green")

            autoTimer = fwat.AutoTimer(self.activityList)
            autoTimer.start_execution()

        except Exception as e:

            print_exception_text(e, "red")

            ex_type, ex, tb = sys.exc_info()
            print_exception_text("Exception traceback: ", "red", end="")
            traceback.print_tb(tb)
        finally:
            del tb


    def __store_data_to_file(self):

        try:

            self.activityList.store_activity_list_in_file()

        except Exception as e:

            print_exception_text(e)


    def __update_firebase_db(self):

        try:

            save_data = FbSaveData.getInstance()
            save_data.update_db_at_user_exit()

        except Exception as e:

            print_exception_text(e)


    def __run_at_exit(self, sig, frame):

        if os.getenv("db_choice") == "1":

            print_text("\n\n"+("**")*52+"\n", "magenta", highlight="on_white")

            print_info_text("Running funtions before exiting...\n")

            self.__store_data_to_file()

            print_text()

            self.__update_firebase_db()

            print_text("\nExiting...", color="cyan")
            
            sys.exit()

        elif os.getenv("db_choice") == "2":

            sys.exit()

        sys.exit()