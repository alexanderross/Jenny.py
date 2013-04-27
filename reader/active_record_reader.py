
from reader import Reader

class ActiveRecordReader(Reader):
	TYPE_HASH = {
	"binary": "number",
	"boolean" : "number" ,
	"date" : "string",
	"datetime": "string",
	"decimal" : "number",
	"float" : "number",
	"integer" : "number",
	"primary_key" : "_index",
	"string": "string",
	"text": "string",
	"time": "string",
	"timestamp": "string"
	}
	@staticmethod
	def read(path):
		linez = open(path,'r').read()
		linez = linez.split("\n")
		currModel=""
		return_hash = dict()
		for line in linez:
				if("create_table" in line):
					currModel = line.split('"')[1]
					return_hash[currModel]=dict()		
				elif("t." in line and not currModel == ""):
					return_hash[currModel][line.split('"')[1]] = (line.split("t.")[1].split(" ")[0]).strip()

		return return_hash

	@staticmethod
	def translate_type(type):
		return ActiveRecordReader.TYPE_HASH[type]
