import os
from random import randrange
import copy
from datetime import datetime
import sys


class verbage:
	
	#Next thing to do:: Scope the remembered variables by their models.
	#ie. Claim.name != User.name.

	global CUSTOM_DELIM
	global COMMENT_SYMBOL
	global CUSTOM_CONCAT
	global SAVE_DELIM
	global COMMAND_DELIM
	global RANGE_DELIM
	global FILE_ENDING
	global DATA_PATH
	global HELP_COMMAND
	global OUTPUT_FILE
	global DOSQL
	global ADDED_STUFF
	global PERSIST_TOGGLE_SYMBOL
	global PERSIST_GET_SYMBOL
	global PERSIST_SET_SYMBOL
	global CONTINGENCY_NOTE

	# Config stuff here. 
	OUTPUT_FILE="internal_seed.sql"
	COMMENT_SYMBOL = "#"
	CUSTOM_DELIM=">"
	CUSTOM_CONCAT="+"
	SAVE_DELIM="||"
	COMMAND_DELIM=":"
	RANGE_DELIM="-"
	FILE_ENDING="wtf"
	DATA_PATH="groups/"
	HELP_COMMAND="??"
	PERSIST_TOGGLE_SYMBOL="``"
	PERSIST_GET_SYMBOL = "@@"
	PERSIST_SET_SYMBOL = "$$"
	DOSQL=True
	ADDED_STUFF=[["date","updated_at","date"],["date","created_at","date"]]
	CONTINGENCY_NOTE="=>"

	#Would be hesitant to touch anything under this. Prepare for monolithic, mal-commented python.

	flat_sql=False
	estentries=0
	dunentries=0
	efiles=1
	start_index=1
	start_file=0
	curr_dest=""
	internal_block = 250
	file_block = -1
	persistance=dict()
	dictionary=dict()
	stuff=dict()
	stuff_association=dict()
	writey=open(OUTPUT_FILE,"w")
	enumOne=["","one","two","three","four","five","six","seven","eight","nine"]
	enumSpec=["ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"]
	enumTen=["","","twenty","thirty","fourty","fifty","sixty","seventy","eighty","ninety"]
	disallow=[]
	disremember=dict()
	genActions=["model","fields:","block","c","lit:","dec","email","zip","address","fk","ip","fullname","filename","date","coll","datetime","num:","num","boolean","iter"]
	addOnActions=[]
	customActions=dict()
	contingent = ""
	def __init__(self):
		self.dictionary=dict()
		self.stuff=dict()
		self.initializeDefaults()

	def returnMostSimilar(self,context):
	#	if("_name" in context):
	#		return "compnm"
		if("email" in context):
			return "email"
		if("_zip" in context):
			return "zip"
		if("status" in context):
			return "state"
		if("city" in context):
			return "city"
		if("state" in context):
			return "state"
		if("address" in context):
			return "address"
		if("number" in context):
			return "num"
		if("_id" in context):
			return "num_key"
		if("_ip" in context):
			return "ip"
		if("name" in context):
			if("first" in context):
				return "firstname"
			elif("last" in context):
				return "lastname"
			elif("file_" in context):
				return "filename"
			else:
				return "fullname"
		else:
			return "undef"

	def randomCrap(self,lengthy):
		rtnstr=""
		for i in range(0,lengthy):
			rtnstr+=chr(randrange(26)+97)

		return rtnstr

	def getRandFromArray(self,array):
		return array[randrange(len(array)-1)]

	def compareString(self,context,dicty):
		sim=0
		context=context.replace("_","")
		for char in context:
			if(char in dicty):
				sim = sim + 1

		if(len(context) == sim):
			sim = sim+1
		return sim

	def processTag(self,itera,curr,gentool):
		rtnVal=""
		tool=gentool
		persistVal=""
		capitalize=False
		if(gentool[0]=="!"):
			capitalize = True
			tool = gentool[1:len(gentool)]
		if PERSIST_TOGGLE_SYMBOL in tool:
			split = tool.split(PERSIST_TOGGLE_SYMBOL)
			recompiled=""
			for command in split:
				command=command.replace(PERSIST_TOGGLE_SYMBOL,"")
				if (PERSIST_SET_SYMBOL in command):
					persistVal=command.replace(PERSIST_SET_SYMBOL,"")
					command=""
				if (PERSIST_GET_SYMBOL in command):
					command=command.replace(PERSIST_GET_SYMBOL,"")
					command = self.eval_persist(command)
				recompiled = recompiled+command
			tool=recompiled
		if  "datetime" in tool:
			rtnVal=str(2000+randrange(12))+"-0"+str(randrange(8)+1)+"-0"+str(randrange(8)+1)+" "+str(randrange(24))+":"+str(randrange(60))+":"+str(randrange(60))
		elif(CUSTOM_DELIM in tool):
			rtnVal=self.processCustom(tool,itera,curr)
		elif("coll"+COMMAND_DELIM in tool and "{" in tool and "}" in tool):
			temp=tool.split("{")[1]
			temp=temp.split("}")[0].split(",")
			rtnVal=self.process_intype_coll(temp,itera,curr)
		elif(tool in self.addOnActions):
			rtnVal=self.getRand(tool)
		elif(tool=="operator"):
			rtnVal=self.getRandFromArray(["<",">",">=","<=","=","LIKE"])
		elif(tool=="models"):
			rtnVal=self.getRandFromArray(self.stuff.keys())
		elif(("fields"+COMMAND_DELIM) in tool):
			splitty=tool.split(COMMAND_DELIM)
			rtnVal=self.getRandFromArray(self.stuff[splitty[1]])[1]
		elif "date" in tool:
			rtnVal=str(2000+randrange(12))+"-0"+str(randrange(8)+1)+"-0"+str(randrange(8)+1)
		elif("char"+COMMAND_DELIM in tool):
			splitty=tool.split(COMMAND_DELIM)
			ranges=splitty[1].split(RANGE_DELIM)
			if(ranges[1] == ranges[0]):
				rtnVal = ranges[1]
			else:
				if(ord(ranges[1]) > ord(ranges[0])):
					ranges = [ord(ranges[1]),ord(ranges[0])]
				else:
					ranges = [ord(ranges[0]),ord(ranges[1])]
				rtnVal=chr(randrange(ranges[1]-ranges[0])+ranges[0])
				if(len(splitty)>2):
					for i in range(0,int(splitty[2])-1):
						rtnVal=rtnVal+chr(randrange(ranges[1]-ranges[0])+ranges[0])
		elif("num"+COMMAND_DELIM in tool):
			splitty=tool.split(COMMAND_DELIM)
			ranges=splitty[1].split(RANGE_DELIM)
			if(ranges[1]==ranges[0]):
				rtnVal = ranges[1]
			else:
				rtnVal=str(randrange(int(ranges[1])-int(ranges[0]))+int(ranges[0]))
				if(len(splitty)>2):
					for i in range(0,int(splitty[2])-1):
						rtnVal=rtnVal+str(randrange(int(ranges[1])-int(ranges[0]))+int(ranges[0]))
		elif(tool == "current_dex"):
			rtnVal=str(curr)
		elif(tool == "iter"):
			rtnVal=str(randrange(itera))	
		elif(tool == "num"):
			rtnVal=str(randrange(50000))
		elif(tool=="address"):
			rtnVal=str(randrange(10000))+" N "+str(randrange(180)+10)+"th st"
		elif("fk"+COMMAND_DELIM in tool):
			numrel=1
			dex=str(curr)
			splitty = tool.split(COMMAND_DELIM)
			if(len(splitty)==3):
				if(int(splitty[2])>=1):
					numrel=splitty[2]
				else:
					dex=str(self.getNextIndexForModel(splitty[1]))
			if(DOSQL):
				rtnVal=[dex,numrel]
			else:
				rtnVal=[tool.split(COMMAND_DELIM)[1].lower()+"_entry"+self.getVerbal(randrange(itera)).replace("_","",1)+".id",numrel]
		elif(tool=="zip"):
			rtnVal=str(randrange(9))+str(randrange(9))+str(randrange(9))+str(randrange(9))+str(randrange(9))
		elif(tool=="email"):
			rtnVal=self.getRand("firstname")+self.getRand("lastname")+"@"+self.randomCrap(5)+".com"
		elif("lit"+COMMAND_DELIM in tool):
			rtnVal= tool.split(COMMAND_DELIM)[1]
		elif("file"+COMMAND_DELIM in tool):
			rtnVal=self.randomCrap(10)+"."+tool.split(COMMAND_DELIM)[1]
		elif(tool=="fullname"):
			rtnVal=self.getRand("firstname")+" "+self.getRand("lastname")
		elif(tool=="dec"):
			rtnVal=str(randrange(2000))+"."+str(randrange(100))
		elif(tool=="ip"):
			rtnVal=str(randrange(255))+"."+str(randrange(255))+"."+str(randrange(255))+"."+str(randrange(255))
		elif tool=="text":
			rtnVal="kickasstext"
		elif tool=="boolean":
			rtnVal=randrange(1)
		elif "crap"+COMMAND_DELIM in tool:
			rtnVal=self.randomCrap(int(tool.split(COMMAND_DELIM)[1]))
		else:
			rtnVal=gentool;
		if persistVal != "":
			self.persistance[persistVal]=rtnVal
		if capitalize:
			rtnVal = rtnVal.capitalize()
		return rtnVal
		
	def processCustom(self,customComm,itera,curr):
		commie=customComm.split(CUSTOM_DELIM)
		if(not commie[0]==""): # if there's nothing in the name field, fuck it, we don't need to save. So: 
			if(self.customActions.has_key(commie[0])):#we've got a key, so its either a rewrite, or call.
				if(not commie[1]==""):#we're forcing an expression into an already defined custom, overwrite that shit and save. 
					self.customActions[commie[0]]=commie[1]
					self.saveCustoms()
				else: #The custom action has the expression, and we dont want to overwrite it. 
					commie[1]=self.customActions[commie[0]]
			else: #never seen this, so it's a new one. But this should never happen, cause it happens at the screen process.
				self.customActions[commie[0]]=commie[1]
				self.saveCustoms()
		#If there's no name on it, screw it. just run that shizzle

		#So the save reference and all that is dealt with. time to process it.
		#We'll treat it like python concatenation, evaluating variables as being catted to strings
		# so   [ "Banana "+firstname+" Jackson "+ num:4-50 ] would literally render the words Banana and Jackson, but would attempt to process
		# firstname and num:4-50. These aren't verified, so if they do fuck up typing them, it'll just insert 10 random crap chars.
		commie[1]=commie[1].replace(CUSTOM_DELIM,"")
		coll=commie[1].split("\"")
		rtnVal=""
		for line in coll:
			if(CUSTOM_CONCAT in line):
				line = line.replace(CUSTOM_CONCAT,"")
				line = line.replace(" ","")
				rtnVal += self.processTag(itera,curr,line)
			else:
				rtnVal += line
		return rtnVal

	def process_intype_coll(self,collection_array,itera,curr):
		output_data = []
		target = collection_array[randrange(len(collection_array))]
		if(target != ""):
			return self.processTag(itera,curr,target)
		else:
			return ""

	def eval_persist(self,persist_str):
		equ = persist_str.split(" ")
		eval_str=""
		if(len(equ)==1):
			return self.persistance[equ[0]]
		else:
			for entry in equ:
				if(entry!="+" and entry != "-" and entry != "*" and entry != "/"):
					eval_str = eval_str + str(self.get_persistence(entry))
				else:
					eval_str = eval_str + entry
			return str(eval(eval_str))
			
	def operate(self,num1,num2,op):
		if(op=="+"):
			return int(num1)+int(num2)	
		elif(op=="-"):
			return int(num1)-int(num2)	
		elif(op=="*"):
			return int(num1)*int(num2)	
		else:
			return int(num1)/int(num2)			

	def get_persistence(self,command):
		try:
			return int(command)
		except ValueError:
			pass
		if(self.persistance.has_key(command)):
			command=self.persistance[command]
			if("." in command):
				command = str(int(float(command)))
		else:
			print "PERSISTED VARIABLE "+command+" Not found. Check the order."
			command="0"
		return command

	def set_persistence(self,persist_enabled_string):
		split = persist_enabled_string.split(PERSIST_TOGGLE_SYMBOL)
		for command in split: 
			if (PERSIST_SET_SYMBOL in command):
				self.persistance[command]
	
	def screen_custom(self,customComm):
		goodtogo=True
		coll=customComm.split("\"")
		rtnVal=""
		for line in coll:
			if(CUSTOM_CONCAT in line or len(coll)==1):
				line = line.replace(CUSTOM_CONCAT,"")
				line = line.replace(" ","")
				if(not self.screen_general_command(line)):
					print "Custom parse error at "+line
					goodtogo=False
		return goodtogo

	def getValue(self,typed,context,itera,curr,gentool,curr_id):
		
		rtnVal = self.processTag(itera,curr,gentool)
		use=rtnVal
		mul=1
		if("fk"+COMMAND_DELIM in gentool):
			if(len(rtnVal)==2):
				use=rtnVal[0]
				mul=rtnVal[1]

		if(typed=="string" or typed=="text" or typed=="date" or typed=="datetime"):
			return ["'"+use.replace("'","")+"'",mul]
		return [use,mul]

	def getRand(self,diction):

		if(self.contingent != ""):
			to_return = self.contingent
			self.contingent = ""
			return to_return
		else:
			if(isinstance(self.dictionary[diction], list)):
				lengths = len(self.dictionary[diction])
				return self.dictionary[diction][randrange(lengths)]
			else:
				lengths = len(self.dictionary[diction].keys())
				item = self.dictionary[diction].keys()[randrange(lengths)]
				self.contingent=self.dictionary[diction][item]
				return item

	def getRandFromDefined(self,defined):
		return defined[randrange(len(defined))]

	def initializeDefaults(self):
		path = DATA_PATH
		listing = os.listdir(path)
		for infile in listing:
			if("remember" in infile):
				self.initRem(path+""+infile)
			elif("custom" in infile):
				self.initCustom(path+""+infile)
			elif("deny" in infile):
				self.initializeAs(infile.split('.')[0],path+""+infile)
			else:
				if(not infile.split('.')[0]==""):
					self.initializeAs(infile.split('.')[0],path+""+infile)
					self.addOnActions.append(infile.split('.')[0])

	def getVerbal(self,num):
		result = ""
		if(num>=10 and num <20):
			return "_"+self.enumSpec[num-10]
		else:
			if(num==0):
				return ""
			elif(num<100):
				return "_"+self.enumTen[num/10]+"_"+self.enumOne[num%10]
			elif(num>=100 and num<1000):
				return "_"+self.enumOne[num/100]+"_hundred"+self.getVerbal(num%100)
			elif(num>=1000 and num <1000000):
				return "_"+self.getVerbal(num/1000)+"_thousand"+self.getVerbal(num%1000)
			elif(num>=1000000):
				return "_"+self.getVerbal(num/1000000)+"_million"+self.getVerbal(num%1000000)
			else:
				pass #If you have over a billion fixtures, you're out of your goddamn mind. 

	def initializeAs(self,name,filen):
		filed=open(filen)
		filed = filed.read()
		filed = filed.split("\n")
		if(CONTINGENCY_NOTE in filed[0]):
			self.dictionary[name]= dict()
			for line in filed:
				if(not line==""):
					line = line.split(CONTINGENCY_NOTE)
					self.dictionary[name][line[0]]=(line[1].replace("\n","").rstrip())
		else:
			self.dictionary[name]= []
			for line in filed:
				if(not line==""):
					self.dictionary[name].append(line.replace("\n","").rstrip())

	def getCommandFieldQual(self,prompt,contx):
		valid_response= False


		rtn=""
		while(not valid_response):
			rtn=raw_input(prompt)
			if rtn == "block":
				self.setDissallowed(contx)
				print contx+" added to block list"
				return "skip"
			elif HELP_COMMAND in rtn:
				if("n" in rtn):
					print "Native----------------------"
					for valid in self.genActions:
						print "- "+valid
				if("a" in rtn):
					print "Added Collections-----------"
					for valid in self.addOnActions:
						print "- "+valid
				if("c" in rtn):
					print "Custom Statements-----------"
					for valid,state in self.customActions.items():
						print "- "+valid+">"+state
			elif rtn == "":
				autogen=self.returnMostSimilar(contx)
				return autogen
			elif(self.screen_general_command(rtn)):
				return rtn
			else:
				print "Unknown command"


	def screen_general_command(self,rtn):
		if(CUSTOM_DELIM in rtn):
			splitty=rtn.split(CUSTOM_DELIM)
			if(splitty[1]==""):
				if(self.customActions.has_key(splitty[0])):
					return True
				else:
					print "Unknown custom statement"
			elif(self.screen_custom(splitty[1])): #if each subexpression works, then we're set.
				self.customActions[splitty[0]]=splitty[1] #save it for later.
				self.saveCustoms()
				return True #Doesn't matter, we have an expression to use. 
			else:
				print "Error in custom declaration."
		for accept in self.genActions+self.addOnActions:
				if accept in rtn:
					return True
		return False
			

	def insert_association(self,genstr,model,context):
		splitgen=genstr.split(":")
		if(len(splitgen)>2):
				self.stuff_association[model].append([splitgen[1],int(splitgen[2]),context])
		else:
			self.stuff_association[model].append([splitgen[1],1,context])

	def getCommandBool(self,prompt):
		valid= False
		rtn=""
		while(not valid):
			rtn= raw_input(prompt)
			if("y" in rtn.lower()):
				return True
			elif("n" in rtn.lower()):
				return False

	def getCommandInt(self,prompt):
		valid= False
		rtn=""
		while(not valid):
			try:
				rtn= int(raw_input(prompt))
				valid=True
			except:
				print "That isn't a number..."
		return rtn

	def printHeader(self,model,start):
		self.writey.write("\n")
		self.writey.write("\n")
		self.writey.write("#-----------------------------------------\n")
		if(start):
			self.writey.write("#    Start "+model +"\n")
		else:
			self.writey.write("#    End "+model +"\n")
		self.writey.write("#-----------------------------------------\n")
		self.writey.write("\n")
		self.writey.write("\n")

	def getCommandStr(self,prompt):
		return raw_input(prompt)

	def isAllowed(self,name):
		for line in self.dictionary["deny"]:
			if line in name:
				return False
		return True

	def setDissallowed(self,name):
		if(self.isAllowed(name)):
			self.dictionary["deny"].append(name)
			filly=self.get_file_object(DATA_PATH+"deny."+FILE_ENDING,'a')
			filly.write(name+"\n")

	def initRem(self,path):
		crap=self.get_file_object(path,"r")
		i=0
		for line in crap:
			i=i+1
			line = line.replace("\n","").split(COMMENT_SYMBOL)[0]
			if(not line==""):
				line= line.split(SAVE_DELIM)
				if(len(line) <= 1):
					raise Exception("Bad line at "+path+":"+str(i))
				self.disremember[line[0]]=line[1]

	def isRemembered(self,name):
		if name in self.disremember:
			return True
		return False

	def getRemembered(self,name):
		return self.disremember[name]

	def initCustom(self,path):
		print "custom init"
		crap=self.get_file_object(path,"r")
		for line in crap:
			if(not line==""):
				line=line.replace("\n","").split(SAVE_DELIM)
				self.customActions[line[0]]=line[1]

	def saveCustoms(self):
		filly=self.get_file_object(DATA_PATH+"custom."+FILE_ENDING,'w')
		for entry,expression in self.customActions.items():
			filly.write(entry+SAVE_DELIM+expression+"\n")

	def setRemembered(self,name,tool):
		if(not self.isRemembered(name)):
			self.disremember[name]=tool

			filly=self.get_file_object(DATA_PATH+"remember."+FILE_ENDING,'a')
			filly.write(name+SAVE_DELIM+tool+"\n")

	def getCommandGeneral(self,prompt,options):
		valid= False
		rtn=[]
		while(not valid):
			print prompt
			for i,option in enumerate(option):
				print "("+str(i)+"):"

	def addField(self,model,context,vartype,auto):
		if(self.isAllowed(context)):
			global gentool
			gentool=""
			if(not self.isRemembered(model+"*"+context)):
				if(auto):
					gentool=self.returnMostSimilar(context)
				else:
					gentool=self.getCommandFieldQual("Generator for "+model+"."+context+":"+vartype+"?",context)
					self.setRemembered(model+"*"+context,gentool)
				if( not "ted_at" in context):

					if(self.stuff.has_key(model)):
						self.stuff[model].append([vartype,context,gentool])
					else:
						self.stuff[model]=[]
						self.stuff_association[model]=[]
						self.stuff[model].append([vartype,context,gentool])
			else:
				if(not auto):
					gentool=self.disremember[model+"*"+context]
					if(self.stuff.has_key(model)):
						self.stuff[model].append([vartype,context,gentool])
						#print "put "+self.disremember[context]+" in "+model
					else:
						self.stuff[model]=[]
						self.stuff_association[model]=[]
						self.stuff[model].append([vartype,context,gentool])
						#print "put "+self.disremember[context]+" in "+model
			if("fk"+COMMAND_DELIM in gentool):
				self.insert_association(gentool,model,context)

	def getRelationalData(self,model):
		final_rel = dict() # [a=>n] be sure that in addition to the lock, that field a is iterated /n times. If this needs to be used n>1, you suck at schemas. 
		final_mul = self.getIterationMultiplier(model)
		for entry in self.stuff_association[model]:
			data=self.getIterationMultiplier(model,1,entry[0])
			final_rel[entry[2]]= data
		return [final_mul,final_rel] #Final multiplier, step multipliers TBA count boost, used indices

	#Give me a model, I'll tell you the factor which it's relations multiply it by tracing relations backward. (No cyclic relations, hopefully.)
	def getIterationMultiplier(self,model,mul=1,sticky=""):
		k = self.getPrimaryMRelation(model,sticky)
		if(k):
			if(sticky==k[0]):
				return mul*k[1] #just the multipler for the sticky Model.
			mul = mul*k[1]  #Skip it if it's a primary relation, for the iteration lock below deals with the primary, bro. 

			return self.getIterationMultiplier(k[0],mul,sticky)
		return mul # No love from local primary relation being >0

	def getPrimaryMRelation(self,model,sticky=""):
		bestcache=[0,0]
		lookahead=[0,0]
		for entry in self.stuff_association[model]: #[targetModel,self count to]
			if(sticky!=""):
				temp=self.getPrimaryMRelation(entry[0],sticky)
				if(temp):
					temp[1]= temp[1]*entry[1]
					lookahead=temp
				if(entry[0]==sticky):
					bestcache = entry
			elif(entry[1] >= bestcache[1]):
				bestcache = entry
		if(bestcache[1]!=0):
			if(lookahead[1]!=0):
				bestcache[1]=bestcache[1]*lookahead[1]
			return bestcache


	def getModelOutputOrder(self):
		return_order=[]
		action_sense=0
		loop_sense=0
		currentModel=""
		temp_association = copy.deepcopy(self.stuff_association)
		while(True):
			loop_sense = loop_sense+1
			full=0
			for model,assoc in temp_association.items():
				currentModel=model
				if(len(assoc)>0):
					#This has dependencies, we can't load this until those are dealt with.
					full=full+1
				else:
				    #This model is not dependent on any models still out of the load array
					return_order.append(model)
					#Remove links to this in other models
					for k,v in temp_association.items():
						toremove=[]
						for item in v:
							if(model == item[0]):
								toremove.append(item)
								action_sense = action_sense+1
						for target in toremove:
							v.remove(target)
					del temp_association[model]
					action_sense = action_sense+1
			if(full==0):
				#There are no more dependencies to insert. We're done.
				break
			if(loop_sense > action_sense):
				print "ERROR:: Missing Association-----------------------------------"
				print ">>> Missing model for association around "+currentModel+". Stopped writing. Some models may be missing."
				print temp_association[currentModel]
				print "Not resolving in "
				print temp_association
				break 
		return return_order

	def prefetch_create_relations(self):
		mxset=dict()
		for model,data in self.stuff_association.items():
			for entry in data:
				if(entry[1]==0):
					if not mxset.has_key(entry[0]):
						mxset[entry[0]]=[]
					mxset[entry[0]].append(model)
		return mxset


	def compile_model_association(self,iters):
		order = self.getModelOutputOrder()
		corresp= self.prefetch_create_relations()
		record_ct=0
		newData=dict()
		for model in order:
			boomer_data=self.getRelationalData(model)
			newData[model] = boomer_data
			record_ct = record_ct + (boomer_data[0]*iters)
		for model,entry in corresp.items():
			add_to=0
			for addmod in entry:
				add_to=add_to+ (iters*newData[addmod][0])
			newData[model].append(add_to) #boost
			record_ct= record_ct+ add_to
			newData[model].append(1) #used indices
		self.stuff_association = newData
		return record_ct

	def getNextIndexForModel(self,model):
		val= self.stuff_association[model][3]
		self.stuff_association[model][3]=val+1
		return val

	def get_file_object(self,path,arg):
		arg=arg.lower()
		if(arg=="a" or arg=="r"):
			if(os.path.exists(path)):
				return open(path,arg)
			elif(arg=="a"):
				return open(path,"w")
			else:
				#temp=open(path,"w")
				#temp.close()
				return open(path,"r")
		else:
			return open(path,"w")

	def create_indexed_file_name(self, path, curr_index):
		data = path.split(".")
		return "".join(data[0:-1])+str(curr_index)+"."+data[-1]

	def writeToFile(self,iterations,dest):
		records=0
		self.writey.close()
		self.curr_dest = dest
		queries=self.compile_model_association(iterations)
		self.estentries = queries
		est_files=0
		for entry in self.stuff:
			if(DOSQL):
				estimated=queries 
				estimated = estimated + (((estimated/self.internal_block)+len(self.stuff))*3)
			else:
				estimated=estimated + len(entry)+3
				estimated=(estimated+ 2) * iterations
		if(self.file_block >0):
			dest=self.create_indexed_file_name(dest,self.start_file)
			self.efiles = estimated / (self.file_block+((self.file_block / self.internal_block)*3))
		self.writey=open(dest,"w")
		print "------------------------WRITING::{}---------------------------\n".format(OUTPUT_FILE)
		print "Writing"+self.getVerbal(iterations).replace("_"," ")+" base entries each for"+self.getVerbal(len(self.stuff)).replace("_"," ")+" Models"
		print "Estimated lines: "+str(estimated)
		print "Estimated file size: {:,}".format(estimated*30)+" bytes"
		print "Estimated completion time: A while."
		print "Estimated File Count "+str(self.efiles)
		print "Started on "+str(datetime.now())
		print ""
		for model,data in self.stuff_association.items():
			new=self.writeModelSQL(model,iterations,data)
			print "\nWrote "+str(new)+" lines for "+model
			records= records+new
		return records


	def writeModelYML(self,model,iterations,data):
		records=0
		self.printHeader(model,True)
		for i in range(0,iterations):

			self.writey.write("\n")
			self.writey.write(model.lower()+"_entry"+self.getVerbal(i).replace("_","",1)+":\n")
			records=records+1
			self.writey.write("  _model: \""+model+"\"\n")
			for v in self.stuff[model]:
				if(not v[0]=="boolean" and not v[2]=="skip"):
					self.writey.write("  "+v[1]+": "+self.getValue(v[0],v[1],iterations,i+1,v[2],i)+"\n")
		self.printHeader(model,False)
		print "DONE"
		return records

	def writeModelSQL(self,model,iterations,fk_mutex_data):
		records=0
		coreIter=0
		if(not self.flat_sql):
			self.printHeaderSQL(model,True)
		last_write=datetime.now()
		broke_entry=False
		eta = ""
		divider = 100
		if(self.estentries< divider):
			progressBlock = 1
		else:
			progressBlock = self.estentries / divider
		baseIterations = iterations * fk_mutex_data[0]
		if(len(fk_mutex_data)>2): #das booster exists!
			print "DAS BOOSTER!"
			coreIter=baseIterations
			baseIterations = baseIterations+fk_mutex_data[2]
		additional_locks = fk_mutex_data[1] #[context,mul]
		i=0
		while (i < baseIterations):
			if(i==0):
				if(not self.flat_sql):
					self.writey.write("\n  ")
			else:
				advanced = False
				if(self.file_block > 0):
					if(i%self.file_block ==0):
						if(not self.flat_sql):
							self.writey.write(";")
							self.printHeaderSQL(model,False)
						self.writey.close()
						self.writey = open(self.create_indexed_file_name(self.curr_dest,self.start_file+int(i/self.file_block)),'w')
						if(not self.flat_sql):
							self.printHeaderSQL(model,True)	
						advanced = True

				if(i%self.internal_block == 0 and self.internal_block >0  and not broke_entry and not advanced and not self.flat_sql):
					self.writey.write(";")
					self.printHeaderSQL(model,False)
					self.printHeaderSQL(model,True)
					self.writey.write("\n  ")
					advanced = True
				
				if(not advanced):
					if(not self.flat_sql):
						self.writey.write(",\n")
					else:
						self.writey.write("\n")
			records=records+1
			if(not self.flat_sql):
				self.writey.write("(")
			self.writey.write(str(self.start_index+i))
			for v in self.stuff[model]+ADDED_STUFF:
				if(not v[2]=="skip"):
					final_i= i+1
					if("fk"+COMMAND_DELIM in v[2] and additional_locks[v[1]]!=0):
						final_i=(i+self.start_index/additional_locks[v[1]])+1

					val=self.getValue(v[0],v[1],self.start_index+iterations,final_i,v[2],str(self.start_index+i))
					self.writey.write(","+str(val[0]))
			if(not self.flat_sql):
				self.writey.write(")")
			if(i<coreIter):
				self.getNextIndexForModel(model)
			i=i+1
			self.dunentries = self.dunentries+1
			if(self.dunentries % progressBlock == 0):
				pct = self.dunentries / progressBlock
				sys.stdout.flush()
				last_write = datetime.now()
				sys.stdout.write("\x1b]2;Jenny: "+str(pct)+"% Complete\x07")
				sys.stdout.write("\rComplete: ["+("-"*pct)+(" "*(divider-pct))+"] %"+str(pct)+" @ "+str(last_write))
		if(not self.flat_sql):
			self.writey.write(";");
			self.printHeaderSQL(model,False)
		sys.stdout.write("\x1b]2;Jenny\x07")
		return records

	def printHeaderSQL(self,model,start):
		self.writey.write("\n")
		if(start):
			self.writey.write("INSERT INTO `"+model+"` (`id`")
			for data in self.stuff[model]+ADDED_STUFF:
				if(data[2]!="skip"):
					self.writey.write(",`"+data[1]+"`")
			self.writey.write(")\n VALUES")
		else:
			self.writey.write("")

	def printHeaderCSV(self,model,start):
		if(start):
			self.writey.write("id")
			for data in self.stuff[model]+ADDED_STUFF:
				if(data[2]!="skip"):
					self.writey.write(","+data[1]+"")
			self.writey.write("\n")
		else:
			self.writey.write("\n")

	def start_party(self, path, indifferent=False):
		w = open(path,'r')
		currModel=""
		for line in w:
			if("create_table" in line):
				if(self.isRemembered(">>"+line.split('"')[1])):
					if(self.getRemembered(">>"+line.split('"')[1]).find("!")>=0):
						currModel="!"
					else:
						currModel=line.split('"')[1]
				else:
					currModel=""
					self.setRemembered(">>"+line.split('"')[1],currModel)
			elif("t." in line and not currModel == "!" and not currModel == ""):
				self.addField(currModel,line.split('"')[1],line.split("t.")[1].split(" ")[0],indifferent)
