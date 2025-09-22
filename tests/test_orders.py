import json
from src.db import db
from src.models.Order import Order

sample_order = {
    "OrderID": 99999,
    "CustomerID": "CUST123",
    "EmployeeID": 1,
    "OrderDate": "2025-09-20",
    "RequiredDate": "2025-09-25",
    "ShippedDate": "2025-09-21",
    "ShipVia": 1,
    "Freight": "50.00",
    "ShipName": "Test Shipping",
    "ShipAddress": "123 Test Street",
    "ShipCity": "Testville",
    "ShipRegion": "TestState",
    "ShipPostalCode": "12345",
    "ShipCountry": "Testland"
}

def cleanup_order(client):
    with client.application.app_context():
        with db.session.begin():
            order = db.session.get(Order, sample_order["OrderID"])
            if order:
                db.session.delete(order)

def test_get_orders(client):
    response = client.get("/orders")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "OrderID" in data[0]
    assert "CustomerID" in data[0]

def test_post_order_success(client):
    response = client.post("/orders", json=sample_order)
    print(response.get_json())
    assert response.status_code == 200
    assert b"Insert success" in response.data
    cleanup_order(client)

def test_post_order_duplicate_pk(client):
    client.post("/orders", json=sample_order)

    response = client.post("/orders", json=sample_order)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data["error"] == "Integrity error"

    cleanup_order(client)

def test_patch_order_success(client):
    client.post("/orders", json=sample_order)

    patch_data = {"ShipCity": "UpdatedCity"}

    response = client.patch(
        f"/orders/{sample_order['OrderID']}",
        data=json.dumps(patch_data),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert b"Update success" in response.data

    cleanup_order(client)

def test_patch_order_not_found(client):
    patch_data = {"ShipCity": "GhostTown"}

    response = client.patch(
        "/orders/999999999",
        data=json.dumps(patch_data),
        content_type="application/json"
    )
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data["error"] == "Order not found"

def test_patch_order_invalid_data(client):
    client.post("/orders", json=sample_order)

    patch_data = {"Freight": "not_a_number"}

    response = client.patch(
        f"/orders/{sample_order['OrderID']}",
        data=json.dumps(patch_data),
        content_type="application/json"
    )
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data["error"] in ("Invalid data", "Integrity error", "Unexpected error", "Database operation failed")

    cleanup_order(client)
