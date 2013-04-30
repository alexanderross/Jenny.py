__all__ = ["html_reader","xml_reader","active_record_reader", "csv_reader", "json_reader","sql_reader"]

import os
import urllib2 as url_sock

class Reader:
	@staticmethod
	def read(path):
		file_data = open(path,'r')
		return file_data.read()

def str_ends_with(string, ending): #does str end with ending?

	return (string[-len(str(ending)):] == str(ending))