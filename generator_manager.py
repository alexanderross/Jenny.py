import sys
import os 
sys.path.insert(0, '/reader')
from reader.csv_reader import CSVReader as csv
from reader.json_reader import JSONReader as json
from factory.generator_factory import GeneratorFactory
from generator.collection_generator import CollectionGenerator
from generator.range_generator import RangeGenerator
from generator.dynamic_collection.dynamic_collection import DynamicCollection
from node.generator_node import GeneratorNode

class GeneratorManager:
	#generator declaration = $name = anythin
	registered_generators = dict()
	known_formats = "coll","cus","ran","rel"
	path = ""

	def __init__(self, pre_loads=[],load_cache=None):

		if(load_cache!=None):
			DynamicCollection.resource_pool = load_cache
		for pd_path in pre_loads: #expects [directory,extension]
			self.load_predefined(pd_path[0],pd_path[1])

	def get_resource_pool(self):
		return DynamicCollection.resource_pool


	def process_generator_tag(self,data_line, current_schema):
		active_gen = None
		if(not data_line):
			return None
		data_line=str(data_line.strip())
		if(data_line in self.registered_generators and data_line[0]=="$"):
			active_gen = self.registered_generators[data_line]
		else:
			active_gen = GeneratorNode("generator", data_line, self, current_schema)
		return active_gen

	def process_node_reference(self,name, node):
		self.registered_generators[name] = node

	def load_hash(self, generator_hash):
		for name, data in generator_hash.items():
			if(isinstance(data, dict)): # has to be a dynamic.
				if(not "format" in data.keys()):
					data["format"] = "xml"
				self.registered_generators[name] = DynamicCollection(data["url"],data["keys"],data["format"])
			else:
				self.load_single(str(name),str(data))

	def load_single(self, name, data):
		new_gen, vars_used = GeneratorFactory.new_generator(data)
		if(new_gen != None):
			self.registered_generators[name] = new_gen
		else:
			print data+" could not be compiled into comprehensible generator"


	def load_predefined(self, load_directory, extension_hash = []):
		
		path = load_directory
		listing = os.listdir(load_directory)

		for infile in listing:
			name_split = infile.split('.')
			if(name_split[1] in extension_hash.keys()):
				if(extension_hash[name_split[1]] == "collection"):
					self.registered_generators[name_split[0]] = CollectionGenerator(csv.read(load_directory+"/"+infile))
				elif(extension_hash[name_split[1]] == "contingent_collection"):
					self.registered_generators[name_split[0]] = CollectionGenerator(json.read(load_directory+"/"+infile))






