def test_attendance_double_check_out_forbidden(client):
    # vytvoř user
    user = client.post(
        "/users/",
        json={
            "telegram_id": "double-out",
            "full_name": "Double Checkout User",
            "role": "employee",
        },
    ).json()

    # vytvoř shift
    shift = client.post(
        "/shifts/",
        json={
            "name": "Double Out Shift",
            "date": "2025-12-17",
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
            "user_id": user["id"],
            "shift_id": shift["id"],
        },
    ).json()

    attendance_id = attendance["id"]

    # první check-out
    r1 = client.post(f"/attendance/check-out/{attendance_id}")
    assert r1.status_code == 200

    # druhý check-out musí selhat
    r2 = client.post(f"/attendance/check-out/{attendance_id}")
    assert r2.status_code == 409
