def test_attendance_max_workers_limit(client):
    # user 1
    u1 = client.post("/users/", json={
        "telegram_id": "mw1",
        "full_name": "MW User 1",
        "role": "employee",
    }).json()

    # user 2
    u2 = client.post("/users/", json={
        "telegram_id": "mw2",
        "full_name": "MW User 2",
        "role": "employee",
    }).json()

    # shift s kapacitou 1
    shift = client.post("/shifts/", json={
        "name": "Limited Shift",
        "date": "2025-12-18",
        "start_time": "08:00:00",
        "end_time": "16:00:00",
        "location": "Office",
        "max_workers": 1,
    }).json()

    # první check-in OK
    r1 = client.post("/attendance/check-in", json={
        "user_id": u1["id"],
        "shift_id": shift["id"],
    })
    assert r1.status_code == 200

    # druhý check-in musí selhat (409)
    r2 = client.post("/attendance/check-in", json={
        "user_id": u2["id"],
        "shift_id": shift["id"],
    })
    assert r2.status_code == 409
