from flask import Blueprint, request, jsonify

from db import db
from models.Product import Product
from utils import get_all_records, insert_record

product_ctrl = Blueprint("product_ctrl", __name__)

@product_ctrl.route("/products", methods= ["GET", "POST"])
def handle_product():
    match request.method:
        case "GET":
            try:
                resp = get_all_records(Product)
                return jsonify(resp), 200
            except Exception as e:
                return f"Error : {e}", 400
        case "POST":
            try:
                response = request.form.to_dict()
                if response.get("Discontinued"):
                    response["Discontinued"] = response["Discontinued"].lower() == "true"
                insert_record(response, Product)
                return "Insert success", 200
            except Exception as e:
                return f"Error : {e}", 400
            
@product_ctrl.route("/products/<int:product_id>", methods=["PATCH"])
def handle_product_update(product_id):
    try:
        data = request.get_json()
        product = db.session.execute(db.select(Product).filter_by(ProductID=product_id)).scalar_one()
        product.update_vals(data)
        db.session.commit()
        return "Update success", 200
    except Exception as e:
        return f"Error : {e}", 400  