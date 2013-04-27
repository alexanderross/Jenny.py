from node.asset_node import AssetNode
from node.generator_node import GeneratorNode

class AttributeNode(AssetNode):

	def __init__(self, name, data_type_in, is_key_in):
		AssetNode.__init__(self,name)
		self.data_type = data_type_in
		self.generator = None
		self.is_key = is_key_in

	def set_generator(self, generator_node_in):
		self.generator = generator_node_in
		generator_node_in.parent = self
