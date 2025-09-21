from unittest.mock import patch, MagicMock
from sqlalchemy.exc import NoResultFound
from src.models.Product import Product

@patch("src.controllers.product_controller.get_all_records")
def test_get_products(mock_get_all, client):
    mock_get_all.return_value = [{"ProductID": 1, "Name": "Test"}]
    response = client.get("/products")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"ProductID": 1, "Name": "Test"}]
    mock_get_all.assert_called_once()

@patch("src.controllers.product_controller.insert_record")
def test_post_product(mock_insert, client):
    data = {"Name": "New Product", "Discontinued": "true"}
    response = client.post("/products", data=data)

    assert response.status_code == 200
    assert "Insert success" in response.get_data(as_text=True)
    mock_insert.assert_called_once()
    inserted_data = mock_insert.call_args[0][0]
    assert inserted_data["Discontinued"] is True

@patch("src.controllers.product_controller.db.session")
def test_patch_product(mock_session, client):
    mock_product = MagicMock()
    mock_session.execute.return_value.scalar_one.return_value = mock_product

    response = client.patch("/products/1", json={"Name": "Updated"})

    assert response.status_code == 200
    assert "Update success" in response.get_data(as_text=True)
    mock_product.update_vals.assert_called_once_with({"Name": "Updated"})
    mock_session.commit.assert_called_once()

@patch("src.controllers.product_controller.get_all_records")
def test_get_products_exception(mock_get_all, client):
    mock_get_all.side_effect = Exception("DB error")
    response = client.get("/products")

    assert response.status_code == 400
    assert "Error : DB error" in response.get_data(as_text=True)

@patch("src.controllers.product_controller.insert_record")
def test_post_product_invalid_discontinued(mock_insert, client):
    data = {"Name": "New Product", "Discontinued": "not-a-boolean"}
    response = client.post("/products", data=data)

    assert response.status_code == 200
    mock_insert.assert_called_once()
    inserted_data = mock_insert.call_args[0][0]
    assert inserted_data["Discontinued"] is False

@patch("src.controllers.product_controller.db.session")
def test_patch_product_not_found(mock_session, client):
    mock_session.execute.return_value.scalar_one.side_effect = NoResultFound()
    response = client.patch("/products/999", json={"Name": "Ghost"})

    assert response.status_code == 400
    assert "Error" in response.get_data(as_text=True)