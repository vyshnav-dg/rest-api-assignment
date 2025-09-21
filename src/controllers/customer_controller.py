from flask import Blueprint, request, jsonify

from src.db import db
from src.utils import get_all_records, insert_record
from src.models.Customer import Customer

customer_ctrl = Blueprint("customer_ctrl", __name__)

@customer_ctrl.route("/customers", methods=["GET", "POST"])
def handle_customer():
    match request.method:
        case "GET":
            try:
                resp = get_all_records(Customer)
                return jsonify(resp), 200
            except Exception as e:
                return jsonify({
                    "error": "ERROR",
                    "message": str(e)
                }), 400
        case "POST":
            try:
                response = request.form.to_dict()
                insert_record(response, Customer)
                return "Insert success", 200
            except Exception as e:
                return jsonify({
                    "error": "ERROR",
                    "message": str(e)
                }), 400
@customer_ctrl.route("/customers/<customer_id>", methods=["PATCH"])
def handle_customer_update(customer_id):
    try:
        data = request.get_json()
        customer = db.session.execute(db.select(Customer).filter_by(CustomerID=customer_id)).scalar_one()
        customer.update_vals(data)
        db.session.commit()
        return "Update success", 200
    except Exception as e:
        return jsonify({
            "error": "ERROR",
            "message": str(e)
        }), 400