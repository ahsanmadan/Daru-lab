from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://test:asan@cluster0.hmhssac.mongodb.net/?retryWrites=true&w=majority")
db = client.daru
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')    