def test_rules_no_overlapping_shifts(client):
    # employee
    employee = client.post(
        "/users/",
        json={
            "telegram_id": "overlap_emp",
            "full_name": "Overlap Employee",
            "role": "employee",
        },
    ).json()

    # shift 1 (08:00–16:00)
    shift1 = client.post(
        "/shifts/",
        json={
            "name": "Overlap Shift 1",
            "date": "2025-12-26",
            "start_time": "08:00:00",
            "end_time": "16:00:00",
            "location": "Office",
            "max_workers": 5,
        },
    ).json()

    # shift 2 overlaps (15:00–23:00)
    shift2 = client.post(
        "/shifts/",
        json={
            "name": "Overlap Shift 2",
            "date": "2025-12-26",
            "start_time": "15:00:00",
            "end_time": "23:00:00",
            "location": "Office",
            "max_workers": 5,
        },
    ).json()

    # first OK
    r1 = client.post(
        "/attendance/check-in",
        json={
            "user_id": employee["id"],
            "shift_id": shift1["id"],
        },
    )
    assert r1.status_code == 200

    client.post(f"/attendance/check-out/{r1.json()['id']}")

    # second forbidden (overlap)
    r2 = client.post(
        "/attendance/check-in",
        json={
            "user_id": employee["id"],
            "shift_id": shift2["id"],
        },
    )
    assert r2.status_code == 409
