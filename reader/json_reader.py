import json
import sys
import urllib2 as url_sock
sys.path.insert(0, '/reader')
from reader import Reader

class JSONReader(Reader):

	@staticmethod
	def read(path,is_url=False):
		if is_url:
			return json.load(url_sock.urlopen(path).read())
		else:
			return json.load(open(path,'r'))

	@staticmethod
	def read_str(str):
		return json.load(str)