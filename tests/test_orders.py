from unittest.mock import patch, MagicMock
from sqlalchemy.exc import NoResultFound
from src.models.Order import Order

@patch("src.controllers.order_controller.get_all_records")
def test_get_orders(mock_get_all, client):
    mock_get_all.return_value = [{"OrderID": 1, "CustomerID": "C001"}]
    response = client.get("/orders")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"OrderID": 1, "CustomerID": "C001"}]
    mock_get_all.assert_called_once()

@patch("src.controllers.order_controller.insert_record")
def test_post_order(mock_insert, client):
    data = {"CustomerID": "C001", "OrderDate": "2023-01-01"}
    response = client.post("/orders", data=data)

    assert response.status_code == 200
    assert "Insert success" in response.get_data(as_text=True)
    mock_insert.assert_called_once_with(data, Order)

@patch("src.controllers.order_controller.db.session")
def test_patch_orders(mock_session, client):
    mock_order = MagicMock()
    mock_session.execute.return_value.scalar_one.return_value = mock_order

    response = client.patch("/orders/1", json={"OrderDate": "2023-01-02"})

    assert response.status_code == 200
    assert "Update success" in response.get_data(as_text=True)
    mock_order.update_vals.assert_called_once_with({"OrderDate": "2023-01-02"})
    mock_session.commit.assert_called_once()

@patch("src.controllers.order_controller.get_all_records")
def test_get_orders_exception(mock_get_all, client):
    mock_get_all.side_effect = Exception("DB error")
    response = client.get("/orders")

    assert response.status_code == 400
    assert "Error : DB error" in response.get_data(as_text=True)

@patch("src.controllers.order_controller.db.session")
def test_patch_order_not_found(mock_session, client):
    mock_session.execute.return_value.scalar_one.side_effect = NoResultFound()
    response = client.patch("/orders/999", json={"OrderDate": "2023-01-03"})

    assert response.status_code == 400
    assert "Error" in response.get_data(as_text=True)