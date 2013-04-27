from reader import Reader

class CSVReader(Reader):
	@staticmethod
	def read(path):
		process_data = Reader.read(path)
		process_data = process_data.split("\n")
		return_data = []
		if (len(process_data) == 0):
			print "Empty file at "+path
			return []
		else:
			for line in process_data:
				if(line.strip() != ""):
					c_index = line.find(",")
					if(c_index > -1):
						line = line.split(",")
						return_data.append(map(str.strip, line))
					else:
						return_data.append(line.strip())
		return return_data
