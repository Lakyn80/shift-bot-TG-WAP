def test_notifications_only_manager_can_list(client):
    # employee
    employee = client.post(
        "/users/",
        json={
            "telegram_id": "notif_emp",
            "full_name": "Notif Employee",
            "role": "employee",
        },
    ).json()

    # manager
    manager = client.post(
        "/users/",
        json={
            "telegram_id": "notif_mgr",
            "full_name": "Notif Manager",
            "role": "manager",
        },
    ).json()

    # employee nesmí
    r_emp = client.get(
        "/notifications",
        headers={"X-User-Id": str(employee["id"])},
    )
    assert r_emp.status_code == 403

    # manager smí
    r_mgr = client.get(
        "/notifications",
        headers={"X-User-Id": str(manager["id"])},
    )
    assert r_mgr.status_code == 200
    assert isinstance(r_mgr.json(), list)
