def test_rules_max_hours_per_day(client):
    # manager
    manager = client.post(
        "/users/",
        json={
            "telegram_id": "rule_mgr_day",
            "full_name": "Rule Manager Day",
            "role": "manager",
        },
    ).json()

    # employee
    employee = client.post(
        "/users/",
        json={
            "telegram_id": "rule_emp_day",
            "full_name": "Rule Employee Day",
            "role": "employee",
        },
    ).json()

    # shift 1 (8h)
    shift1 = client.post(
        "/shifts/",
        json={
            "name": "Day Shift 1",
            "date": "2025-12-23",
            "start_time": "08:00:00",
            "end_time": "16:00:00",
            "location": "Office",
            "max_workers": 5,
        },
    ).json()

    # shift 2 (8h same day)
    shift2 = client.post(
        "/shifts/",
        json={
            "name": "Day Shift 2",
            "date": "2025-12-23",
            "start_time": "16:00:00",
            "end_time": "23:59:00",
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

    # second check-in should be forbidden (over daily limit)
    r2 = client.post(
        "/attendance/check-in",
        json={
            "user_id": employee["id"],
            "shift_id": shift2["id"],
        },
    )
    assert r2.status_code == 409
