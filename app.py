from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from pymongo import MongoClient
import jwt
import datetime
import hashlib
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import requests
import os
from bson import ObjectId
from os.path import join, dirname
import shutil
import uuid
import random
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
SECRET_KEY = "DARU"

uri = "mongodb+srv://test:clean@cluster0.hmhssac.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.daru

TOKEN_KEY = "mytoken"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/faq')
def faq():
    return render_template('FAQs.html')


@app.route('/produk')
def produk():
    data = list(db.produk.find({}))
    return render_template('Produk.html', data=data)


@app.route('/us')
def us():
    return render_template('us.html')


@app.route('/dampak')
def dampak():
    return render_template('dampak.html')


@app.route('/produk1')
def produk1():
    return render_template('detail-Produk1.html')


@app.route('/produk2')
def produk2():
    return render_template('detail-Produk2.html')


@app.route('/produk3')
def produk3():
    return render_template('detail-Produk3.html')


@app.route('/produk4')
def produk4():
    return render_template('detail-Produk4.html')


# def verify_password(password):
#     # Gantilah dengan logika verifikasi password yang sesuai
#     return password == 'daru'


@app.route('/login', methods=['POST', 'GET'])
def login():
    # # Menggunakan POST untuk ambil password
    # password = request.form.get('password')

    # if not verify_password(password):
    #     # Menampilkan pesan kesalahan dengan alert JavaScript
    #     return render_template('index.html', msg=None, error_message="Password salah! Anda tidak diizinkan mengakses halaman ini")

    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )

        if 'username' not in session:
            return redirect(url_for('login', msg='Please login first'))

        user_info = db.users.find_one({'username': payload.get('id')})
        return redirect(url_for('dashboard', user_info=user_info))
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        msg = request.args.get('msg')
        return render_template('login.html', msg=msg, error_message=None)


