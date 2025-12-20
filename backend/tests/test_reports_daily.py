def test_report_daily_hours(client):
    r = client.get("/reports/hours/daily")
    assert r.status_code == 200
    assert "total_hours" in r.json()
