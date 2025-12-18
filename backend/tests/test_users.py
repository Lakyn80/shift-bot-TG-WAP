def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "full_name": "Test User",
            "role": "employee",
            "telegram_id": "123",
            "whatsapp_id": None,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Test User"
    assert data["is_active"] is True


def test_create_user_inactive(client):
    response = client.post(
        "/users/",
        json={
            "full_name": "Inactive User",
            "role": "employee",
            "telegram_id": "999_inactive",
            "whatsapp_id": None,
            "is_active": False,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] is False
