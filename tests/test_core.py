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


@pytest.fixture
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
