from datetime import datetime, timedelta

import pytest
from dateutil.parser import isoparse

import oblique
from oblique import core
from oblique.database import crud

from . import mock_pypi_api  # noqa: F401 (just importing it will monkey-patch requests.get to mimic PyPi API !)


def test_package_has_version():
    assert len(oblique.__version__) > 0


def test_request_pypi_api_valid_package():
    data = core.get_package_info_from_pypi("transformers")

    assert len(data) == 3
    assert ("v1.2.10", isoparse("2021-08-09T14:27:16"), False) in data
    assert ("v1.1.0", isoparse("2021-06-09T14:27:16"), True) in data
    assert ("v0.2.0", isoparse("2021-05-09T14:27:16"), False) in data


def test_request_pypi_api_nonexisting_package():
    data = core.get_package_info_from_pypi("lisduyfg")

    assert len(data) == 0


def test_request_pypi_api_unknown_status_code():
    with pytest.raises(core.PyPiAPIException):
        core.get_package_info_from_pypi("redirected")


@pytest.fixture(scope="session")
def pkg_release_2022(db):
    db_pkg = crud.create_package(db, "pkg_release_2022")

    releases = [
        ("v1.2.10", isoparse("2022-08-09T14:27:16"), False),
        ("v1.1.1", isoparse("2021-06-09T14:27:16"), True),
        ("v1.1.0", isoparse("2021-05-09T14:27:16"), True),
        ("v0.2.0", isoparse("2020-05-09T14:27:16"), False),
        ("v0.1.0", isoparse("2020-04-09T14:27:16"), False),
        ("v0.0.4", isoparse("2020-04-10T14:27:16"), False),
    ]
    crud.create_releases(db, releases, db_pkg.id)

    yield db_pkg


def test_get_stats_basic(db, pkg_release_2022):
    last_release, n_versions, n_versions_yanked = core.get_stats_for(db, pkg_release_2022)

    assert last_release == "09 Aug 2022"
    assert n_versions == 6
    assert n_versions_yanked == 2


def test_get_stats_non_human_readable(db, pkg_release_2022):
    last_release, n_versions, n_versions_yanked = core.get_stats_for(db, pkg_release_2022, human_readable=False)

    assert last_release == isoparse("2022-08-09T14:27:16")
    assert n_versions == 6
    assert n_versions_yanked == 2


@pytest.fixture(scope="session")
def pkg_no_release(db):
    yield crud.create_package(db, "pkg_no_release")


def test_get_stats_no_release(db, pkg_no_release):
    with pytest.raises(core.UnknownPackageException):
        core.get_stats_for(db, pkg_no_release)


@pytest.fixture(scope="session")
def pkg_release_16d_ago(db):
    db_pkg = crud.create_package(db, "pkg_release_16d_ago")

    releases = [
        ("v1.34.10", datetime.utcnow() - timedelta(days=16), False),
    ]
    crud.create_releases(db, releases, db_pkg.id)

    yield db_pkg


def test_get_stats_format_x_days_ago(db, pkg_release_16d_ago):
    last_release, n_versions, n_versions_yanked = core.get_stats_for(db, pkg_release_16d_ago)

    assert last_release == "16 days ago"
    assert n_versions == 1
    assert n_versions_yanked == 0


@pytest.fixture(scope="session")
def pkg_release_1d_ago(db):
    db_pkg = crud.create_package(db, "pkg_release_1d_ago")

    releases = [
        ("v3.3.0", datetime.utcnow() - timedelta(days=1), False),
    ]
    crud.create_releases(db, releases, db_pkg.id)

    yield db_pkg


def test_get_stats_format_1_day_ago(db, pkg_release_1d_ago):
    last_release, n_versions, n_versions_yanked = core.get_stats_for(db, pkg_release_1d_ago)

    assert last_release == "1 day ago"
    assert n_versions == 1
    assert n_versions_yanked == 0


@pytest.fixture(scope="session")
def pkg_release_8h_ago(db):
    db_pkg = crud.create_package(db, "pkg_release_8h_ago")

    releases = [
        ("v0.3.3", datetime.utcnow() - timedelta(hours=8), False),
    ]
    crud.create_releases(db, releases, db_pkg.id)

    yield db_pkg


def test_get_stats_format_x_hours_ago(db, pkg_release_8h_ago):
    last_release, n_versions, n_versions_yanked = core.get_stats_for(db, pkg_release_8h_ago)

    assert last_release == "8h ago"
    assert n_versions == 1
    assert n_versions_yanked == 0
