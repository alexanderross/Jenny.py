from node.asset_node import AssetNode as AN
from node.generator_node import GeneratorNode
import variable as p_var

class SchemaManager:

	current_schema = None
	current_gen_manager = None
	IGNORE_STR = "_ignore"
	RESERVED_CHAR = "_"
	WHOAMI = "JENNY:0.7a:"

	persistant_variables = dict()

	def __init__(self, head_node):
		self.current_schema = head_node


	def load_preferences(self, preferences, gen_manager):
		self.current_gen_manager = gen_manager
		if("_curr_generators" in preferences.keys()):
			gen_manager.load_hash(preferences["_curr_generators"])
			print self.WHOAMI+" Generators after adding "+str(len(preferences["_curr_generators"].keys()))+" from configuration:"
		else:
			print self.WHOAMI+" Loaded no additional generators"

		print "----"
		print " , ".join(gen_manager.registered_generators.keys())
		print "----"
		print ""

		ir=0
		to_destroy = [] #wait to kill models
		for	model_node in self.current_schema.children:
			if(not model_node.name in preferences.keys()):
				preferences[model_node.name] = dict()

			if(self.IGNORE_STR in preferences[model_node.name].keys()):
				to_destroy.append(model_node)
			else:
				to_destroy_atr = []
				for attribute_node in model_node.children:

					keep = False
					if(not attribute_node.name in preferences[model_node.name].keys()):
						preferences[model_node.name][attribute_node.name] = dict()
					data = preferences[model_node.name][attribute_node.name]
					if(self.IGNORE_STR in data.keys()):
						to_destroy_atr.append(attribute_node)
					else:
						if(attribute_node.is_key):
							attribute_node.set_generator(gen_manager.process_generator_tag("$_index", self))
							attribute_node.generator.parent = attribute_node
							keep = True
						#TODO implement HM and BT relations (probably needs some helper methods, likely re-tooling of some of the variable management)
						if("belongs_to" in data.keys()):
							print "HAZ BELONG TO "
							fk_data = data["belongs_to"]
							print fk_data
							#should essentially hold the keys to independently make one of these
							keep = True
							count = 1
							if(self.RESERVED_CHAR+"repeat" in fk_data.keys()):
								count = int(fk_data[self.RESERVED_CHAR+"repeat"].strip())
							if(not self.RESERVED_CHAR+"class" in fk_data.keys()):
								raise Exception("A belongs to relation was created, but there's no class to tie the relation to...")

							model_node.add_relation_by_name("Root."+fk_data[self.RESERVED_CHAR+"class"].strip(), count)

						if("gen" in data.keys()):
							keep = True
							if(data["gen"] != ""):
								attribute_node.set_generator(gen_manager.process_generator_tag(data["gen"],self))
					if(not keep):
						to_destroy_atr.append(attribute_node)
					else:
						#Establish env variable for this attribute
						if(attribute_node.generator):
							if("persist" in data.keys()): #A custom name for this var
								attribute_node.generator.sets_vars.append(data["persist"].strip())
							else:
								attribute_node.generator.sets_vars.append(model_node.name+"."+attribute_node.name)

				if((model_node.children) == 0): #no attributes, no reason to render...
					to_destroy.append(model_node)
				else:
					model_node.remove_children(to_destroy_atr)

		#Remove pending model deletions
		self.current_schema.remove_children(to_destroy)
		#Compile node dependencies derived from variables
		self.compile_variable_dependencies()
		return preferences

	def compile_variable_dependencies(self):
		#TODO Is there a way to legitimately globalize this?
		print self.WHOAMI+" Compiling Variable Dependencies"
		for model_node in self.current_schema.children:
			#TODO This all can be done better. It wasn't originally made to do what it does now.
			for attribute_node in model_node.children:
				if(attribute_node.generator): 
					g = attribute_node.generator
					for index in range(0,len(g.references_vars)):
						g.references_vars[index]= self.update_variable(g.references_vars[index] , g, False)

					for index in range(0,len(g.gen_stack)):
						item = g.gen_stack[index]
						if(isinstance(item ,str) and item[0]=="$"):
							g.gen_stack[index] = self.update_variable(item[1:],g,False)

					for index in range(0,len(g.assg_var_stack)):
						item = g.assg_var_stack[index]
						if(isinstance(item ,str) and item[0]=="$"):
							g.assg_var_stack[index] = self.update_variable(item[1:],g,True,True)

					for index in range(0,len(g.var_stack)):

						if(g.var_stack[index]):

							return_args = {}
							for arg, ref_var in g.var_stack[index].items():
								if(isinstance(ref_var , list)): #contingency vars for a collection
									return_args[arg] = []
									for dependency in ref_var:
										if(dependency[0]=="$"):
											t_var = self.update_variable(dependency[1:],g,False)
											return_args[arg].append(t_var)
										else:
											return_args[arg].append(dependency)
								else: #seems like range generator vars
									if(ref_var[0]=="$"):
										t_var = self.update_variable(ref_var[1:],g,False)
										return_args[arg] = t_var
									else:
										return_args[arg] = ref_var
								g.var_stack[index] = return_args
						else:
							g.var_stack[index] = None

					for index in range(0,len(g.sets_vars)):
						if(isinstance(g.sets_vars[index],str)): #we may already have done this.
							g.sets_vars[index] = self.update_variable(g.sets_vars[index], g, True)

		print self.WHOAMI+" Compiling variable linkage into node links"
		for name, variable_obj in self.persistant_variables.items():
			variable_obj.compile_links()

		print self.WHOAMI+" Ordering models and attrbutes by variable reference order"
		print ""
		for model_node in self.current_schema.children:
			model_node.sort_child_nodes()
		self.current_schema.sort_child_nodes()


	#If it's not declaring(setting) the var, it's using it. 
	#At the moment, a variable can only be assigned once. 
	def update_variable(self, variable_name, node, is_declaring = False, is_partial_declaration = False):
		if(not variable_name in self.persistant_variables.keys()):
			self.persistant_variables[variable_name] = p_var.Variable(variable_name)
		elif(is_declaring and self.persistant_variables[variable_name].declared_by != None):
			raise Exception("Re-assigning a variable is not yet supported!")
		if(variable_name[0]=="$" or "never"=="true"):
			self.persistant_variables[variable_name].value = node
			self.current_gen_manager.process_node_reference(variable_name, node)

		active_var = self.persistant_variables[variable_name]


		if(is_declaring):
			active_var.declare_from(node, is_partial_declaration)
		else:
			active_var.used_from(node)
		return active_var


	








