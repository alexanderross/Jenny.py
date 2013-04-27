from os.path import expanduser
import os.path
import sys

class prefman:
	data=""

	def __init__(self, file_path):
		read_file= open(file_path)
		self.data = self.file_to_hash(read_file)

	def file_to_hash(hashfile):
		pre_buffer = ""
		owner_stack = [dict()]
		quote_lock=False
		reading_var = ""
		line = 0
		prev_char=""
		hashfile.read(1)
		while True:
			c = hashfile.read(1)
			pre_buffer = pre_buffer + c 
			if(c=="\n"):
				line = line+1
			if(c=="\"" and prev_char!="\\"):
				if(quote_lock):
					quote_lock= False
				else:
					quote_lock = True

			if(not quote_lock):
				if(c==":"):
					reading_var = scrub_line(pre_buffer[0:-1])
					owner_stack[len(owner_stack)-1][reading_var] = ""
					pre_buffer=""
				if(c=="{"):
					if(isinstance(owner_stack[len(owner_stack)-1],list)):
						owner_stack[len(owner_stack)-1].append(dict())
						owner_stack.append(owner_stack[len(owner_stack)-1][len(owner_stack[len(owner_stack)-1])-1])
					else:
						owner_stack[len(owner_stack)-1][reading_var]= dict()
						owner_stack.append(owner_stack[len(owner_stack)-1][reading_var])

					reading_var=""
					pre_buffer=""
				if(c=="}"):
					if(len(owner_stack)!=1):
						if(plain_val):
							owner_stack[len(owner_stack)-1][reading_var] = scrub_line(pre_buffer[0:-1])
						owner_stack.pop()
						pre_buffer=""
				if(c=="["):
					owner_stack[len(owner_stack)-1][reading_var]= []
					owner_stack.append(owner_stack[len(owner_stack)-1][reading_var])
					reading_var=""
					curr_type = "a"
					pre_buffer=""
				if(c=="]"):
					if(plain_val):
						owner_stack[len(owner_stack)-1].append(pre_buffer[0:-1])
					pre_buffer=""
					owner_stack.pop()
				if(c==","):
					if(isinstance(owner_stack[len(owner_stack)-1],list)):
						owner_stack[len(owner_stack)-1].append(pre_buffer[0:-1])
					elif(plain_val):
						owner_stack[len(owner_stack)-1][reading_var] = scrub_line(pre_buffer[0:-1])
					pre_buffer=""
				if( not c):
					break
			prev_char = c
		return owner_stack[0]

	

	def hash_to_file(hashfile, level):
		return_state = ""
		tabs = get_tabs(level)

		for key in hashfile:
			value = ""
			precursor = ""

			if(isinstance(hashfile, list)):
				value = key
			else:
				precursor = key+":"
				value = hashfile[key]

			if(isinstance(value,dict)):
				return_state = return_state + "\n"+tabs+precursor+" {"+hash_to_file(value, level+1)+tabs+"},"
			elif(isinstance(value,list)):
				return_state = return_state + "\n"+tabs+precursor+" ["+hash_to_file(value, level+1)+tabs+"],"
			else:
				if(isinstance(hashfile, list)):
					if(value!=""):
						return_state = return_state +precursor+" "+value+","
				else:
					return_state = return_state +"\n"+tabs+precursor+" "+value+","
		return return_state[0:-1]+"\n"


	def get_tabs(num):
		return_data = ""
		for i in range(0,num):
			return_data = return_data + "\t"
		return return_data

	def scrub_line(line):
		line = line.replace("\n","")
		line = line.replace("\t","")
		line = line.replace("\r","")
		line = line.lstrip()
		line = line.rstrip()
		return line




http://localhost:3000/companies
http://localhost:3000/companies?utf8=%E2%9C%93&search=carp&search_type=name
http://localhost:3000/companies?utf8=%E2%9C%93&search=crap&search_type=dn
http://localhost:3000/companies?utf8=%E2%9C%93&search=*.*.*&search_type=e_locus
http://localhost:3000/dictionaries
http://localhost:3000/dictionaries?group_by=updated
http://localhost:3000/dictionaries?group=4.2&group_by=locus
http://localhost:3000/visuals/index?visual=grid
http://localhost:3000/visuals/index?visual=treemap
http://localhost:3000/visuals/index?visual=densitymap
http://localhost:3000/visuals/index?visual=geomap











