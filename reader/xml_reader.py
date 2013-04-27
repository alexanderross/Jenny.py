from xml.dom import minidom


from reader import Reader
import urllib2 as url_sock

#Do we depreciate this on the HTML reader? 
#XML Reader has no library reliance, so maybe a 'lite' version can use this? 
#HTML Reader can effectively do XML(RSS and swag), HTML, and the reasonable derivatives of those, rather well.
class XMLReader(Reader):

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
				new_data = minidom.parseString(data)
			except Exception as e:
				raise e
			
		else:
			new_data = minidom.parseString(open(path,'r').read())

		return XMLReader(new_data)


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
				return XMLReader.to_hash(item)
			elif(item.nodeType == 1):

				if not item.nodeName in new_data.keys(): #We initially assume a dictionary, but if we attempt to assign to the key again, we convert it's value to a list
					new_data[item.nodeName] = XMLReader.to_hash(item)
				elif(not isinstance(new_data[item.nodeName], list)):
					existing = new_data[item.nodeName]
					new_data[item.nodeName] = []
					new_data[item.nodeName].append(existing)
					new_data[item.nodeName].append(XMLReader.to_hash(item))
				else:
					new_data[item.nodeName].append(XMLReader.to_hash(item))

			elif(item.nodeType == 2):
				new_data[item.name] = item.value
			elif(item.nodeType == 3 and item.data.strip()!=""):
				new_data = item.data
		return new_data


	def _process_targets(self,scope_targets):
		validation_split = False
		if("." in scope_targets[0]):
			for item in range(0,len(scope_targets)):
				scope_targets[item] = scope_targets[item].split(".")
				if(validation_split):
					for subitem in range(0,len(validation_split)):
						if(scope_targets[item][subitem] != validation_split[subitem]):
							raise Exception("Attempted to compare "+".".join(scope_targets[item][:-1])+" and "+".".join(validation_split[item]) +"Invalid processing definition for XML data - each target must only contain one addional unique scope more than its predecessor")
				validation_split = scope_targets[item][:-1]
		return scope_targets


	def _recurse_scope_on_hash(self,data,scope_targets):
		return_data = []
		if(len(scope_targets[0]) > 1 and len(scope_targets) > 1):
			return_data = dict()
			
		for child in data.childNodes:
			#print  scope_targets[0][0], child.nodeName, (scope_targets[0][0] == child.nodeName)
			if(scope_targets[0][0] == child.nodeName): #we've matched a current h-scope. We'll be saving this node to reference all following scopes from
				if(len(scope_targets[0])==1): # current h-scope is down to this
					if(child.nodeType==2): # is an attr
						return_data.append(child.value)
					elif(child.nodeType==3): # is a text node
						return_data.append(child.data)
					elif(child.nodeType==1 and len(child.childNodes) == 1 and child.childNodes[0].nodeType==3):
						return_data.append(child.childNodes[0].data)
					else:
						raise Exception ("Attempted to assign data of non-extractable node type ("+str(child.nodeType)+") named "+child.localName)
				else: # there are more h-scopes, which means that we need to retain this object for the next scopes, and grab it's key from the remaining h-scope
					new_scope_targets = [] #Can't directly modify the existing, for there are other child nodes here that rely on it. 
					for dex in range(0,len(scope_targets)): #we've found the first scope, so remove this parent key from the following scope targets
						new_scope_targets.append(scope_targets[dex][1:])

					current_key = self._recurse_scope_on_hash(child,new_scope_targets)
					if(len(current_key)==0):
						print scope_targets
						raise Exception("Key not found for "+new_scope_targets[0][0]+" within "+child.namespaceURI)
					elif(len(current_key) > 1):
						print "Warning, multiple keys found for "+new_scope_targets[0][0]+" within "+child.namespaceURI+". Took the first, which was "+(current_key[0])

					if(len(new_scope_targets) > 1): #overall scope is singular, but we've knocked out the leading node with this.
						new_scope_targets = new_scope_targets[1:] #we still have another scope
					if(isinstance(return_data,dict)):
						return_data[current_key[0]] = self._recurse_scope_on_hash(child, new_scope_targets)
					else:
						return_data= return_data + (self._recurse_scope_on_hash(child, new_scope_targets))
			else: #not found here.
				if(len(child.childNodes)!=0):
					if(isinstance(return_data,dict)):
						return_data.update(self._recurse_scope_on_hash(child, scope_targets))
					else:
						return_data = return_data + self._recurse_scope_on_hash(child, scope_targets)
		return return_data



