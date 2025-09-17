from flask import Flask, render_template

from db import db

from controllers import customer_controller, order_controller, product_controller


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost:3306/Northwind"

db.init_app(app)

app.register_blueprint(customer_controller.customer_ctrl)
app.register_blueprint(order_controller.order_ctrl)
app.register_blueprint(product_controller.product_ctrl)

@app.route("/")
def hello():
    return render_template("index.html")