from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)


# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['image-gpt']
users_collection = db['users']

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Check if the user already exists
    if users_collection.find_one({'username': username}):
        return jsonify({'message': 'User already exists'}), 409

    # Hash the user's password before storing it
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({'username': username, 'password': hashed_password})

    # Successfully created the user
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Find the user by username
    user = users_collection.find_one({'username': username})
    if not user or not check_password_hash(user['password'], password):
        # Authentication failed
        return jsonify({'message': 'Invalid credentials'}), 401

    # Authentication successful
    return jsonify({'message': 'Logged in successfully'})


@app.after_request
def after_request(response):
    # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    # response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    # response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')



    return response

if __name__ == '__main__':
    app.run(debug=True)
