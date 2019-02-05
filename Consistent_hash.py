import flask
import requests
import csv
import hashlib
import sys

servers = ['5000','5001','5002','5003']
serverHash=[]

for i in range(0,len(servers)):
    m=int(hashlib.sha256(servers[i].encode('utf-8')).hexdigest(), 16) % 10**8
    serverHash.append(m)


with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 0:
            hashString=row[0] + row[1] + row[3]
            key=int(hashlib.sha256(hashString.encode('utf-8')).hexdigest(), 16) % 10**8
            data = "{\""+str(key)+"\":\""+row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+","+row[5]+"\"}"
            
            target = ""
            for i in range(0, len(serverHash)):
                if key < serverHash[i]:
                    if target == "":
                        target = i
                    elif serverHash[target] > serverHash[i]:
                        target = i
                elif key > max(serverHash):
                    target = serverHash.index(min(serverHash))

            result_post = requests.post('http://localhost:' + servers[target] + '/api/v1/entries',
                                 data=data,
                                 headers={'Content-Type': 'application/json'})

            print(result_post.content.decode())
            line_count = line_count + 1

        if line_count==0:
            line_count= line_count+1

print("Uploaded all "+str(line_count-1)+" entries\n")
print("Verifying the data\n")
f= open("output1.txt", "w+")
f.write("Uploaded all "+str(line_count-1)+" entries\n")
f.write("Verifying the data\n")
for i in range(0, len(servers)):
    print("GET http://localhost:"+servers[i])
    f.write("GET http://localhost:"+servers[i])	
    result = requests.get('http://localhost:'+servers[i]+'/api/v1/entries')
    print(result.content.decode())
    f.write(result.content.decode())	
