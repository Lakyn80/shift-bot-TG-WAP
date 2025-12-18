def test_rules_min_rest_between_shifts(client):
    # employee
    employee = client.post(
        "/users/",
        json={
            "telegram_id": "rest_emp",
            "full_name": "Rest Employee",
            "role": "employee",
        },
    ).json()

    # shift 1 (end 22:00)
    shift1 = client.post(
        "/shifts/",
        json={
            "name": "Evening Shift",
            "date": "2025-12-24",
            "start_time": "14:00:00",
            "end_time": "22:00:00",
            "location": "Office",
            "max_workers": 5,
        },
    ).json()

    # shift 2 (start 06:00 next day › rest only 8h)
    shift2 = client.post(
        "/shifts/",
        json={
            "name": "Morning Shift",
            "date": "2025-12-25",
            "start_time": "06:00:00",
            "end_time": "14:00:00",
            "location": "Office",
            "max_workers": 5,
        },
    ).json()

    # first check-in OK
    r1 = client.post(
        "/attendance/check-in",
        json={
            "user_id": employee["id"],
            "shift_id": shift1["id"],
        },
    )
    assert r1.status_code == 200

    client.post(f"/attendance/check-out/{r1.json()['id']}")

    # second check-in forbidden (min rest 11h not met)
    r2 = client.post(
        "/attendance/check-in",
        json={
            "user_id": employee["id"],
            "shift_id": shift2["id"],
        },
    )
    assert r2.status_code == 409
