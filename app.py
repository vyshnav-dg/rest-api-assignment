from flask import Flask, request, jsonify, render_template

from models.Customer import Customer
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost:3306/Northwind"

db.init_app(app)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/customers", methods=["GET", "POST"])
def handle_customer():
    match request.method:
        case "GET":
            customers = db.session.execute(db.select(Customer)).scalars()
            cols = Customer.get_cols()
            resp = [{col: getattr(customer, col) for col in cols} for customer in customers]
            return jsonify(resp)
        case "POST":
            try:
                response = request.form.to_dict()
                customer = Customer(response)
                db.session.add(customer)
                db.session.commit()
                return "Insert success", 200
            except Exception as e:
                return f"Error : {e}", 400

@app.route("/customers/<customer_id>", methods=["PATCH"])
def handle_customer_update(customer_id):
    try:
        data = request.get_json()
        customer = db.session.execute(db.select(Customer).filter_by(CustomerID=customer_id)).scalar_one()
        customer.update_vals(data)
        db.session.commit()
        return "Update success", 200
    except Exception as e:
        return f"Error : {e}", 400

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