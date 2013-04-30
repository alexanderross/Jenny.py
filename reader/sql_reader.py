import sys
from reader import Reader, str_ends_with
#sql will add additional attrs to schema info - 


class SQLReader(Reader):

	TYPE_HASH = {
		"INTEGER":"number",
		"INT":"number",
		"SMALLINT":"number",
		"TINYINT":"number",
		"MEDIUMINT":"number",
		"BIGINT":"number",
		"DECIMAL":"number",
		"NUMERIC":"number",
		"FLOAT":"number",
		"DOUBLE":"number",
		"BIT":"number",
		"DATE":"string",
		"TIME":"string",
		"DATETIME":"string",
		"TIMESTAMP":"string",
		"YEAR":"string",
		"CHAR":"string",
		"VARCHAR":"string",
		"BINARY":"string",
		"VARBINARY":"string",
		"BLOB":"string",
		"TEXT":"string",
		"LONGTEXT":"string",
		"TINYTEXT":"string",
		"MEDIUMTEXT":"string",
		"ENUM":"string"
	}

	LINE_END = ';'
	LINE_COMMENT = "--"
	BLOCK_COMMENT = ['/*','*/']
	DATA_WRAP = [["'"],["`"]]
	MAKE_START = "CREATE TABLE"
	TABLE_DEC_WRAP = [["(",")"]]
	ITEM_DELIM = ","
	ATTR_DEC_WRAP = TABLE_DEC_WRAP
	REQUIRED_FLAG = "NOT NULL"
	#Format should be returning models/attr with some means of data type
	@staticmethod
	def read(path):
		data = open(path, 'r').read()
		return SQLReader.walk_file(data)

	#Add char to buffer
	#Check if we're starting a comment
	#
	#Check if we're in a comment
	#
	#Are we ending a comment?
	@staticmethod
	def walk_file(file_stream):
		schema_data = dict()
		c_buffer = ""
		release_comment = None
		data_start_char = None # Marker to designate waiting for the start char of a data sequence (eg. table names, etc.)
		data_release_char = None

		waiting_for_model = False
		waiting_for_type = False
		waiting_for_attrs = False
		current_attr = ""
		current_model = None
		current_line = 1
		ignore_until = None

		capture_context = ""
		
		for char in file_stream:
			c_buffer = c_buffer + char

			if(char == "\n"):
				current_line = current_line + 1

			if(ignore_until != None):
				
				c_buffer = ""
				if(char == ignore_until):
					ignore_until = None

			elif(release_comment == None and data_start_char == None and data_release_char == None): # We aren't within any type of comment block. Process freely
				if( str_ends_with(c_buffer,SQLReader.LINE_COMMENT) ):
					release_comment = "\n"
				elif( str_ends_with(c_buffer,SQLReader.BLOCK_COMMENT[0])):
					release_comment =SQLReader.BLOCK_COMMENT[1]
				else:#we aren't starting a comment or anything.. process more freely.
					if(str_ends_with(c_buffer,SQLReader.MAKE_START)):
						data_start_char = SQLReader.DATA_WRAP
						c_buffer = ""
						waiting_for_model = True


			elif(release_comment != None and str_ends_with(c_buffer, release_comment)):
				release_comment = None

			elif(data_start_char != None): 
				for wrapper in data_start_char:
					if(str_ends_with(c_buffer, wrapper[0])): #our data dec wrapper has started, set the start
						
						data_release_char = wrapper[0]
						data_start_char = None
						capture_context = c_buffer.strip()
						c_buffer = ""
						break

			elif(data_release_char != None and str_ends_with(c_buffer,data_release_char)):
				
				if(waiting_for_model):
					
					current_model = c_buffer[:-len(data_release_char)] #dont forget to trim the added char to the buffer dawg...
					schema_data[current_model]= dict()
					data_start_char = data_release_char
					data_release_char = None
					waiting_for_attrs = True
					waiting_for_model = False
					c_buffer = ""
					current_attr = ""
				elif(current_attr == ""): #was properly cleared 
					
					if("KEY" in capture_context): #defining key or index
						if("PRIMARY" in capture_context):
							pass
						else:
							pass
						c_buffer = ""
						ignore_until = ")"
						data_release_char = None
					else: #defining an attr
						current_attr = c_buffer[:-len(data_release_char)]
						if(current_model != None):
							
							schema_data[current_model][current_attr] = {"type":None,"len":None,"required":False}
							c_buffer = ""
							waiting_for_type = True
						else:
							raise Exception("SQL Parsing Error: Declaring an attribute outside of table declaration at line: "+str(current_line))

			elif(waiting_for_type): #we're pretty much reading until we hit a space
				
				if((char == " " or char == SQLReader.ITEM_DELIM) and len(c_buffer) > 1): #c_buffer should be ' <type dec> '
					waiting_for_type = False
					c_buffer = c_buffer.strip().upper()

					type_data = []
					
					if(SQLReader.ATTR_DEC_WRAP[0][0] in c_buffer): #len / precision restrictions exist
						type_data = c_buffer.split(SQLReader.ATTR_DEC_WRAP[0][0])

						type_data[0] = type_data[0]
						type_data[1] = int(type_data[1][:-len(SQLReader.ATTR_DEC_WRAP[0][1])])
					else:
						if(char == SQLReader.ITEM_DELIM):
							c_buffer = c_buffer[:-1]
						type_data = [c_buffer,None]

					if(type_data[0] in SQLReader.TYPE_HASH.keys()):
						schema_data[current_model][current_attr]["type"] = SQLReader.TYPE_HASH[type_data[0]]
						schema_data[current_model][current_attr]["len"] = type_data[1]
					else:
						raise Exception("SQL Parsing Error at line: "+str(current_line)+" \n Unknown data type '"+c_buffer+"'")
					waiting_for_attrs = True
					waiting_for_type = False
					c_buffer = ""
			elif(current_attr != "" and str_ends_with(c_buffer,SQLReader.REQUIRED_FLAG)):
				
				schema_data[current_model][current_attr]["required"] = True
				c_buffer = ""

			elif(waiting_for_attrs and str_ends_with(c_buffer,SQLReader.ITEM_DELIM)): # A comma clears the attr vars
				
				current_attr = ""
				data_start_char = SQLReader.DATA_WRAP
				
				waiting_for_attrs=True
				c_buffer = ""

			elif(waiting_for_attrs and str_ends_with(c_buffer, SQLReader.TABLE_DEC_WRAP[0][1])):

				
				waiting_for_attrs = False
				data_release_char = None
				current_model = None
				current_attr = ""
		
		return schema_data







	
