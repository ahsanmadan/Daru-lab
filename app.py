from flask import (
    Flask, render_template, jsonify, request, session, redirect, url_for
)
from pymongo import MongoClient
import jwt
from datetime import datetime

client = MongoClient(
    "mongodb+srv://test:asan@cluster0.hmhssac.mongodb.net/?retryWrites=true&w=majority")
db = client.daru
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')
