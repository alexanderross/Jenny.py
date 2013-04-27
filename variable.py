from node.generator_node import GeneratorNode

class Variable:
	#variables = @anything
	def __init__(self, name_in):
		self.name = name_in
		self.declared_by = None
		self.used_by = []
		self.value = None

	def compile_links(self, partial_dec = False):
		if(self.declared_by):
			if(len(self.used_by) > 0):
				for node in self.used_by:
					if(node!=self.declared_by):#Any variable reference errors within the attr module itself... well... not totally our fault.
						node.parent.add_relation_by_ref(self.declared_by.parent)
			else:
				if(self.name[0]!="_" and not "." in self.name):
					print "Friendly Warning: variable '"+self.name+"'. Is set in "+self.declared_by.get_full_name(True,".")+", but was never actually used..."
		else:
			raise Exception("Exception in variable '"+self.name+"' was never even declared..... it's a bit wasteful.")

	def declare_from(self, node, partial_set = False):
		self.declared_by = node
		if(isinstance(node,GeneratorNode) and not partial_set):
			node.sets_vars.append(self)
		#It's hard to be a winner when you're abiding by the laws of Thermodynamics. Fuck thermodynamics.

	def used_from(self, node):
		self.used_by.append(node)
		if(isinstance(node,GeneratorNode)):
			node.references_vars.append(self)

