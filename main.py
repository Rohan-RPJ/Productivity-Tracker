"""DOCSTRINGS"""


# Standard library imports
import os


# Third party imports


# Local application imports
from ProductivityTrackerAssistant.ActivityTracker.main import Backend
from ProductivityTrackerAssistant.print_colored_text import *
from ProductivityTrackerAssistant import check_conn

print_text("\nDATABASES:  ", "blue", end="")
print_text("1. CLOUD FIREBASE  2. LOCAL JSON", "cyan")
print_text("\nEnter your choice: ", end="  ")

db_choice = input()

print_text("\nPREDICTION MODES: ", "blue", end="")
print_text("1. CLOUD  2. DOCKER\n", "cyan")

print_text("Enter your choice: ", end="  ")
prediction_mode = input()
print_text("")


def main():

	choices = ["1", "2"]
	if not ((db_choice in choices) and (prediction_mode in choices)):
		print_text()
		print_warning_text("Enter valid option\n")
		return

	if db_choice == "1" or prediction_mode == "1":
		# check internet connection
		isInternetConnected = check_conn.checkInternetConn()
		if isInternetConnected:
			print_info_text("Connected to Internet", "green")
		else:
			print_err_text("Not connected to Internet!\n")
			print_warning_text("Please check your Internet connection to use cloud resources\n")
			return

	if prediction_mode == "2":
		isDockerRunning = check_conn.checkDockerConn()
		if isDockerRunning:
			print_text("\n", end="")
			print_info_text("Docker Container up and running", "green")
		else:
			print_text("\n", end="")
			print_err_text("Connection to Docker failed")
			print_warning_text("Please check your Docker connection to run text classifier container\n")
			return

	os.environ["db_choice"] = db_choice
	os.environ["prediction_mode"] = prediction_mode

	print_text()
	print_info_text("Your are good to go!", "green")

	backend = Backend()
	backend.main()

		
main()