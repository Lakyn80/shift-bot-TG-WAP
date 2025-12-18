def test_rules_max_hours_per_week(client):
    # employee
    employee = client.post(
        "/users/",
        json={
            "telegram_id": "rule_emp_week",
            "full_name": "Rule Employee Week",
            "role": "employee",
        },
    ).json()

    # 6 shifts × 8h = 48h (OK)
    for day in range(1, 7):
        shift = client.post(
            "/shifts/",
            json={
                "name": f"Week Shift {day}",
                "date": f"2025-12-{day:02d}",
                "start_time": "08:00:00",
                "end_time": "16:00:00",
                "location": "Office",
                "max_workers": 5,
            },
        ).json()

        r = client.post(
            "/attendance/check-in",
            json={
                "user_id": employee["id"],
                "shift_id": shift["id"],
            },
        )
        assert r.status_code == 200
        client.post(f"/attendance/check-out/{r.json()['id']}")

    # 7th shift › forbidden (over 48h/week)
    shift7 = client.post(
        "/shifts/",
        json={
            "name": "Week Shift 7",
            "date": "2025-12-07",
            "start_time": "08:00:00",
            "end_time": "16:00:00",
            "location": "Office",
            "max_workers": 5,
        },
    ).json()

    r7 = client.post(
        "/attendance/check-in",
        json={
            "user_id": employee["id"],
            "shift_id": shift7["id"],
        },
    )
    assert r7.status_code == 409
