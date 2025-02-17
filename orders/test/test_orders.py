from fastapi.testclient import TestClient
from main import app
from databases.database import data
from fastapi.security import OAuth2PasswordRequestForm
client = TestClient(app)


def test_add_to_cart():
    response = client.post(
        "/orders/cart", json={"id": 1, "name": "Test Item", "price": 10.0, "quantity": 2, "category": "Electronics"}
    )
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Test Item",
                                "price": 10.0, "quantity": 2, "category": "Electronics"}]


def test_view_cart():
    client.post(
        "/orders/cart", json={"id": 2, "name": "Another Item", "price": 20.0, "quantity": 1, "category": "Electronics"}
    )
    response = client.get("/orders/cart/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    response = client.delete("/orders/cart/clear")
    assert response.status_code == 200
    assert response.json()["message"] == "Cart cleared"


def test_checkout_no_discount():
    client.post(
        "orders/cart", json={"id": 3, "name": "Item 3", "price": 5.0, "quantity": 3, "category": "Electronics"}
    )
    response = client.post("orders/checkout")
    assert response.status_code == 200
    assert response.json()["total_after_discount"] == 15.0
    assert response.json()["discount_amount"] == 0.0
    assert response.json()["applied_discount"] is None


def test_checkout_with_discount():
    data.discount_codes["TEST_DISCOUNT"] = 0.1
    client.post(
        "orders/cart", json={"id": 4, "name": "Item 4", "price": 100.0, "quantity": 1, "category": "Electronics"}
    )
    response = client.post("orders/checkout", json={"code": "TEST_DISCOUNT"})
    assert response.status_code == 200
    assert response.json()["total_after_discount"] == 90.0
    assert response.json()["discount_amount"] == 10.0
    assert response.json()["applied_discount"] == "TEST_DISCOUNT"


def test_checkout_invalid_discount():
    response = client.post("orders/checkout", json={"code": "INVALID_CODE"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid discount code"


def test_admin_generate_discount_code():
    data.nth_order = 5
    response = client.get("/orders/discount_code?order_number=5")
    assert response.status_code == 200
    assert response.json() is not None
    assert "code" in response.json()
    response2 = client.get("/orders/discount_code?order_number=6")
    assert response2.status_code == 200
    assert "code" in response.json()


def test_admin_stats():
    # create some orders for the test.
    client.post("/orders/cart", json={"id": 6, "name": "Item 6",
                "price": 25.0, "quantity": 4, "category": "Electronics"})
    client.post("/orders/checkout", json={"code": "TEST_DISCOUNT"})
    form_data = {"username": "Admin", "password": "admin"}
    response = client.post("/users/login", data=form_data)
    login_data = response.json()
    access_token = login_data["access_token"]
    headers = {"authorization": f"bearer {access_token}"}
    response = client.get("/orders/stats", headers=headers)
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_items_purchased"] == 8
    assert stats["total_purchase_amount"] == 195.0
    assert "TEST_DISCOUNT" in stats["discount_codes"]
    assert stats["total_discount_amount"] == 20.0


def test_clear_cart():
    client.post("/orders/cart", json={"id": 7, "name": "Item 7",
                "price": 1.0, "quantity": 1, "category": "Electronics"})
    response = client.delete("/orders/cart/clear")
    assert response.status_code == 200
    assert response.json()["message"] == "Cart cleared"
    response2 = client.get("/orders/cart")
    assert len(response2.json()) == 0
