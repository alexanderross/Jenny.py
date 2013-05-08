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
			#scope_targets = self._process_targets(scope_targets)
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

		current_target = original_target= None
		get_index = None
		get_regex = None

		if(len(scope_targets[0]) == 0):

			if(formatter):

				to_return = formatter.match(data.text)
				if(to_return):
					print "MATCHED", to_return.group(1)
					return to_return.group(1)
				else:
					return ""
			else:
				return data.text.strip()
		else:
			current_target = original_target = scope_targets[0][0]



		if(len(scope_targets) == 1):
			if(len(scope_targets[0])==1):

				#split it up pre-emptively for the RE check
				#new_ct would be a persist for the target minus RE
				re_split = current_target.split(HTMLReader.RE)
				new_ct = re_split[0]

				if(len(current_target.split(HTMLReader.RE)) >= 3): #does current contain a regular expression?
					#attempt to compile RE, store the re in get_regex and remove it from the current target
					if(len(current_target)==3):
						re_split = re_split[1]
					else:
						re_split = "".join(re_split[1:len(re_split)-1])
					if(not "(" in re_split and not ")" in re_split): # A janky check for matching parentheses 
						re_split =  "("+re_split+")" #add em.

					get_regex = re.compile(re_split)


					current_target = new_ct

				if(current_target.count(HTMLReader.INDEX[0]) == current_target.count(HTMLReader.INDEX[1]) == 1): #Has an indexed selector
					#remove index selector from target, store val in get_index.
					current_target = current_target.split(HTMLReader.INDEX[0])
					tail_split = current_target[1].split(HTMLReader.INDEX[1])
					get_index = int(tail_split[0])
					current_target = current_target[0]+tail_split[1]
		

				#scope_targets[0][0]=current_target# set it backwards so strip matches the tags across recursions
				index = 0

				new_scopes = self.strip_current_target(original_target,scope_targets)

				for node in data.select(current_target):
					if(get_index != None):
						if(index == get_index):
			
							return_data.append(self._recurse_scope_on_hash(node,new_scopes,get_regex))
						index = index + 1
					else:
						return_data.append(self._recurse_scope_on_hash(node,new_scopes,get_regex))
			else: #l of i > 1
				for node in data.select(current_target):
					return_data = return_data +  self._recurse_scope_on_hash(node,self.strip_current_target(original_target,scope_targets),get_regex)

		else: # l-s_c > 1
			return_data = dict()
			new_scopes = self.strip_current_target(original_target,scope_targets)
			print current_target, len(data.select(current_target))
			print data
			for node in data.select(current_target):
				key = self._recurse_scope_on_hash(node,[new_scopes[0]],get_regex)
				if(len(key)==0):
					print "WARN - KEY is 0"
				elif(len(key)!=1):
					key = key[0]
				else:
					key = key[0]
				print new_scopes[1:]
				return_data[key] = self._recurse_scope_on_hash(node,new_scopes[1:],get_regex)
		return return_data


#return_data[key] = self._recurse_scope_on_hash(node,self.strip_current_target(current_target,scope_targets)[1:],get_regex)


