def test_home_route(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "<head>" in r.text and "<body>" in r.text


def test_favion(client):
    r = client.get("/favicon.ico")
    assert r.status_code == 200


def test_unknown_route(client):
    r = client.get("/wtf")
    assert r.status_code == 404
    assert "Error" in r.text and "404" in r.text


def test_search_basic(client, db):
    pkg = "transformers_app_1"
    r = client.get(f"/search?pkg={pkg}", headers={"hx-request": "true"})

    assert r.status_code == 200
    assert pkg in r.text
    assert "09 Aug 2021" in r.text and "Last release" in r.text
    assert "3" in r.text and "Versions released" in r.text
    assert "1" in r.text and "Versions yanked" in r.text


def test_search_unknown(client, db):
    pkg = "unknown_app_1"
    r = client.get(f"/search?pkg={pkg}", headers={"hx-request": "true"})

    assert r.status_code == 200
    assert pkg in r.text and "does not exist" in r.text


def test_search_no_args(client, db):
    r = client.get("/search", headers={"hx-request": "true"})

    assert r.status_code == 422


def test_search_not_htmx(client, db):
    # Without the right headers, this route should return a 404
    pkg = "transformers_app_2"
    r = client.get(f"/search?pkg={pkg}")

    assert r.status_code == 404
