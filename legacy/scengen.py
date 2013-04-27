import os
import verbage
import time
import sys


source = "schema.rb"
destination = "/output/file.sql"
file_block_size=-1
internal_block_size=500
iterations = -1

vw=verbage.verbage()

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
        vw.start_index = int(sys.argv[i+1])
        i=i+1
    elif(sys.argv[i]=="-start_file_no"):
        vw.start_file = int(sys.argv[i+1])
        i=i+1
    elif(sys.argv[i]=="-c"):
        iterations =  int(sys.argv[i+1])
        i=i+1
    elif(sys.argv[i] == "-flat"):
        vw.flat_sql = True

vw.file_block = file_block_size
vw.internal_block = internal_block_size
print "commands:"+str(vw.genActions+vw.addOnActions)
path = '/'
listing = os.listdir(path)

#prompt=vw.getCommandBool("Should you be guiding this?")
prompt=True


vw.start_party(source)

if(iterations==-1):
    iterations = vw.getCommandInt("How many instances of each model do we want??") 
start=time.time()       
num = vw.writeToFile(iterations,destination)
end=time.time()

total=end-start

print "Wrote {:,} test objects in {} seconds".format(num,total)
    		






