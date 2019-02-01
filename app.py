from flask import Flask, jsonify, request, abort
from pymongo import MongoClient
from bson import json_util
import json

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.viero
callback = db.callback 

@app.route('/callback/<callback_id>', methods=['GET'])
def get_order_by_id(callback_id):

    return app.response_class(
        response=json.dumps(callback.find_one({'CALLBACKID':'%s' % callback_id}, {'_id': False}), indent=4, default=json_util.default),
        status=200,
        mimetype='application/json'
    )

@app.route('/callback/<callback_id>', methods=['POST'])
def post_order_by_id(callback_id):
    
    data = request.get_json()
    data.update({'CALLBACKID':'%s' % callback_id})
    callback.insert(data)

    return app.response_class(
        response="{}",
        status=200,
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(debug=True)
