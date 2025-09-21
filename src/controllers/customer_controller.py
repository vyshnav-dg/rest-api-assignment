from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError, DataError, OperationalError, NoResultFound
from src.db import db
from src.utils import get_all_records, insert_record
from src.models.Customer import Customer

customer_ctrl = Blueprint("customer_ctrl", __name__)

@customer_ctrl.route("/customers", methods=["GET", "POST"])
def handle_customer():
    if request.method == "GET":
        try:
            resp = get_all_records(Customer)
            return jsonify(resp), 200
        except OperationalError as e:
            return jsonify({"error": "Database connection failed", "message": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Unexpected error", "message": str(e)}), 400

    elif request.method == "POST":
        try:
            response = request.form.to_dict()
            insert_record(response, Customer)
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

@customer_ctrl.route("/customers/<customer_id>", methods=["PATCH"])
def handle_customer_update(customer_id):
    try:
        data = request.get_json()
        customer = db.session.execute(
            db.select(Customer).filter_by(CustomerID=customer_id)
        ).scalar_one()
        customer.update_vals(data)
        db.session.commit()
        return "Update success", 200

    except NoResultFound:
        return jsonify({"error": "Customer not found", "message": f"No customer with ID '{customer_id}'"}), 404
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
