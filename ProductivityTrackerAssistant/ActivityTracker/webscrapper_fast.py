"""
DOCSTRINGS
"""


# Standard library imports
import sys


# Third party imports
from contextlib import closing
import requests, re

if sys.version_info[0] >= 3:
    import html as html_parser
    html = html_parser
else:
    from six.moves import html_parser    
    html = html_parser.HTMLParser()


# Local application imports
from ..print_colored_text import *



class WebsiteInfo:

	
	def __init__(self,url):
		self.url = url
		self.__title = None
		self.__description = None
		self.set_title_and_desc()


	def __parse_html(self):
		CHUNKSIZE = 1024
		retitle = re.compile("<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
		redesc = re.compile("""<meta name="description" content="(.*?)">""")
		buffer = ""
		is_title_matched = False
		is_desc_matched = False

		try:

			with closing(requests.get(self.url, stream=True)) as res:
				for chunk in res.iter_content(chunk_size=CHUNKSIZE, decode_unicode=True):
					buffer = "".join([buffer, chunk])

					if not is_title_matched:
						matcht = retitle.search(buffer)
						if matcht:
							is_title_matched = True
							self.__title = html.unescape(matcht.group(1))
							# print_info_text("Title: {}".format(self.__title))
							
							if is_desc_matched:
								break

					if not is_desc_matched:

						matchd = redesc.search(buffer)
						if matchd:
							is_desc_matched = True
							self.__description = html.unescape(matchd.group(1))
							# print_info_text("Desc: {}".format(self.__description))

							if is_title_matched:
								break

		except Exception as e:

			print_exception_text("Exception in __parse_html : {}".format(e))


	# set title,description of website from content of meta tag with name='description'
	def set_title_and_desc(self): 

		self.__parse_html()


	def get_title_and_desc(self):
		return (self.__title, self.__description)


	# returns title + description
	def get_text(self):
		if self.__title is None:
			if self.__description is None:
				return None
			else:
				return self.__description
		elif self.__description is None:
			return self.__title
		else: 
			return self.__title + " " + self.__description


	def clean_text(self, text):

		if text != None and text.strip() != '' and '404' not in text:
			return text
		else:
			return None


# wi = WebsiteInfo("https://amazon.com")


"""
# testing ws1

from time import time

def get_avg_extraction_time():

	avg_time = 0
	steps = 10
	for i in range(steps):
		t1=time()
		wi = WebsiteInfo("https://amazon.in")
		t2=time()

		avg_time += (t2-t1)

	print("Total time for extracting {} times: {}".format(steps, avg_time))
	avg_time /= steps
	print("Avg time for extracting once: {}".format(avg_time))


get_avg_extraction_time()

# Total time for extracting 10 times: 17.23781108856201
# Avg time for extracting once: 1.7237811088562012

"""