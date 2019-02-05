from flask import Flask
from flask_restful import Resource, Api, reqparse, request
import sys

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('HashEntry')

data = {}


class HashProj(Resource):
    def get(self):
        print(data)
        return data

    def post(self):
        url_id = 1
        if len(data) > 0:
            url_id = len(data["entries"])+1
        #print(url_id)
        data["Num_entries"] = url_id
        #print(data)
        data.setdefault("entries", []).append(request.json)
        return '201 Created'


api.add_resource(HashProj, '/api/v1/entries')

if __name__ == '__main__':
    app.run(debug=True,port=int(sys.argv[1]))
