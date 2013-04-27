import node.asset_node as AN
import node.attribute_node as ATN
import node.model_node as MN

class NodeFactory:
	@staticmethod
	def process_schema(data, name="Root"):

		root_node = AN.AssetNode(name)
		for model_name, model_data in data.items():
			new_node = NodeFactory.process_model(model_name,model_data)
			root_node.add_child(new_node)
		return root_node
	@staticmethod
	def process_model(model_name, data):
		model_node = MN.ModelNode(model_name)

		key_node = None

		for attr_name, attr_data in data.items():
			is_primary = False
			if (attr_data=="_index"):
				is_primary = True
				attr_data = "number"

			new_node = NodeFactory.process_attribute(attr_name, attr_data, is_key = is_primary)

			model_node.add_child(new_node)

			if(is_primary):
				model_node.set_index(new_node)


		if(model_node.index_node == None):

			key_node = NodeFactory.process_attribute("id","number",is_key = True)
			model_node.set_index(key_node)
			model_node.add_child(key_node)

		return model_node
	@staticmethod
	def process_attribute(attr_name, attr_data, is_key):
		attr_node = ATN.AttributeNode(attr_name, attr_data, is_key)
		return attr_node