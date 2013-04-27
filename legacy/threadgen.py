import threading
import os
import sys


class ThreadClass(threading.Thread):
	def __init__(self,s,d,ibs,fbs,start_index,start_file,iterations):
		super(ThreadClass, self).__init__()
		self.s = s 
		self.d = d 
		self.fbs = fbs
		self.ibs = ibs
		self.start_file = start_file
		self.start_dex = start_index
		self.iterations = iterations

	def run(self):
		os.system("python scengen.py -s "+self.s+" -d "+self.d+" -fblock "+str(self.fbs)+" -iblock "+str(self.ibs)+" -start_file_no "+str(self.start_file)+" -start_index "+str(self.start_dex)+" -c "+str(self.iterations))
source = ""
destination = ""
internal_block_size = 0
file_block_size = 0
start_dex = 0
start_file = 0
iterations = 0
threads = 4
for i in range(1,len(sys.argv)-1):
    if(sys.argv[i]=="-s"):
        source = sys.argv[i+1]
        i=i+1
    elif(sys.argv[i]=="-d"):
        destination = sys.argv[i+1]
        i=i+1
    elif(sys.argv[i]=="-iblock"):
        internal_block_size = int(sys.argv[i+1])
        i=i+1
    elif(sys.argv[i]=="-fblock"):
        file_block_size = int(sys.argv[i+1])
        i=i+1
    elif(sys.argv[i]=="-start_index"):
        start_dex = int(sys.argv[i+1])
        i=i+1
    elif(sys.argv[i]=="-start_file_no"):
        start_file = int(sys.argv[i+1])
        i=i+1
    elif(sys.argv[i]=="-c"):
        iterations =  int(sys.argv[i+1])
        i=i+1
    elif(sys.argv[i]=="-threads"):
    	threads =  int(sys.argv[i+1])
        i=i+1

split = iterations / threads

proc_array = []
for i in range(threads):
	t=ThreadClass(source, destination, internal_block_size, file_block_size, (i*split)+start_dex , ((i*split)/file_block_size)+start_file, split)
	t.start()
	proc_array.append(t)

		