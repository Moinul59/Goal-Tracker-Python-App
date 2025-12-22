def test_app_running(client):
    res = client.get("/")
    assert res.status_code in (200, 302)