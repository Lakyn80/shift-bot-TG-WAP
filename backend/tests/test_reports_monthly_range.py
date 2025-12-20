def test_report_monthly_with_date_range(client):
    u = client.post("/users/", json={
        "telegram_id": "rep_month",
        "full_name": "Monthly Report",
        "role": "employee",
    }).json()

    s = client.post("/shifts/", json={
        "name": "Monthly Shift",
        "date": "2025-11-15",
        "start_time": "08:00:00",
        "end_time": "12:00:00",
        "location": "Office",
    }).json()

    r = client.post("/attendance/check-in", json={
        "user_id": u["id"],
        "shift_id": s["id"],
    })
    client.post(f"/attendance/check-out/{r.json()['id']}")

    res = client.get(
        "/reports/hours/monthly"
        "?user_id={uid}&from_date=2025-11-01T00:00:00"
        "&to_date=2025-11-30T23:59:59".format(uid=u["id"])
    )

    assert res.status_code == 200
    assert res.json()["total_hours"] > 0
