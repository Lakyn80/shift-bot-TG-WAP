from datetime import datetime, timedelta


def test_attendance_manual_edit_only_manager_allowed(client):
    # vytvoøení employee
    employee = client.post(
        "/users/",
        json={
            "telegram_id": "emp1",
            "full_name": "Employee One",
            "role": "employee",
        },
    ).json()

    # vytvoøení managera
    manager = client.post(
        "/users/",
        json={
            "telegram_id": "mgr1",
            "full_name": "Manager One",
            "role": "manager",
        },
    ).json()

    # vytvoøení smìny
    shift = client.post(
        "/shifts/",
        json={
            "name": "Edit Shift",
            "date": "2025-12-19",
            "start_time": "08:00:00",
            "end_time": "16:00:00",
            "location": "Office",
            "max_workers": 5,
        },
    ).json()

    # employee check-in
    attendance = client.post(
        "/attendance/check-in",
        json={
            "user_id": employee["id"],
            "shift_id": shift["id"],
        },
    ).json()

    new_check_in = (datetime.utcnow() - timedelta(hours=1)).isoformat()
    new_check_out = datetime.utcnow().isoformat()

    # pokus employee o editaci › FORBIDDEN
    r_employee = client.patch(
        f"/attendance/{attendance['id']}",
        json={
            "check_in": new_check_in,
            "check_out": new_check_out,
        },
        headers={
            "X-User-Id": str(employee["id"])
        },
    )
    assert r_employee.status_code == 403

    # pokus managera › OK
    r_manager = client.patch(
        f"/attendance/{attendance['id']}",
        json={
            "check_in": new_check_in,
            "check_out": new_check_out,
        },
        headers={
            "X-User-Id": str(manager["id"])
        },
    )
    assert r_manager.status_code == 200
    data = r_manager.json()
    assert data["check_in"] is not None
    assert data["check_out"] is not None
