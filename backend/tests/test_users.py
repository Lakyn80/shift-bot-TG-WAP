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
    assert data["role"] == "employee"
