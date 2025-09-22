from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError, DataError, OperationalError, NoResultFound

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
            except OperationalError as e:
                return jsonify({"error": "Database connection failed", "message": str(e)}), 400
            except Exception as e:
                return jsonify({"error": "Unexpected error", "message": str(e)}), 400
        case "POST":
            try:
                response = request.get_json()
                insert_record(response, Order)
                return jsonify({"message": "Insert success"}), 200
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

@order_ctrl.route("/orders/<int:order_id>", methods=["PATCH"])
def handle_order_update(order_id):
    try:
        data = request.get_json()
        order = db.session.execute(db.select(Order).filter_by(OrderID=order_id)).scalar_one()
        order.update_vals(data)
        db.session.commit()
        return jsonify({"message": "Update success"}), 200

    except NoResultFound:
        return jsonify({"error": "Order not found", "message": f"No order with ID '{order_id}'"}), 400
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