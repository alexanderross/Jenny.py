#from xml.dom import minidom
from lib.bs4 import BeautifulSoup as soup
import urllib2 as url_sock
from reader import Reader
import re


class HTMLReader(Reader):
	INDEX = [":eq(",")"]
	RE = "/"

	def __init__(self,data):
		self.read_data = data


	@staticmethod
	def read(path,is_url=False):
		new_data = False
		if is_url:
			try:
				data = url_sock.urlopen(path).read()
			except Exception as e:
				raise e
			try:
				new_data = soup(data)
				#new_data = minidom.parseString(data)
			except Exception as e:
				raise e
			
		else:
			new_data = minidom.parseString(open(path,'r').read())

		return HTMLReader(new_data)


	def to_hash(self,scope_targets=False):
		if(scope_targets):
			scope_targets = self._process_targets(scope_targets)
			return self._recurse_scope_on_hash(self.read_data,scope_targets)
		else:
			return self._to_unscoped_hash(self.read_data)

	def _to_unscoped_hash(self,data):#Attempts to emulate JSON hash from XML structure. Lol.
		new_data = dict()
		for item in data.childNodes:
			if(item.nodeType == 9):
				return self._to_unscoped_hash(item)
			elif(item.nodeType == 1):

				if not item.nodeName in new_data.keys(): #We initially assume a dictionary, but if we attempt to assign to the key again, we convert it's value to a list
					new_data[item.nodeName] = self._to_unscoped_hash(item)
				elif(not isinstance(new_data[item.nodeName], list)):
					existing = new_data[item.nodeName]
					new_data[item.nodeName] = []
					new_data[item.nodeName].append(existing)
					new_data[item.nodeName].append(self._to_unscoped_hash(item))
				else:
					new_data[item.nodeName].append(self._to_unscoped_hash(item))

			elif(item.nodeType == 2):
				new_data[item.name] = item.value
			elif(item.nodeType == 3 and item.data.strip()!=""):
				new_data = item.data
		return new_data


	def _process_targets(self,scope_targets):
		validation_split = False
		current_shared = []
		match_index = 0
		for item in range(0,len(scope_targets)):
			if(len(current_shared) == 0):
				current_shared = scope_targets[0]

			for subitem in range(0,len(validation_split)):
				if(len(current_shared)-1 < subitem):
					if(current_shared[subitem] == scope_targets[subitem]):
						match_index = subitem
			current_shared = current_shared[0:match_index]
					#raise Exception("Attempted to compare "+".".join(scope_targets[item][:-1])+" and "+".".join(validation_split[item]) +"Invalid processing definition for XML data - each target must only contain one addional unique scope more than its predecessor")

		for item in range(0,len(scope_targets)):
			scope_targets[0][match_index] = "_@_"+scope_targets[item][match_index] 

		return scope_targets

	def strip_current_target(self,current_target,scope_targets):
		if(len(scope_targets[0]) >= 1):
			new_target = []
			index=0
			for item in scope_targets:
				if(item[0]==current_target):

					new_target.append(item[1:])
				else:
					new_target.append(item)
				index = index + 1
			return new_target
		else:
			return scope_targets

	def _recurse_scope_on_hash(self,data,scope_targets,formatter=None,lock = False):
		return_data = []

		current_target = None
		get_index = None
		get_regex = None
		if(len(scope_targets[0]) == 0):
			if(formatter):
				to_return = formatter.match(data.text)
				if(to_return):
					return to_return.group(1)
				else:
					return ""
			else:
				return data.text
		else:
			current_target = scope_targets[0][0]

		if(len(scope_targets[0])==1):
			if("_@_" in current_target):
				lock = True

			if(current_target.count(HTMLReader.INDEX[0]) == current_target.count(HTMLReader.INDEX[1]) == 1):
				current_target = current_target.split(HTMLReader.INDEX[0])
				tail_split = current_target[1].split(HTMLReader.INDEX[1])
				get_index = int(tail_split[0])
				current_target = current_target[0]+tail_split[1]

			re_split = current_target.split(HTMLReader.RE)
			new_ct = re_split[0]
			if(len(current_target.split(HTMLReader.RE)) >= 3):
				if(len(current_target)==3):
					re_split = re_split[1]
				else:
					re_split = "".join(re_split[1:len(re_split)-1])
				if(not "(" in re_split and not ")" in re_split): # A janky check for matching parentheses 
					re_split =  "("+re_split+")" #add em.

				get_regex = re.compile(re_split)

				current_target = new_ct

			scope_targets[0][0]=current_target# set it backwards so strip matches the tags across recursions

		#recurse and knock out sub-indexes until locked
		#if not locked,
			#iterate over current sub only, remove sub across all targets.
		#if locked, 
			#if total len is 1, expect to append results into a list
			#if total len is above one, iterate over current t sub to get keys and for that key, find the target

		return return_data

#return_data[key] = self._recurse_scope_on_hash(node,self.strip_current_target(current_target,scope_targets)[1:],get_regex)


