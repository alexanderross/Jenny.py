import variable
from node.asset_node import AssetNode
from generator import *
from factory.generator_factory import GeneratorFactory


class GeneratorNode(AssetNode):

	SEPARATOR = "\'"
	ESCAPE_CHAR = '\\'
	SYSTEM_CHAR = "_"
	schema_reference = None
	generator_reference = None

	OPCHARS = ['*','/','%','+','-']

	def __init__(self, name, data_in, generator_reference_in, schema_reference_in):
		AssetNode.__init__(self,name)
		#This needs work... 
		self.sets_vars = []
		self.references_vars = []
		self.gen_stack = [] #Stack of generators used in sample
		self.operator_stack = [] # Lead operators for each generator (0 would be the operator appended after generator at index 0. '' as an operator signifies end of sequence)
		self.var_stack = [] #index- correspondant var usage for each generator
		self.assg_var_stack = []
		self.operate_as_string = True
		self.last_value = ""
		self.generator_reference = generator_reference_in
		self.schema_reference = schema_reference_in

		self.parse_custom_str(data_in)



	def compile_vars(self, at_index):
		#Before this is called, the used vars should be compiled.
		if(self.var_stack[at_index]):
			return_args = {}
			for arg, ref_var in self.var_stack[at_index].items():
				if(isinstance(ref_var , list)): #contingency vars for a collection
					return_args[arg] = []
					for dependency in ref_var:
						if(isinstance(dependency,variable.Variable)):
							return_args[arg].append(dependency.value)
						else:
							return_args[arg].append(dependency)
				else: #seems like range generator vars
					if(isinstance(ref_var,variable.Variable)):
						return_args[arg].append(ref_var,value)
					else:
						return_args[arg].append(ref_var)
			return return_args
		else:
			return None


	# We should be able to declare variables any which way. 

	#Env Vars :::: root=> root node, i=> assigned ID, total_count=> requested generation count
	def sample(self, environment_vars):
		rtn_str = ""
		index = 0
		for entry in self.gen_stack:


			new_item = ""
			if(isinstance(entry, str)):
				if(entry[0] == self.SYSTEM_CHAR):
					new_item = environment_vars[entry[1:]]
				else:
					new_item = entry
			elif(isinstance(entry, variable.Variable)):
				new_item = entry.value
			else:
				#these should already be resolved to variables. We just need to output them replacing the var references with their current values (but not erase the pointer, of course.)
				new_item = entry.sample(self.compile_vars(index))
			if(isinstance(new_item,unicode)):
				new_item = new_item.encode('utf8')
			else:
				new_item = str(new_item)

			if(self.assg_var_stack[index]):
				self.assg_var_stack[index].value = new_item

			rtn_str = rtn_str + new_item
			if(not self.operate_as_string):
				rtn_str = rtn_str + self.operator_stack[index]

			index += 1 

		if(self.operate_as_string):
			self.last_value = rtn_str
		else:
			self.last_value = str(eval(rtn_str))
		return self.last_value

	def parse_custom_str(self, command):
		buffer_str = ""
		prev_char = ''
		escaped = False
		setting_to = ""
		is_string = False
		current_operator = ""

		for char in command:

			if(char in self.OPCHARS and (prev_char == " " or prev_char == self.SEPARATOR)):

				self.process_fragment(buffer_str, char)
				buffer_str = ""
			else:
				buffer_str = buffer_str + char
				prev_char = char
		
		self.process_fragment(buffer_str, '')

		if(setting_to != ""):
			self.sets_vars.append(setting_to)

	def append_var_stack(self, new_vars):
		if(new_vars):
			for arg, ref_var in new_vars.items():
				#substring the vars, for there is some var delimiter before them.
				if(isinstance(ref_var , list)): #contingency vars for a collection
					for dependency in ref_var:
						self.references_vars.append(dependency[1:])
				else: #seems like range generator vars
					self.references_vars.append(ref_var[1:])



	def process_fragment(self, buffer_str, operator):
		new_vars = None
		set_vars = None

		buffer_str = buffer_str.strip()
		if(buffer_str!=""):
			if(self.operate_as_string and (not operator in "+")):
				raise Exception("Invalid concatenation of string using '"+operator+"' in "+buffer_str)
			else:
				if(self.SEPARATOR in buffer_str):
					buffer_str = buffer_str.replace(self.SEPARATOR,"")
					self.operate_as_string = True
					self.gen_stack.append(buffer_str)
				else: #transitioning into escaped sequence => buffer is a generator or var string
					use_gen=True
					if(buffer_str[0]=="$"):
						if(buffer_str.count("=")==1):
							assg_split = buffer_str.split("=")
							assg_split[0]= assg_split[0].strip()
							set_vars = assg_split[0]
							buffer_str = assg_split[1].strip()
						else:
							if(buffer_str[1] != self.SYSTEM_CHAR):
								self.references_vars.append(buffer_str[1:])
								self.gen_stack.append(buffer_str)
							else:
								self.gen_stack.append(buffer_str[1:])
							use_gen = False
					if(use_gen):
						#Active args should be a dictionary tailored to the specific kind of generator coming back. (matches Gvars in generators)
						#Coll -> contingent: [collection of contingencies]
						#Range -> min: minimum, max:maximum, repeat: number of repetition
						new_generator, active_args = GeneratorFactory.get_generator(buffer_str.strip(), self.generator_reference.registered_generators)
						new_vars = active_args
						self.gen_stack.append(new_generator)
				self.assg_var_stack.append(set_vars)
				self.var_stack.append(new_vars)



