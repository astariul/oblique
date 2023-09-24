from dateutil.parser import isoparse

from oblique.database import crud


def test_pkg_infos_basic(client, db):
    db_pkg = crud.create_package(db, "transformers#api_1")
    crud.create_releases(db, [("v0.0.1", isoparse("2002-07-25T11:27:16"), False)], db_pkg.id)

    r = client.post("/api/pkg_infos", json={"pkg_name": "transformers#api_1"})

    assert r.status_code == 200
    data = r.json()
    assert data["last_release"] == "2002-07-25T11:27:16"
    assert data["n_versions"] == 1
    assert data["n_versions_yanked"] == 0


def test_pkg_infos_force_refresh(client, db):
    db_pkg = crud.create_package(db, "transformers#api_2")
    crud.create_releases(db, [("v0.0.1", isoparse("2002-07-25T11:27:16"), False)], db_pkg.id)

    r = client.post("/api/pkg_infos", json={"pkg_name": "transformers#api_2", "force_refresh": True})

    assert r.status_code == 200
    data = r.json()
    assert data["last_release"] == "2021-08-09T14:27:16"
    assert data["n_versions"] == 3
    assert data["n_versions_yanked"] == 1


def test_pkg_infos_unknown_package(client, db):
    r = client.post("/api/pkg_infos", json={"pkg_name": "unknown#api"})

    assert r.status_code == 404
