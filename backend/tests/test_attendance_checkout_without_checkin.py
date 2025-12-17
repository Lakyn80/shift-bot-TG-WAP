def test_attendance_check_out_without_check_in(client):
    # pokus o check-out neexistující attendance
    r = client.post("/attendance/check-out/9999")
    assert r.status_code == 409
