from flask import Blueprint, request, jsonify

from src.db import db
from src.models.Order import Order
from src.utils import get_all_records, insert_record

order_ctrl = Blueprint("order_ctrl", __name__)

@order_ctrl.route("/orders", methods=["GET", "POST"])
def handle_order():
    match request.method:
        case "GET":
            try:
                customer_id = request.args.get("customer_id")
                if customer_id:
                    # Get orders by customer ID
                    orders = db.session.execute(db.select(Order).filter_by(CustomerID=customer_id)).scalars()
                    cols = Order.get_cols()
                    resp = [{col : getattr(order, col) for col in cols} for order in orders]
                else:
                    resp = get_all_records(Order)
                return jsonify(resp), 200
            except Exception as e:
                return f"Error : {e}", 400
        case "POST":
            try:
                response = request.form.to_dict()
                insert_record(response, Order)
                return "Insert success", 200
            except Exception as e:
                return f"Error : {e}", 400

@order_ctrl.route("/orders/<int:order_id>", methods=["PATCH"])
def handle_order_update(order_id):
    try:
        data = request.get_json()
        order = db.session.execute(db.select(Order).filter_by(OrderID=order_id)).scalar_one()
        order.update_vals(data)
        db.session.commit()
        return "Update success", 200
    except Exception as e:
        return f"Error : {e}", 400   