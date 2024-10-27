from sqlite3 import IntegrityError
from flask import Flask, jsonify, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import delete_row, select_all, select_where, insert_into, select_user_orders
from utils import place_order

app = Flask(__name__)
app.secret_key = "GIETU, best university in eastern india"

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")
    data = {}
    data['orders'] = select_user_orders(session['user_id']);
    data['items'] = select_all('items')
    return render_template("index.html", data = data)

@app.route("/checkout", methods = ['GET', 'POST'])
def checkout():
    if "user_id" not in session:
        return redirect("/login")

    info = select_where("users", "id", session['user_id'])
    if request.method == 'GET':
        data = {}
        data['orders'] = select_user_orders(session['user_id']);
        data['address'] = info[3]
        return render_template("checkout.html", data=data)
    orders = select_user_orders(session['user_id'])

    if not len(orders):
        return jsonify({ 'msg': "Place atlest one order" }), 400

    place_order(info[1], info[2], info[3], orders)

    delete_row("orders", "user_id", session['user_id'])
    return redirect("/")

@app.route("/order", methods = ['DELETE', 'POST'])
def order():
    if "user_id" not in session:
        return redirect("/login")

    item_id = request.json
    if request.method == "DELETE":
        delete_row("orders", "id", item_id)
        return jsonify({ 'status': 200 })

    try:
        insert_into("orders", ('item_id', 'user_id'), (item_id, session['user_id']))
        return jsonify({ 'status': 200 })
    except IntegrityError:
        return jsonify({ 'status': 400 })

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username, password = request.form['username'], request.form["password"]
    row = select_where('users', 'username', username)
    if row == None:
        return render_template("login.html", message = "invalid username")
    if not check_password_hash(row[4], password):
        return render_template("login.html", message = "invalid password")
    session["user_id"] = row[0]
    session["user_name"] = row[1]
    return redirect("/")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    username, password = request.form['username'], request.form["password"]
    email, addr = request.form["email"], request.form['address']
    if select_where('users', 'username', username):
        return render_template("register.html", message = "username already present")
    if select_where('users', 'email', email):
        return render_template("register.html", message = "email already present")
    password_hash = generate_password_hash(password)
    insert_into('users', ('username', 'email', 'address', 'password_hash'), (username, email, addr, password_hash))
    return redirect("/login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

app.run()
