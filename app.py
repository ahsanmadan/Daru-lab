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

@app.route('/faq')
def faq():
    return render_template('FAQs.html')
    
@app.route('/produk')
def produk():
    return render_template('Produk.html')

@app.route('/us')
def us():
    return render_template('us.html')

@app.route('/dampak')
def dampak():
    return render_template('dampak.html')

@app.route('/produk1')
def produk1():
    return render_template ('detailProduk1.html')

@app.route('/produk2')
def produk2():
    return render_template ('detailProduk2.html')

@app.route('/produk3')
def produk3():
    return render_template ('detailProduk3.html')

@app.route('/produk4')
def produk4():
    return render_template ('detailProduk4.html')

@app.route('/login')
def login():
    return render_template('login.html')





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)