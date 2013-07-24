from generator.collection_generator import CollectionGenerator
from reader.json_reader import JSONReader
from reader.html_reader import HTMLReader as xml_read

class DynamicCollection(CollectionGenerator):

	#UPCOMING FEATURES
	# -Indexed scoping
	#   +can reference index of final target, rather than being screwed at the proposition of multiple matches (html mostly)
	# -generators within URL
	#   +Able to put static range/collection gens within the url to tie one collection to multiple pageloads
	#   +Each of the items in the range/collection could be the first level key, or each page's data would append to/ update the collection
	#
	#
	#
	resource_pool = dict() # declaring this dict() outside of a method essentially makes this shared among all instances...
	DO_CACHE = False
	DYN_SYMBOL = "live>"

	#not sure if i'm leveraging a bug, but it seems cool.
	def __init__(self, url, targets = [], format = False):
		new_obj = None
		self.default_gvars = {"contingent":[]}
		rtn_string = "Imported Dynamic"

		if(not isinstance(targets[0],list)):
			targets = [targets]
		if(not format):
			format = url.split(".")[-1]

		temp = None
		self.cache_address = self.get_cache_address(url,targets)

		if(self.cache_address in self.resource_pool.keys() and 1==0):
			rtn_string = rtn_string + " from cache"
			temp = self.resource_pool[self.cache_address]
		else:
			if(format=="xml" or format=="rss" or format=="html"):
				read_data = xml_read.read(url,True)
				temp = read_data.to_hash(targets)
				print temp
			elif(format=="json"):
				temp = JSONReader.read(url,True)
		if(self.DO_CACHE):
			self.resource_pool[self.cache_address] = temp
		
		rtn_string = rtn_string+ " as "+format+ ", resulting in "+str(len(temp))
		if(len(targets)>1):
			rtn_string = rtn_string + " keys to a "+str(len(targets))+"-level dictionary"
		else:
			rtn_string = rtn_string + " items in a flat collection"
		print rtn_string

		self.complex = (not isinstance(temp, list))
		self.collection = temp


	def get_cache_address(self,url,targets):
		t_str = ""
		K_LEN = 4
		c_type = "ccoll"
		if(len(targets)==1 and len(targets[0])==1):
			c_type="coll"
		url = url.replace(" ","")
		url = url.replace("/","_")
		url = url.replace(".","_")
		url = url.split("&")
		if(len(url) > 2 ):
			url[1] = "_".join(url[1:])
		url = "_".join(url)

		for element in url.split("_"):
			if len(element) < K_LEN:
				t_str = t_str + element
			else:
				t_str = t_str + element[0:K_LEN-1]

		for item in targets:
			for sub in item:
				t_str+=sub.replace(" ","")
		t_str = t_str.replace("/","_")

		return t_str+"."+c_type






		

#Will serve as an implementation to collectionGenerator that dynamically sources it's input data from the web. This either
#uses RSS, XML, JSON or other easily parsable formats,
#TODO support applying scopes to HTML pages to parse out sets