def test_attendance_check_in_and_out(client):
    # vytvoř user
    user = client.post(
        "/users/",
        json={
            "telegram_id": "999",
            "full_name": "Attendance Tester",
            "role": "employee",
        },
    ).json()

    # vytvoř shift
    shift = client.post(
        "/shifts/",
        json={
            "name": "Test Shift",
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
    )
    assert attendance.status_code == 200
    data = attendance.json()
    assert data["check_in"] is not None
    assert data["check_out"] is None

    # check-out
    checkout = client.post(
        f"/attendance/check-out/{data['id']}"
    )
    assert checkout.status_code == 200
    assert checkout.json()["check_out"] is not None


def test_attendance_double_check_in_fails(client):
    # vytvoř user
    user = client.post(
        "/users/",
        json={
            "telegram_id": "888",
            "full_name": "Double Check Tester",
            "role": "employee",
        },
    ).json()

    # vytvoř shift
    shift = client.post(
        "/shifts/",
        json={
            "name": "Double Shift",
            "date": "2025-12-18",
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "location": "Office",
            "max_workers": 5,
        },
    ).json()

    # první check-in → OK
    first = client.post(
        "/attendance/check-in",
        json={
            "user_id": user["id"],
            "shift_id": shift["id"],
        },
    )
    assert first.status_code == 200

    # druhý check-in na stejný shift → FAIL
    second = client.post(
        "/attendance/check-in",
        json={
            "user_id": user["id"],
            "shift_id": shift["id"],
        },
    )
    assert second.status_code == 409


def test_attendance_check_out_without_check_in_fails(client):
    # pokus o check-out neexistující attendance
    response = client.post("/attendance/check-out/99999")
    assert response.status_code == 409
