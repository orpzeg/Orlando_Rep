from flask import Flask, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/Orlando'
mongo = PyMongo(app)

@app.route('/view', methods=['GET'])
def get_view_data():
    my_view = mongo.db.Final_View
    data = list(my_view.find())
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True)