@app.route("/sign_in", methods=["POST"])
def sign_in():
    # Sign in
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    result = db.users.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
    )
    if result:
        payload = {
            'id': username_receive,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        session['username'] = username_receive
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({
            "result": "fail",
            "msg": "We could not find a user with that id/password combination",
        })


@app.route("/save", methods=["POST"])
def sign_up():
    username_receive = request.form["username_give"]
    nama_receive = request.form["nama_give"]
    password_receive = request.form["password_give"]
    password_hash = hashlib.sha256(
        password_receive.encode("utf-8")).hexdigest()
    doc = {
        "username": username_receive,  # id
        "password": password_hash,  # password
        "nama_lengkap": nama_receive,  # user's name is set to their id by default
    }
    result = db.users.insert_one(doc)
    if result:
        payload = {
            'id': username_receive,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        session['username'] = username_receive
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({
            "result": "fail",
            "msg": "Something Wrong",
        })


@app.route("/admin", methods=["POST", "GET"])
def admin():

    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({'username': payload.get('id')})

        return render_template("admin-home.html", user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Your login session has expired, please log in again"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="Please login first"))


@app.route("/admin/product", methods=["POST", "GET"])
def admin_product():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({'username': payload.get('id')})
        data = list(db.produk.find({}))
        return render_template("admin-product.html", user_info=user_info, data=data)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Your login session has expired, please log in again"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="Please login first"))


# bagian user


@app.route("/admin/user", methods=["POST", "GET"])
def admin_user():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({'username': payload.get('id')})
        data = list(db.users.find({}))
        return render_template("admin-user.html", user_info=user_info, data=data)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Your login session has expired, please log in again"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="Please login first"))


@app.route("/admin/comment", methods=["POST", "GET"])
def admin_comment():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({'username': payload.get('id')})
        data = list(db.users.find({}))
        return render_template("admin-comment.html", user_info=user_info, data=data)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Your login session has expired, please log in again"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="Please login first"))


@app.route("/deleteUser", methods=['GET'])
def deleteUser():
    id = request.args.get("id")
    db.users.delete_one({'_id': ObjectId(id)})
    data = db.users.find({})
    return render_template("admin-user.html", data=data)
# akhir bagian user


@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('name', None)
    return redirect("/")


# @app.route('/getUsers', methods=['GET'])
# def getUsers():
#     data = list(db.users.find({}))
#     return jsonify({'users': Alluser})

# untuk mengubah format rupiah


def format_rupiah(amount):
    # Ubah angka menjadi string dan tambahkan '0' di depan jika panjangnya kurang dari 3
    amount_str = str(amount).rjust(3, '0')

    # Pisahkan angka menjadi grup-grup yang terdiri dari 3 digit, mulai dari digit paling belakang
    groups = []
    while amount_str:
        groups.append(amount_str[-3:])
        amount_str = amount_str[:-3]

    # Gabungkan grup-grup dengan pemisah '.'
    formatted_amount = '.'.join(reversed(groups))
    return formatted_amount
# post card ke page produk dan dashboard produk

# random id


def generate_random_id(min_value, max_value):
    return random.randint(min_value, max_value)


@app.route('/save_product', methods=['POST'])
def save_product():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        user_info = db.users.find_one({'username': payload.get('id')})
        # membuat id acak
        # Membuat UUID versi 4 (ID acak)
        random_id = generate_random_id(1000, 9999)
        # buat kode input data disini
        idProduk = random_id
        pname_receive = request.form.get('pname_give')
        ppic_receive = request.files['ppic_give']
        price_receive = request.form.get('price_give')  # Ambil jenis layout
        format_price = format_rupiah(price_receive)
        desc = request.form.get('desc_give')

        # Mencari nomor folder terakhir
        last_folder = db.produk.find_one(
            sort=[('folder', -1)], projection={'folder': 1})
        if last_folder and 'folder' in last_folder:
            last_number = int(
                last_folder['folder'].replace('detailProduk', ''))
            detail = f"detailProduk{last_number + 1}"
        else:
            detail = "detailProduk1"

        directory = f'static/img/detail_product/{detail}'
        os.makedirs(directory, exist_ok=True)

        # akhir kode cari folder

        extension = ppic_receive.filename.split('.')[1]
        filename = f'{directory}/{pname_receive}.{extension}'
        ppic_receive.save(filename)

        card_ppic = f'img/detail_product/{detail}/{pname_receive}.{extension}'

        doc = {
            'idProduk': idProduk,
            'pname': pname_receive,
            'ppic': card_ppic,
            'folder': detail,
            'price': format_price,
            'desc': desc,
        }
        db.produk.insert_one(doc)
        return jsonify({'msg': 'Product added successfully', 'result': 'success'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('/login'))

# deleteProduct


@app.route("/deleteProduk", methods=['POST'])
def hapusProduk():
    id = request.form["id_give"]
    check = db.produk.find_one({'idProduk': int(id)})

    if check:
        # hapus folder
        folder_delete = check['folder']
        folder_path = os.path.join(
            'static', 'img', 'detail_product', folder_delete)

        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        db.produk.delete_one({'idProduk': int(id)})
        db.detail_produk.delete_many({'folder': check.get('folder')})
        return jsonify({"msg": "Produk berhasil di hapus"})
    else:
        return jsonify({"msg": "Produk tidak ditemukan"})


@app.route('/admin/fill-edit/<int:id>', methods=['GET'])
def fill_edit(id):
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )

        fill = db.produk.find_one({'idProduk': id}, {'_id': False})

        if save_product:
            return jsonify({'result': 'success', 'post': fill})
        else:
            return jsonify({'result': 'error', 'msg': 'Tambahkan Produk terlebih dahulu'}), 404

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))


@app.route('/admin/prosesEdit/<int:id>', methods=['POST'])
def prosesEdit(id):
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )

        pname_receive = request.form.get('pname-give')
        price_receive = request.form.get('price-give')
        format_price = format_rupiah(price_receive)
        desc = request.form.get('desc-give')

        if "ppic_give" in request.files:
            new_image = request.files['ppic-give']

            old_post = db.produk.find_one({'idProduk': id})
            old_image_path = old_post.get('ppic')

            if new_image:
                # mengambil varialbel folder di database
                folder = db.produk.find_one({'idProduk': id}, {"folder": 1})
                # Lakukan penyimpanan file gambar yang baru
                extension = new_image.filename.split(
                    '.')[-1]  # Ambil ekstensi dengan benar
                filename = f'static/img/detail_product/{folder}/{pname_receive}.{extension}'
                new_image.save(filename)

                new_image_path = f'img/detail_product/{folder}/{pname_receive}.{extension}'
                db.produk.update_one({'idProduk': id},
                                     {'$set': {'pname': pname_receive, 'desc': desc, 'price': format_price, 'ppic': new_image_path}})

                # Hapus gambar yang lama
                if old_image_path:
                    old_image_file = os.path.join('static', old_image_path)
                    if os.path.exists(old_image_file):
                        os.remove(old_image_file)

        else:
            # Jika tidak ada file yang diunggah, tetap perbarui title dan layout
            db.produk.update_one(
                {'idProduk': id}, {'$set': {'pname': pname_receive, 'desc': desc, 'price': format_price}})

        return jsonify({'result': 'success', 'msg': 'Data produk telah diperbarui'})

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))


@app.route('/produk/<folder>', methods=['GET'])
def produkdetail(folder):
    post = db.produk.find_one({'folder': folder}, {'_id': False})
    id = post.get('idProduk')

    if id:
        list_folder = post.get('folder')

        detail = list(db.product_detail.find(
            {'folder': list_folder}, {'_id': False}))
    # Periksa apakah 'username' ada dalam sesi
    username = session.get('username')

    return render_template('detailproduk.html', post=post, detail=detail, username=username)


@app.route('/tambahDetailProduk', methods=['POST'])
def tambahdetail():
    data = request.get_json()
    daftar_cara_pemakaian = data['daftarCaraPemakaian'].split('\n')

    doc = {
        "penggunaan" : daftar_cara_pemakaian,
    }
    return jsonify({'result': 'success', 'msg': 'Detil produk berhasil di tambahkan'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
