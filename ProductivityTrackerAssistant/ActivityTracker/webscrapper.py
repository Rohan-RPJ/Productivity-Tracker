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
		self.title = None
		self.description = None
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
				self.title = soup_obj.find('title').string
			except Exception as e:
				print_exception_text("Exception occurred while finding title: {}".format(e))

			try:
				# get description of website
				meta_tag = soup_obj.find('meta', attrs={'name': 'description'})
				self.description = meta_tag['content']
			except Exception as e:
				print_exception_text("Exception occurred while finding description: {}".format(e))


	def get_title_and_desc(self):
		return (self.title, self.description)


	# returns title + description
	def get_text(self):
		if self.title is None:
			if self.description is None:
				return None
			else:
				return self.description
		elif self.description is None:
			return self.title
		else: 
			return self.title + " " + self.description


	def clean_text(self, text):

		if text != None and text.strip() != '' and '404' not in text:
			return text
		else:
			return None
