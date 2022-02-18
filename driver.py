from flask import Flask, send_from_directory, request, render_template, jsonify
from flask_restful import Api, Resource, reqparse
#from flask_cors import CORS #comment this on deployment
from api.HelloApiHandler import HelloApiHandler
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
from pymongo import MongoClient
import pymongo
client = pymongo.MongoClient("mongodb+srv://basicuser:123@crudproject.rqnu3.mongodb.net/crudproject?retryWrites=true&w=majority")
db = client.crudproject

app = Flask(__name__)
CORS(app)
@app.route('/')
def get():
    return {
      'resultStatus': 'SUCCESS',
      'message': "Hello Api Handler"
      }

@app.route('/users', methods=['POST', 'GET'])
def data():
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        pid = body['pid']
        name = body['name']
        points = body['points'] 
        # db.users.insert_one({
        db['users'].insert_one({
            "pid": pid,
            "name": name,
            "points":points
        })
        return jsonify({
            'status': 'Data is posted to MongoDB!',
            "pid": pid,
            "name": name,
            "points":points
        })
    
    # GET all data from database
    if request.method == 'GET':
        allData = db['users'].find()
        dataJson = []
        for data in allData:
            pid = data['pid']
            name = data['name']
            points = data['points']
            dataDict = {
                'pid': pid,
                'name': name,
                'points': points
            }
            dataJson.append(dataDict)
        print(dataJson)
        return jsonify(dataJson)

@app.route('/users/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    # GET a specific data by id
    try:
        if request.method == 'GET':
            data = db['users'].find_one({'pid': id})
            pid = data['pid']
            name = data['name']
            points = data['points']
            dataDict = {
                'pid': pid,
                'name': name,
                'points':points
            }
            print(dataDict)
            return jsonify(dataDict)
        
    # DELETE a data
        if request.method == 'DELETE':
            db['users'].delete_many({'pid': id})
            print('\n # Deletion successful # \n')
            return jsonify({'status': 'Data id: ' + id + ' is deleted!'})

    # UPDATE a data by id
        if request.method == 'PUT':
            body = request.json
            pid = body['pid']
            name = body['name']
            points = body['points']

            db['users'].update_one(
                {'pid':id},
                {
                    "$set": {
                        "pid": pid,
                        "name":name,
                        "points": points
                    }
                }
            )

            print('\n # Update successful # \n')
            return jsonify({'status': 'Data id: ' + id + ' is updated!'})
    except TypeError:
        return {
      'resultStatus': 'failed',
      'message': "user does not exist."
      }



#api.add_resource(HelloApiHandler, '/')

#def loadtable():
 #   items = table
  #  chart = ItemTable(items)
   # return chart.__html__()


#def serve(path):
#    return send_from_directory(app.static_folder,'index.html')

#api.add_resource(HelloApiHandler, '/')