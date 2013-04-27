from reader.json_reader import JSONReader
from writer.json_writer import JSONWriter
import sys
import os

class DefaultConfiguration:
	primary = {
		"generator_extension":{
			"coll":"collection",
			"ccoll":"contingent_collection"
		},
		"_genspec":{},
		"genspec_extension":".gspec",
		"generator_directory":"generators",
		"genspec_directory":"configurations",
		"config_filename":"jenny.cflg",
		"config_directory":"cfg",
		"output_directory":"output",
		"default_reader":"/active_record",
		"default_writer":"sql",
		"cache_path":"tmp",
		"preload_paths":["collections"],
		"sql":{
			"line_delimiter": '\n',
			"value_delimiter":',',
			"escape_character":"\\",
			"enclose_non_number": "'",
			"enclose_data_line":"()",
			"block_separator":"\n",
			"block_max_entries": 400,
			"file_max_entries": 100000,
			"null_sequence": "NULL"
		},
		"active_record":{
			"default_primary_key": "id"
		},
		"source":"/Users/tyemilldeveloper/Documents/TM/locus.r5/db/schema.rb",
		"destination":"crap.xxl",
		"rootpath":""
	}


class ConfigurationManager:

	def __init__(self):
		self.data = dict()
		self.GSwrite = JSONWriter()
		self.current_genspec = None
		self.load_config()
		self.load_cached_colls()

	def get_generator_preload_paths(self):
		return_list = []
		for path in self.data["preload_paths"]:
			return_list.append([path,self.data["generator_extension"]])

		return return_list



	def load_cached_colls(self):

		listing = os.listdir(self.data["cache_path"])
		self.data["_cache"] = dict()
		for infile in listing:
			print "loading cache id: "+infile
			self.data["_cache"][infile] = JSONReader.read(self.data["cache_path"]+"/"+infile)

	def save_cached_colls(self, colls):
		for key, coll in colls.items():
			self.data["cache_path"]+key
			self.GSwrite.write(self.data["cache_path"]+"/"+key, coll)


	def load_genspec(self, spec_name):
		self.data["_genspec"][spec_name] = JSONReader.read("/".join([self.data["genspec_directory"],spec_name+self.data["genspec_extension"]]))
		self.current_genspec = spec_name

	def get_current_gemspec(self):
		if(self.current_genspec):
			return self.data["_genspec"][self.current_genspec]
		else:
			raise Exception("Called current genspec when there wasnt one...")

	def save_genspec(self, spec="", data=None):
		if(data != None):
			self.data["_genspec"][spec] = data
		if(spec == ""):
			spec = self.current_genspec
		self.GSwrite.write("/".join([self.data["genspec_directory"],spec+self.data["genspec_extension"]]), self.data["_genspec"][spec])

	def get_current_config_path(self):
		return "/".join([self.data["config_directory"],self.data["config_filename"]])

	def load_config(self,repeated = False):
		if(not repeated):
			self.data = DefaultConfiguration.primary

		pre_load_directory = self.get_current_config_path()

		#self.data = self.data.update(JSONReader.read(pre_load_directory).items())

		self.load_args()
		if(self.get_current_config_path != pre_load_directory and not repeated): #there's a custom config path loaded in.
			self.load_config(True)

	def save_config(self):
		self.GSwrite.write("/".join([self.data["config_directory"],self.data["config_filename"]]), self.data)

	def	load_args(self):
		for i in range(1,len(sys.argv)-1):
			self.process_arg(sys.argv[i][1:].split("."),sys.argv[i+1])

	def process_arg(self, arg_data, value):
		if(len(arg_data) == 0):
			return False
		reference = self.data
		for scope in arg_data:
			reference = reference[scope]
			if(not reference):
				raise Exception("Invalid argument given, cannot find "+scope+" in "+(".").join(arg_data))
		reference = value



