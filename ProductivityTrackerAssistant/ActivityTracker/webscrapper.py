"""
DOCSTRINGS
"""


# Standard library imports


# Third party imports
from bs4 import BeautifulSoup
import ijson
import requests


# Local application imports
from ..print_colored_text import *


class WebsiteInfo:

	
	def __init__(self,url):
		self.url = url
		self.__title = None
		self.__description = None
		self.set_title_and_desc()


	def __extract_html_code(self):

		try:
			headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
			page = requests.get(self.url, headers=headers)        #to extract page from website
			html_code = page.content        #to extract html code from page
			
			return html_code
		except Exception as e:
			print_exception_text("Exception occurred while extracting html code: {}".format(e))
			return None

	def __parse_html(self):
		html_code = self.__extract_html_code()
		if html_code is not None:
			soup_obj = BeautifulSoup(html_code, 'html.parser')  #Parse html code
			return soup_obj
		else:
			return None


	# set title,description of website from content of meta tag with name='description'
	def set_title_and_desc(self): 

		soup_obj = self.__parse_html()

		if soup_obj is not None:
			try:
				# get title of website
				self.__title = soup_obj.find('title').string
				print(self.__title)
			except Exception as e:
				# print_exception_text("Exception occurred while finding title: {}".format(e))
				print_warning_text("The website has no title")

			try:
				# get description of website
				meta_tag = soup_obj.find('meta', attrs={'name': 'description'})
				self.__description = meta_tag['content']
				print(self.__description)
			except Exception as e:
				# print_exception_text("Exception occurred while finding description: {}".format(e))
				print_warning_text("The website has no description")


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
# testing webscrapper

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

# Total time for extracting 10 times: 21.98288607597351
# Avg time for extracting once: 2.198288607597351

"""