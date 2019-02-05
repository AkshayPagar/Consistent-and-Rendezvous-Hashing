import flask
import requests
import csv
import hashlib
import sys
import json
servers = ['5000', '5001', '5002', '5003']

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 0:
            keyString = row[0] + row[1] + row[3]
            key = int(hashlib.sha256(keyString.encode('utf-8')).hexdigest(), 16) % 10 ** 8
            target = 0
            index = 0
            if line_count > 0:
                for i in range(0, len(servers)):
                    hashString = keyString + servers[i]
                    serverHash = int(hashlib.sha256(hashString.encode('utf-8')).hexdigest(), 16) % 10 ** 8
                    if target == 0 or target < serverHash:
                        target = serverHash
                        index = i

                data = "{\"" + str(key) + "\":\"" + row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," + row[
                    4] + "," + row[5] + "\"}"


            result_post = requests.post('http://localhost:'+servers[index]+'/api/v1/entries',
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
            print(result_post.content.decode())

            line_count = line_count + 1

        if line_count == 0:
            line_count = line_count + 1

print("Uploaded all "+str(line_count-1)+" entries\n")
print("Verifying the data\n")
f= open("output.txt", "w+")
f.write("Uploaded all "+str(line_count-1)+" entries\n")
f.write("Verifying the data\n")
for i in range(0, len(servers)):
    print("GET http://localhost:"+servers[i])
    f.write("GET http://localhost:"+servers[i])	
    result = requests.get('http://localhost:'+servers[i]+'/api/v1/entries')
    print(result.content.decode())
    f.write(result.content.decode())	

