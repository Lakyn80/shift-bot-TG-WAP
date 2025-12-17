def test_attendance_double_check_in_forbidden(client):
    user = client.post(
        "/users/",
        json={
            "telegram_id": "double1",
            "full_name": "Double Checkin User",
            "role": "employee",
        },
    ).json()

    shift = client.post(
        "/shifts/",
        json={
            "name": "Double Shift",
            "date": "2025-12-17",
            "start_time": "08:00:00",
            "end_time": "16:00:00",
            "location": "Office",
            "max_workers": 5,
        },
    ).json()

    r1 = client.post(
        "/attendance/check-in",
        json={
            "user_id": user["id"],
            "shift_id": shift["id"],
        },
    )
    assert r1.status_code == 200

    r2 = client.post(
        "/attendance/check-in",
        json={
            "user_id": user["id"],
            "shift_id": shift["id"],
        },
    )
    assert r2.status_code == 409
