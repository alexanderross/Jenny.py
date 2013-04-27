from generator.collection_generator import CollectionGenerator
from generator.dynamic_collection.dynamic_collection import DynamicCollection
from generator.range_generator import RangeGenerator

class GeneratorFactory:

	known_formats = "coll","cus","ran","rel"
	BAIL_ON_NOT_FOUND = False
	VAR_SYMBOL = "$"

	@staticmethod
	def get_generator(data_line, generators):

		arg_wrap = CollectionGenerator.ARGUMENT_WRAPPER
		dyno_sym = DynamicCollection.DYN_SYMBOL

		active_gen = None
		active_args = None
		data_line = data_line.strip()

		if(arg_wrap[0] in data_line and data_line[-1]==arg_wrap[1]): #An existing gen given contingency args

			if(dyno_sym in data_line):
				return DynamicCollection(data_line.split(dyno_sym)[1][1:-1],"xml"), None
			else:
				arg_split = data_line.split(arg_wrap[0])
				if(len(arg_split) != 2): 
					raise Exception("Invalid contingency arguments given")
				else: 
					data_line = arg_split[0].strip()
					active_args = {"contingent":[]}
					for item in arg_split[1][:-1].split(","):
						active_args["contingent"].append(item.strip())


		if(data_line in generators.keys()):
			active_gen = generators[data_line]
		else:
			active_gen, args = GeneratorFactory.new_generator(data_line)
			if(active_args == None):
				active_args = args
			if(active_gen == None):
				if(GeneratorFactory.BAIL_ON_NOT_FOUND):
					raise Exception("Referenced generator '"+data_line+"' not found at compile-time and one couldn't be built from that too...") 
				else:
					active_gen = data_line

		return active_gen, active_args

	#How can we tell them apart w/o explicitly declaring types?

	@staticmethod
	def new_generator(data_line):
		coll_wrap = CollectionGenerator.COLLECTION_WRAPPER
		range_keys = [RangeGenerator.REPEAT_DELIMITER,RangeGenerator.RANGE_DELIMITER]
		arg_wrap = CollectionGenerator.ARGUMENT_WRAPPER
		dyno_sym = DynamicCollection.DYN_SYMBOL

		if(arg_wrap[0] in data_line and arg_wrap[1] in data_line): #An existing gen given contingency args
			if(dyno_sym in data_line):
				data_line = data_line.split(dyno_sym)[1]
				data_split = data_line[1:].split(")")
				#Plasma cutters are for the rich and lazy.
				if(data_split[1]!=""):
					return DynamicCollection(data_split[0], data_split[1][1:-1].split(","),"xml"), None
				else:
					return DynamicCollection(data_split[0]), None

		elif((coll_wrap[0] in data_line and coll_wrap[1] == data_line[-1])): #An explicit collection

			data_line = data_line.strip()[1:-1]

			buffer_str = ""
			data_array = []
			for char in data_line:
				if(char=="," and buffer_str[-1]!="\\"):
					data_array.append(buffer_str)
					buffer_str = ""
				else:
					buffer_str += char
			return CollectionGenerator(data_array), None


		elif(data_line.count(range_keys[0]) == 1 and data_line.count(range_keys[1]) <= 1 ): # A range
			if("$" in data_line):
				generator = RangeGenerator(data_line, False)
				args = generator.split_range_dec(data_line)
				return generator, args
			else:
				return RangeGenerator(data_line), None
		else:
			print "I have no goddamn idea what '"+data_line+"' is"
			return None,None


