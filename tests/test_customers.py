from unittest.mock import patch, MagicMock
from sqlalchemy.exc import NoResultFound
from src.controllers.customer_controller import handle_customer_update
from src.models.Customer import Customer

@patch("src.controllers.customer_controller.get_all_records")
def test_get_all_customers(mock_get_all, client):
    mock_get_all.return_value = [{"CustomerID": "C001", "Name": "Alice"}]
    response = client.get("/customers")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"CustomerID": "C001", "Name": "Alice"}]
    assert "Alice" in response.get_data(as_text=True)

@patch("src.controllers.customer_controller.insert_record")
def test_post_customer(mock_insert, client):
    data = {"CustomerID": "C002", "Name": "Bob"}
    response = client.post("/customers", data=data)

    assert response.status_code == 200
    assert "Insert success" in response.get_data(as_text=True)
    mock_insert.assert_called_once_with(data, Customer)

@patch("src.controllers.customer_controller.db.session")
def test_patch_customer_success(mock_session, client):
    mock_customer = MagicMock()
    mock_session.execute.return_value.scalar_one.return_value = mock_customer

    update_data = {"Name": "Charlie"}
    response = client.patch("/customers/C001", json=update_data)

    assert response.status_code == 200
    assert "Update success" in response.get_data(as_text=True)
    mock_customer.update_vals.assert_called_once_with(update_data)
    mock_session.commit.assert_called_once()

@patch("src.controllers.customer_controller.get_all_records")
def test_get_customers_db_error(mock_get_all, client):
    mock_get_all.side_effect = Exception("Database failure")
    response = client.get("/customers")
    assert response.status_code == 400
    assert "Error : Database failure" in response.get_data(as_text=True)

@patch("src.controllers.customer_controller.insert_record")
def test_post_customer_insert_error(mock_insert, client):
    mock_insert.side_effect = Exception("Insert failed")
    data = {"CustomerID": "C002", "Name": "Bob"}
    response = client.post("/customers", data=data)
    assert response.status_code == 400
    assert "Error : Insert failed" in response.get_data(as_text=True)

@patch("src.controllers.customer_controller.db.session")
def test_patch_customer_not_found(mock_session, client):
    mock_session.execute.return_value.scalar_one.side_effect = NoResultFound()
    response = client.patch("/customers/INVALID", json={"Name": "Ghost"})
    assert response.status_code == 400
    assert "Error" in response.get_data(as_text=True)

