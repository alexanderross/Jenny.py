from generator import Generator
from random import randrange

class CollectionGenerator(Generator):

	COLLECTION_WRAPPER = "{}"
	ARGUMENT_WRAPPER = "()"

	def __init__(self, collection_in):
		Generator.__init__(self)
		self.collection = collection_in
		self.complex = False
		if(isinstance(collection_in, dict)):
			self.complex = True

		self.default_gvars = {"contingent": []}


	def sample(self, gvars=None):
		pull_index = 0
		if(not gvars):
			gvars = self.default_gvars
		if(len(gvars["contingent"])==0):
			if(self.complex):
				return self.collection.keys()[randrange(len(self.collection.keys()))]
			else:
				return self.collection[randrange(len(self.collection))]
		else:
			current_scope = self.collection
			for item in gvars["contingent"]:
				if(item == "*"):
					item = current_scope.keys()[randrange(len(current_scope.keys()))]
				elif(not item in current_scope.keys()):
					print "Contengency could not find key '"+str(item)+"' within collection. "
					raise Exception("Contengency could not find key '"+str(item)+"' within collection. ")
				
				current_scope = current_scope[item]

			if(isinstance(current_scope, dict)):
				return current_scope.keys()[randrange(len(current_scope.keys()))]
			else:
				return current_scope[randrange(len(current_scope))]

