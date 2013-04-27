import json
from writer import Writer

class JSONWriter(Writer):
	
	def write(self,path,data):
		k = open(path,"w")
		json.dump(data,k,indent=1,sort_keys=True)
		k.close()