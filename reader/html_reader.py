#from xml.dom import minidom
from lib.bs4 import BeautifulSoup as soup
import urllib2 as url_sock
from reader import Reader
import re


#Phase 1- Compile similar matched elements from single html page into 1-dimensional array for sampling
#Phase 2- Compile similar matched elements from single html page with common parents into 2-dimensional dictionary for sampling
#Phase 3- Compile similar matched elements from single html page with sequential, heirarchal matching parents into n-dimension dictionary for sampling
#Phase 4- Compile similar matched elements from multiple html pages, creating a syntax to use data from a page to assemble a link to a page containing contextual children. Then compile that into an n-dimension dict for sampling.


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
				#--Use soup instead of minidom. Comparatively soup is much bulkier, but it's a worthy sacrifice to contextual robustness.
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
		#Process targets to derive 'common parents'. Defining these is important in recursing until common parent node classification
		# and then 'locking' the recursive function to prevent propegating child nodes to the recursive sibling's subtree
		# This lock is internally symbolized with a static char or sequence of chars (String!)
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

	#'CONTINGENT' data collection algorithm.
	# Context: XML, HTML data. 
	# Overview (notes referenced inline, explained below)
	# Given a 2-dimensional array containing strings similar to CSS Selectors, A n-dimension array will be created as a 'contingent' data source

	# Brief Example:
	# An HTML page exists that lists all zip codes for all US states and cities. The page contains a div for each state, each of which contain cities within, and so forth for zip codes.
	# Expressing that with a Scope Target Array (St) of:
	# St = 
	#  0             1             2
	#  |.StateDiv    |.StateDiv    |.StateDiv
	#  |.state_label |.CityDiv     |.CityDiv
	#  |             |.city_label  |.ZipDiv
	#							   |.zip_label
	#
	#St should return a 3-dimensional array resembling the structure: 
	#
	#   [State0...StateN]->[City0...CityN]->[Zip0...ZipN]
	#
	# This allows us to generate a logically valid city, state and zip for a single generated entry. 
	#
	# Sequence defined below.

	#As the recursive function advances, we need to trim the similar subtargets from both dimensions. 
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

	#Scenarios to satisfy:
	#1-State/city/zip
	#<html>
	#
	#
	#</html>

	#data - The current node (starts as document)
	#scope_targets - The 2d array containing target elements
	#formatter - The regular expression defining how to process the data
	#lock - Boolean to define when to no longer feed new nodes into the algorithm and 'lock' iteration to a specific level
	#NOTE- Locking is done most effectively/cleanest within the recursive fx, needs to be changed.
	def _recurse_scope_on_hash(self,data,scope_targets, formatter = None,lock = False):
		#Will change to dict if 
		return_data = []

		current_target = original_target= None
		get_index = None
		get_regex = None

		#Scope targets are empty, which means that we're given the node containing data to process.
		if(len(scope_targets[0]) == 0):

			if(formatter): #Regular expression to match?
				to_return = formatter.match(data.text)
				if(to_return):
					print "MATCHED", to_return.group(1)
					return to_return.group(1)
				else:
					return ""
			else:
				return data.text.strip()
		else: #No RE
			current_target = original_target = scope_targets[0][0]


		#There is only one dimension in the scope targets, which means we return this data as an array.
		if(len(scope_targets) == 1):
			#We're at the end of the current scope definition, which means we actually append the recursed data.
			if(len(scope_targets[0])==1):

				#REGULAR EXPRESSION CHECK -------------------------------
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
				# END RE CHECK - BEGIN TARGETED INDEX CHECK

				if(current_target.count(HTMLReader.INDEX[0]) == current_target.count(HTMLReader.INDEX[1]) == 1): #Has an indexed selector
					#remove index selector from target, store val in get_index.
					current_target = current_target.split(HTMLReader.INDEX[0])
					tail_split = current_target[1].split(HTMLReader.INDEX[1])
					get_index = int(tail_split[0])
					current_target = current_target[0]+tail_split[1]
		
				# END TARG. INDEX CHECK
				#scope_targets[0][0]=current_target# set it backwards so strip matches the tags across recursions
				index = 0

				new_scopes = self.strip_current_target(original_target,scope_targets)

				#Iterate matched elements for current target WRT the data given.
				#We behave differently inside of this iteration given the f(x) is 1-1
				for node in data.select(current_target):
					#check for index request.
					#NOTE: INDEXING IS ZERO-BASED
					if(get_index != None):
						if(index == get_index):
							return_data.append(self._recurse_scope_on_hash(node,new_scopes,get_regex))
						index = index + 1
					else:
						return_data.append(self._recurse_scope_on_hash(node,new_scopes,get_regex))

			#Length is N-1, keep recursing until 1-1
			else: #the current scope's length is greater than one, so we just cat the next recursion on.
				for node in data.select(current_target):
					#This doesn't require a call to S_c_t, just cut the array.
					return_data = return_data +  self._recurse_scope_on_hash(node,self.strip_current_target(original_target,scope_targets),get_regex)


		else: # Len is *-N, we don't care about ct's length, for we just recurse on it by itself.
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


