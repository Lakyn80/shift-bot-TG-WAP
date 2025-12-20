def test_report_daily_hours_user_filter(client):
    u1 = client.post("/users/", json={
        "telegram_id": "rep_u1",
        "full_name": "Report User 1",
        "role": "employee",
    }).json()

    u2 = client.post("/users/", json={
        "telegram_id": "rep_u2",
        "full_name": "Report User 2",
        "role": "employee",
    }).json()

    s = client.post("/shifts/", json={
        "name": "Report Shift",
        "date": "2025-12-20",
        "start_time": "08:00:00",
        "end_time": "16:00:00",
        "location": "Office",
    }).json()

    r1 = client.post("/attendance/check-in", json={
        "user_id": u1["id"],
        "shift_id": s["id"],
    })
    client.post(f"/attendance/check-out/{r1.json()['id']}")

    r2 = client.post("/attendance/check-in", json={
        "user_id": u2["id"],
        "shift_id": s["id"],
    })
    client.post(f"/attendance/check-out/{r2.json()['id']}")

    r = client.get(f"/reports/hours/daily?user_id={u1['id']}")
    assert r.status_code == 200
    assert r.json()["total_hours"] > 0
