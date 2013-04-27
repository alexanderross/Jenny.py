import os
from writer import Writer
from node.asset_node import AssetNode


class SQLWriter(Writer):
	line_delimiter = '\n'
	value_delimiter = ','
	escape_character = "\\"
	enclose_non_number = "'"
	enclose_data_line = "()"
	block_separator = "\n"
	block_max_entries = 400
	file_max_entries = 100000
	null_sequence="NULL"


	def __init__(self, destination, preferences):
		self.write_buffers = dict()
		self.writer = open(destination,"w")

	def write( self, head_node, base_count ): #Limited to only node structs
		write_count = 0
		self.write_headers = dict()

		if not isinstance(head_node , AssetNode):
			raise Exception("Write Data struct must be an asset node")
		self.build_headers(head_node)
		mct=0
		for model in head_node.children:
			self.write_model(model, base_count)
		self.writer.close()

	def write_model(self, model, count, augmented_index=[], buffer_output=False):

		if(self.write_buffers[model.name] != ""):
			self.writer.write(write_buffers[model.name])
			write_buffers[model.name]= ""

		if(len(model.children)+len(augmented_index) == 0):
			raise Exception(model.name+" has no attributes. It's quite difficult to write it given that...")

		for i in range(count):
			if( i == 0 or i % self.block_max_entries == 0):
				self.writer.write(self.write_headers[model.name])
			current_line = self.enclose_data_line[0]

			for attribute in model.children:
				current_line += self.format_data(attribute.generator.sample({'index': i}),attribute.data_type)+self.value_delimiter

			self.writer.write(current_line[0:-1]+self.enclose_data_line[1]+self.line_delimiter)


	def build_headers(self, root_node):
		m_index = 0
		for model in root_node.children:
			header_str = self.block_separator+"INSERT INTO "+model.name+" VALUES ("
			for attribute in model.children:
				header_str += attribute.name+","
			
			self.write_headers[model.name] = header_str[0:-1]+")"+self.line_delimiter
			self.write_buffers[model.name] = ""

			m_index+=1

	def dump_buffer(self, index=""):
		#Will there ever be episodes of COPS based in Canada? 
		if(index == ""):
			for item in self.write_buffers.values():
				self.writer.write(item)
				item = ""
		else:
			self.writer.write(self.write_buffers[index])
			self.write_buffers[index] = ""	

	def format_data( self, value_in, type_in ):
		if(type_in == "number"):
			return str(value_in)
		else:
			return self.enclose_non_number+str(value_in.replace(self.enclose_non_number,self.escape_character+self.enclose_non_number))+self.enclose_non_number

