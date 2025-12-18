def test_attendance_export_csv_only_manager_allowed(client):
    # employee
    employee = client.post(
        "/users/",
        json={
            "telegram_id": "exp_emp",
            "full_name": "Export Employee",
            "role": "employee",
        },
    ).json()

    # manager
    manager = client.post(
        "/users/",
        json={
            "telegram_id": "exp_mgr",
            "full_name": "Export Manager",
            "role": "manager",
        },
    ).json()

    # employee nesmí exportovat
    r_employee = client.get(
        "/attendance/export/csv",
        headers={"X-User-Id": str(employee["id"])},
    )
    assert r_employee.status_code == 403

    # manager smí exportovat
    r_manager = client.get(
        "/attendance/export/csv",
        headers={"X-User-Id": str(manager["id"])},
    )
    assert r_manager.status_code == 200
    assert r_manager.headers["content-type"].startswith("text/csv")
    assert r_manager.text.strip() != ""
