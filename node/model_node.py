from node.asset_node import AssetNode

class ModelNode(AssetNode):

	def __init__(self, name):
		AssetNode.__init__(self,name)
		self.index_node = None

	def set_index(self,child_node):
		self.index_node = child_node
