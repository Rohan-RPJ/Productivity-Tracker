"""DOCSTRINGS"""


# Standard library imports
import os


# Third party imports


# Local application imports
from ProductivityTrackerAssistant.ActivityTracker.main import Backend



print("Databases:  1. CloudFirebase  2. LocalJson\n")
db_choice = input("Enter your choice: ")

print("\nPrediction modes: 1. Cloud  2. Docker\n")
prediction_mode = input("Enter your choice: ")
print()

os.environ["db_choice"] = db_choice
os.environ["prediction_mode"] = prediction_mode

if db_choice == "1" or db_choice == "2":
	backend = Backend()
	backend.main()
else:
	print("\nEnter valid option\n")