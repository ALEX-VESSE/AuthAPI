import os
import requests
import json
from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from logging import FileHandler,WARNING

app = Flask(__name__, template_folder="template")
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
MONGODB_URI =""
client = MongoClient(MONGODB_URI)
db = client['my_database']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        if request.is_json:
            username = request.json['username']
            password = request.json['password']

        if db.users.find_one({'username': username}):
            return jsonify({'error': 'Username already exists'}), 400

        user = {'username': username, 'password': generate_password_hash(password)}
        db.users.insert_one(user)
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        print(f"Error during user creation: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/signin', methods=['POST'])
def signin():
    try:
        if request.is_json:
            username = request.json['username']
            password = request.json['password']

        user = db.users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username  
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    except (KeyError, TypeError):
        return jsonify({'error': 'Invalid JSON data'}), 400

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    username = session['username']
    return render_template('dashboard.html', username=username)

@app.route('/update_user', methods=['POST'])
def update_user():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        if request.is_json:
            current_username = session['username']  
           
            update_filter = {'username': current_username}  
            update_data = {'$set': {'username': 'new_username', 'password': generate_password_hash('new_password')}} 
            db.users.update_one(update_filter, update_data)

            session['username'] = 'new_username'  

            return jsonify({'message': 'User information updated successfully'}), 200
    except Exception as e:
        print(f"Error during user update: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run()
