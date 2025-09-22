import json
from src.db import db
from src.models.Product import Product

sample_product = {
    "ProductID": 99999,
    "ProductName": "Test Product",
    "SupplierID": 1,
    "CategoryID": 1,
    "QuantityPerUnit": "10 boxes",
    "UnitPrice": "15.50",
    "UnitsInStock": 20,
    "UnitsOnOrder": 5,
    "ReorderLevel": 2,
    "Discontinued": False
}


def cleanup_product(client):
    with client.application.app_context():
        with db.session.begin():
            product = db.session.get(Product, sample_product["ProductID"])
            if product:
                db.session.delete(product)

def test_get_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "ProductID" in data[0]
    assert "ProductName" in data[0]

def test_post_product_success(client):
    response = client.post("/products", json=sample_product)
    assert response.status_code == 200
    assert b"Insert success" in response.data
    cleanup_product(client)

def test_post_product_duplicate_pk(client):
    client.post("/products", json=sample_product)

    response = client.post("/products", json=sample_product)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data["error"] == "Integrity error"

    cleanup_product(client)

def test_patch_product_success(client):
    client.post("/products", json=sample_product)

    patch_data = {"ProductName": "Updated Product"}

    response = client.patch(
        f"/products/{sample_product['ProductID']}",
        data=json.dumps(patch_data),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert b"Update success" in response.data

    cleanup_product(client)

def test_patch_product_not_found(client):
    patch_data = {"ProductName": "Nonexistent"}

    response = client.patch(
        "/products/999999999",
        data=json.dumps(patch_data),
        content_type="application/json"
    )
    json_data = response.get_json()
    assert response.status_code == 400  
    assert json_data["error"] == "Product not found"

def test_patch_product_invalid_data(client):
    client.post("/products", json=sample_product)

    patch_data = {"UnitPrice": "invalid_price"}

    response = client.patch(
        f"/products/{sample_product['ProductID']}",
        data=json.dumps(patch_data),
        content_type="application/json"
    )
    json_data = response.get_json()
    print(json_data)
    assert response.status_code == 400
    assert json_data["error"] in ("Invalid data", "Integrity error", "Unexpected error", "Database operation failed")

    cleanup_product(client)
