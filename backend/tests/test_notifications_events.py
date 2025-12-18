def test_notification_created_on_shift_creation(client):
    # manager
    manager = client.post(
        "/users/",
        json={
            "telegram_id": "notif_evt_mgr",
            "full_name": "Notif Event Manager",
            "role": "manager",
        },
    ).json()

    # vytvoøení smìny (event)
    client.post(
        "/shifts/",
        json={
            "name": "Notif Shift",
            "date": "2025-12-21",
            "start_time": "08:00:00",
            "end_time": "16:00:00",
            "location": "Office",
            "max_workers": 5,
        },
    )

    # manager si mùže vylistovat notifikace
    r = client.get(
        "/notifications",
        headers={"X-User-Id": str(manager["id"])},
    )
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 1
