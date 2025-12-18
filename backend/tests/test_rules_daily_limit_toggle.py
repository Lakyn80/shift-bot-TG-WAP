def test_daily_limit_disabled(client, monkeypatch):
    monkeypatch.setenv("ATT_ENABLE_DAILY_LIMIT", "false")
    monkeypatch.setenv("ATT_ENABLE_MIN_REST", "false")
    monkeypatch.setenv("ATT_ENABLE_WEEKLY_LIMIT", "true")
    monkeypatch.setenv("ATT_ENABLE_OVERLAP_CHECK", "true")

    employee = client.post("/users/", json={
        "telegram_id": "emp_daily_off",
        "full_name": "Employee Daily Off",
        "role": "employee",
    }).json()

    shift1 = client.post("/shifts/", json={
        "name": "Shift 1",
        "date": "2025-12-23",
        "start_time": "08:00:00",
        "end_time": "16:00:00",
        "location": "Office",
        "max_workers": 5,
    }).json()

    shift2 = client.post("/shifts/", json={
        "name": "Shift 2",
        "date": "2025-12-23",
        "start_time": "16:00:00",
        "end_time": "23:59:00",
        "location": "Office",
        "max_workers": 5,
    }).json()

    r1 = client.post("/attendance/check-in", json={
        "user_id": employee["id"],
        "shift_id": shift1["id"],
    })
    assert r1.status_code == 200

    client.post(f"/attendance/check-out/{r1.json()['id']}")

    r2 = client.post("/attendance/check-in", json={
        "user_id": employee["id"],
        "shift_id": shift2["id"],
    })

    assert r2.status_code == 200
