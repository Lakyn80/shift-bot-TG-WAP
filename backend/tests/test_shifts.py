def test_create_shift(client):
    response = client.post(
        "/shifts/",
        json={
            "name": "Morning",
            "start_time": "08:00",
            "end_time": "16:00",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Morning"


def test_list_shifts(client):
    response = client.get("/shifts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
