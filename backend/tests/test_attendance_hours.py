def test_attendance_hours_daily_and_monthly_manager_only(client):
    # manager
    manager = client.post(
        "/users/",
        json={
            "telegram_id": "hrs_mgr",
            "full_name": "Hours Manager",
            "role": "manager",
        },
    ).json()

    # employee
    employee = client.post(
        "/users/",
        json={
            "telegram_id": "hrs_emp",
            "full_name": "Hours Employee",
            "role": "employee",
        },
    ).json()

    # shift
    shift = client.post(
        "/shifts/",
        json={
            "name": "Hours Shift",
            "date": "2025-12-20",
            "start_time": "08:00:00",
            "end_time": "16:00:00",
            "location": "Office",
            "max_workers": 5,
        },
    ).json()

    # check-in
    attendance = client.post(
        "/attendance/check-in",
        json={
            "user_id": employee["id"],
            "shift_id": shift["id"],
        },
    ).json()

    # check-out
    client.post(f"/attendance/check-out/{attendance['id']}")

    # employee nesmí
    r_emp = client.get(
        "/attendance/hours/daily",
        headers={"X-User-Id": str(employee["id"])},
    )
    assert r_emp.status_code == 403

    # manager denní
    r_day = client.get(
        "/attendance/hours/daily",
        headers={"X-User-Id": str(manager["id"])},
    )
    assert r_day.status_code == 200
    assert "total_hours" in r_day.json()

    # manager mìsíèní
    r_month = client.get(
        "/attendance/hours/monthly",
        headers={"X-User-Id": str(manager["id"])},
    )
    assert r_month.status_code == 200
    assert "total_hours" in r_month.json()
