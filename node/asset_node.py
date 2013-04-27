class AssetNode:
	ALL = 3
	OUT = 2
	IN  = 1

	def __init__(self, name_in):
		self.name = name_in
		self.points_to = []
		self.referred_from = []
		self.children = []
		self.parent = None
		self.outward_weights = []
		self.relation_index = 0

	#Sort any child nodes, refer to wrt_mesh to access same-level node mesh
	def sort_child_nodes(self):
		new_order = [] 
		start_nodes = self.get_origin_child_nodes()

		while start_nodes:
			for node in start_nodes:
				new_order.append(node)
				#Why do I freeze fruit? Because it's fuckin' awesome, that's why. 
				for link in node.points_to:
					if(link.parent != self): #remote link means to update the parent's links.
						#Establish both directions
						self.add_relation_by_ref(link.parent)
					link.referred_from.remove(node) # remove the reference
				#we're done with it now, and it's on the sorted array.
				self.children.remove(node)

			#Idk if while assignment just isn't supported.. but yeah.
			start_nodes = self.get_origin_child_nodes()

		new_order.reverse()

		self.children = new_order
		return self


	def get_origin_child_nodes(self):
		return_array = []
		for node in self.children:
			if (len(node.referred_from) == 0):
					return_array.append(node)

		return return_array if (len(return_array)!= 0) else False

	## FRONT ENDY STUFF

	#Return name from heirarchy. So a node (Hawaii) with a parent (USA) with a parent(World) would return 'World.USA.Hawaii'
	def get_full_name(self, include_root = True, delimiter = "."):
		if(self.parent):
			return self.parent.get_full_name(include_root,delimiter) + delimiter + self.name
		else:
			return self.name

	def get_root_node(self):
		if self.parent == None:
			return self
		else:
			print self.name
			return self.parent.get_root_node()

	def find_deep_child(self, qualified_name):
		qualified_name = qualified_name.replace(self.name+".","")
		if(qualified_name.find(".") != -1):
			next_node = self.find_child(qualified_name.split(".")[0])
			if(next_node):
				return next_node.find_deep_child(qualified_name)
			else:
				print "missed reference from '"+self.name+"' to '"+qualified_name+"'..."
				return None
		else:
			return self #we're there...

	def add_relation_by_name(self,name_in,weight=0):
		if("." in name_in): #scoped, so lets go upwards.
			self.add_relation_by_ref(self.get_root_node().find_deep_child(name_in),weight)
		else:
			raise Exception("Invalid relation '"+name_in+"'")

	def destroy(self):
		if(self.parent):
			self.parent.remove_child(self)
		else:
			del self

	def add_relation_by_ref(self, node,weight=0):
		print self.get_full_name()
		if(node):
			#store the weight
			self.outward_weights.append(weight)
			self.points_to.append(node)
			node.referred_from.append(self)
		else:
			raise Exception("Adding non-existant node relation!! damn!")
		return self

	def add_child(self, node):
		if(node):
			node.parent = self
			self.children.append(node)
		else:
			raise Exception("Adding non-existant node !! damn!")
		return self

	def remove_child(self, child_node):
		if(child_node):
			child_node.clear_relations
			self.children.remove(child_node)
			del child_node

	def remove_children(self, child_nodes):
		for node in child_nodes:
			self.remove_child(node)
		return self

	#mask indices 0- clear outbound(points_to) 1- clear inbound(referred_from)
	def clear_relations(self, cl_mask = 3):
		if(cl_mask & 1 != 0):
			self.clear_outbound_relations
		if(cl_mask & 2 != 0):
			self.clear_inbound_relations

	def clear_outbound_relations(self):
		for out_node in self.points_to:
			self.remove_relation_by_ref(out_node)

	def clear_inbound_relations(self):
		for in_node in self.referred_from:
			in_node.remove_relation_by_ref(self)

	def remove_relation_by_ref(self, node):
		if(node):
			target_index = self.points_to.find(node)
			if(target_index != -1):
				#we've gotta change the node's vector length array too!
				self.outward_weights.pop(target_index)
				self.points_to.pop(target_index)
				node.referred_from.remove(self)
			else:
				raise Exception("Cannot find node "+node.get_full_name()+" to remove from "+self.get_full_name()+"'s references")
		return self

	def find_child(self, node_name):
		for node in self.children:
			if(node.name == node_name):
				return node
		return None
