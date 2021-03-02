from termcolor import *
import colorama


colorama.init()


# prints text in given color
def print_text(text="", color="white", end="\n", highlight=None):  # default color: white
	
	try:
		text = colored(text, color, highlight)
		print(text, end=end)  # used instead of cprint since cprint prints every text on new line
	except Exception as e:
		cprint("Exception occurred while printing text", "red", end=end)
		cprint(e, "red")


def print_firebase_text(text="", color="white", end="\n", highlight=None):

	print_text("[FIREBASE:] ", color="cyan", end="")
	print_text(text, color, end, highlight)



def print_docker_text(text="", color="white", end="\n", highlight=None):

	print_text("[DOCKER:] ", color="cyan", end="")
	print_text(text, color, end, highlight)


def print_algorithmia_text(text="", color="white", end="\n", highlight=None):

	print_text("[ALGORITHMIA:] ", color="cyan", end="")
	print_text(text, color, end, highlight)


def print_json_text(text="", color="white", end="\n", highlight=None):

	print_text("[JOSN:] ", color="cyan", end="")
	print_text(text, color, end, highlight)


def print_local_text(text="", color="white", end="\n", highlight=None):

	print_text("[LOCAL:] ", color="cyan", end="", highlight=highlight)
	print_text(text, color, end, highlight)


def print_exception_text(text="", color="red", end="\n", highlight=None):

	print_text("[EXCEPTION:] ", color="cyan", end="", highlight=highlight)
	print_text(text, color, end, highlight=highlight)


def print_info_text(text="", color="white", end="\n", highlight=None):

	print_text("[INFO:] ", color="cyan", end="", highlight=highlight)
	print_text(text, color, end, highlight)


def print_err_text(text="", end="\n", highlight=None):

	print_text("[ERR:] "+text, color="red", end=end, highlight=highlight)


def print_warning_text(text="", end="\n", highlight=None):

	print_text("[WARNING:] "+text, color="yellow", end=end, highlight=highlight)