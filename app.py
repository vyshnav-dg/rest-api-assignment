from flask import Flask, request, jsonify

from models.Customer import Customer
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost:3306/Northwind"

db.init_app(app)

@app.route("/")
def hello():
    return "<p>Hello!!</p>"

@app.route("/customers")
def handle_customer():
    match request.method:
        case "GET":
            customers = Customer.query.all()
            cols = Customer.get_cols()
            resp = [{col: getattr(customer, col) for col in cols} for customer in customers]
            return jsonify(resp)
        case "POST":
            print(request.get_json())
        case "PATCH":
            ...

@app.route("/orders")
def handle_order():
    match request.method:
        case "GET":
            ...
        case "POST":
            ...
        case "PATCH":
            ...

@app.route("/products")
def handle_product():
    match request.method:
        case "GET":
            ...
        case "POST":
            ...
        case "PATCH":
            ...