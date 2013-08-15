import os

class Writer:

	write_headers = []
	write_queue = []
	model_keys = dict()

	def __init__(self):
		pass

	def fill_queue(self,head_node):
		write_count = 0

		if not isinstance(head_node , AssetNode):
			raise Exception("Write Data struct must be an asset node")

		mct=0

		for model in head_node.children:
			if(len(model.children)+len(augmented_index) == 0):
				raise Exception(model.name+" has no attributes. It's quite difficult to write it given that...")

			model_keys[model.name] = mct
			write_headers[mct] = []

			for attribute in model.children:
				write_headers[mct].append(attribute.name)

			self.fill_model_buffer(model, base_count)
			mct = mct + 1

		self.writer.close()

	def fill_model_buffer(self, model, count):

		current_queue = self.write_queue[self.model_keys[model.name]]
		add_queue = []
		offset = len(current_queue)
		for i in range(offset, offset+count):
			for attribute in model.children:
				add_queue.append(attribute.generator.sample({'index': i}))
			current_queue.append(add_queue)
			add_queue = []
			

	def write(self, path, data):
		pass
