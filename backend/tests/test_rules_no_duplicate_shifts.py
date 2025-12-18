def test_rules_no_duplicate_shifts_for_user(client):
    # employee
    employee = client.post(
        "/users/",
        json={
            "telegram_id": "rule_emp",
            "full_name": "Rule Employee",
            "role": "employee",
        },
    ).json()

    # shift
    shift = client.post(
        "/shifts/",
        json={
            "name": "Rule Shift",
            "date": "2025-12-22",
            "start_time": "08:00:00",
            "end_time": "16:00:00",
            "location": "Office",
            "max_workers": 5,
        },
    ).json()

    # first check-in OK
    r1 = client.post(
        "/attendance/check-in",
        json={
            "user_id": employee["id"],
            "shift_id": shift["id"],
        },
    )
    assert r1.status_code == 200

    # duplicate check-in forbidden
    r2 = client.post(
        "/attendance/check-in",
        json={
            "user_id": employee["id"],
            "shift_id": shift["id"],
        },
    )
    assert r2.status_code == 409
