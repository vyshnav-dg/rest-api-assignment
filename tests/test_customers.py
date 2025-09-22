import json
from src.db import db
from src.models.Customer import Customer

sample_customer = {
    "CustomerID": "TEMP11",
    "CompanyName": "Test Company",
    "ContactName": "John Doe",
    "ContactTitle": "Manager",
    "Address": "123 Test St",
    "City": "Testville",
    "Region": "TS",
    "PostalCode": "12345",
    "Country": "Testland",
    "Phone": "123-456-7890",
    "Fax": "123-456-7891"
}

def cleanup_customer(client):
    with client.application.app_context():
        with db.session.begin():
            customer = db.session.get(Customer, sample_customer["CustomerID"])
            if customer:
                db.session.delete(customer)

def test_get_customers(client):
    response = client.get("/customers")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "CustomerID" in data[0]
    assert "CompanyName" in data[0]

def test_post_customer_success(client):
    response = client.post("/customers", json=sample_customer)
    print(response.get_json())
    assert response.status_code == 200
    assert b"Insert success" in response.data
    cleanup_customer(client)

def test_post_customer_duplicate_pk(client):
    client.post("/customers", json=sample_customer)

    response = client.post("/customers", json=sample_customer)
    print(response.get_json())
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error"] == "Integrity error"

    cleanup_customer(client)

def test_post_customer_missing_required_field(client):
    bad_customer = sample_customer.copy()
    bad_customer.pop("CustomerID")
    response = client.post("/customers", json=bad_customer)
    print(response.get_json())
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error"] == "Integrity error" or json_data["error"] == "Unexpected error"

def test_patch_customer_success(client):
    client.post("/customers", json=sample_customer)

    patch_data = {"CompanyName": "Updated Company"}

    response = client.patch(
        f"/customers/{sample_customer['CustomerID']}",
        json=patch_data,
        content_type="application/json"
    )
    print(response.get_json())
    assert response.status_code == 200
    assert b"Update success" in response.data

    cleanup_customer(client)

def test_patch_customer_not_found(client):
    patch_data = {"CompanyName": "Nonexistent"}

    response = client.patch(
        "/customers/UNKNOWNID",
        json=patch_data,
        content_type="application/json"
    )
    print(response.get_json())
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error"] == "Customer not found"
