from node.asset_node import AssetNode

class ModelNode(AssetNode):

	def __init__(self, name):
		AssetNode.__init__(self,name)
		self.index_node = None

	#Designate a child node (an attribute node) as being the index of this item. 
	def set_index(self,child_node):
		self.index_node = child_node
