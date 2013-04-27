import os
import urllib2 as url_sock

class Reader:
	@staticmethod
	def read(path):
		file_data = open(path,'r')
		return file_data.read()