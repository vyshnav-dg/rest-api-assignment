from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError, DataError, OperationalError, NoResultFound

from src.db import db
from src.models.Product import Product
from src.utils import get_all_records, insert_record

product_ctrl = Blueprint("product_ctrl", __name__)

@product_ctrl.route("/products", methods= ["GET", "POST"])
def handle_product():
    match request.method:
        case "GET":
            try:
                resp = get_all_records(Product)
                return jsonify(resp), 200
            except OperationalError as e:
                return jsonify({"error": "Database connection failed", "message": str(e)}), 400
            except Exception as e:
                return jsonify({"error": "Unexpected error", "message": str(e)}), 400
        case "POST":
            try:
                response = request.form.to_dict()
                if response.get("Discontinued"):
                    response["Discontinued"] = response["Discontinued"].lower() == "true"
                insert_record(response, Product)
                return "Insert success", 200
            except IntegrityError as e:
                db.session.rollback()
                return jsonify({"error": "Integrity error", "message": "Duplicate Primary Key or missing required fields"}), 400
            except DataError as e:
                db.session.rollback()
                return jsonify({"error": "Invalid data", "message": str(e)}), 400
            except OperationalError as e:
                return jsonify({"error": "Database operation failed", "message": str(e)}), 400
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": "Unexpected error", "message": str(e)}), 400
            
@product_ctrl.route("/products/<int:product_id>", methods=["PATCH"])
def handle_product_update(product_id):
    try:
        data = request.get_json()
        product = db.session.execute(db.select(Product).filter_by(ProductID=product_id)).scalar_one()
        product.update_vals(data)
        db.session.commit()
        return "Update success", 200

    except NoResultFound:
        return jsonify({"error": "Customer not found", "message": f"No customer with ID '{product_id}'"}), 404
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Integrity error", "message": "Duplicate Primary Key or missing required fields"}), 400
    except DataError as e:
        db.session.rollback()
        return jsonify({"error": "Invalid data", "message": str(e.orig)}), 400
    except OperationalError as e:
        return jsonify({"error": "Database operation failed", "message": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Unexpected error", "message": str(e)}), 400