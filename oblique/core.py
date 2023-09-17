"""File containing all the business logic, to be used by the API and the web-app."""
from datetime import datetime, timedelta
from typing import List, Tuple

import requests
from dateutil.parser import isoparse
from sqlalchemy.orm import Session

from oblique.database import crud, models


CACHE_TTL = timedelta(hours=24)


class PyPiAPIException(Exception):
    """Exception raised when the PyPi API doesn't respond or respond with an
    unhandled HTTP code.
    """

    pass


class UnknownPackageException(Exception):
    """Exception raised when the given package name is not a package registered
    in PyPi index.
    """

    pass


def get_package_info_from_pypi(pkg_name: str) -> List[Tuple[str, datetime, bool]]:
    """Function that call the PyPi API and retrieve the releases data for a
    specific package name.

    Args:
        pkg_name (str): The package name for which we want to retrieve the data.

    Raises:
        PyPiAPIException: Exception raised if the PyPi API behaves unexpectedly.

    Returns:
        List[Tuple[str, datetime, bool]]: Releases data for this package. It's
            a list, where each element represents a single release, which is a
            tuple with :
            * The version of the release
            * The release date
            * If this release was yanked (`True`) or not (`False`)
            Note that if this list is empty, it means the package does not
            exists in PyPi.
    """
    r = requests.get(f"https://pypi.org/pypi/{pkg_name}/json")

    if r.status_code == 200:
        data = r.json()

        # Extract the data we need from the response
        return [
            (version, isoparse(info["upload_time"]), info["yanked"])
            for version, (info, *_) in data["releases"].items()
        ]
    elif r.status_code == 404:
        # Non-existing package : just return an empty list of releases
        return []
    else:
        raise PyPiAPIException("PyPi API unreachable")


def get_stats_for(db: Session, db_package: models.Package) -> Tuple[str, int, int]:
    """Function that retrieve the statistics of a package stored in the DB.

    Args:
        db (Session): DB Session.
        db_package (models.Package): The DB object corresponding to the package
            we want to extract statistics from.

    Raises:
        UnknownPackageException: Exception raised if the package is not a
            package registered in PyPi index (has no releases).

    Returns:
        Tuple[str, int, int]: The statistics for this package. This is a tuple
            with :
            * The release date in a human-readable format
            * The number of versions released
            * The number of versions yanked
    """
    # From the DB, get our statistics
    last_release = crud.get_latest_release_of(db, db_package)
    n_versions = crud.get_n_versions_of(db, db_package)
    n_versions_yanked = crud.get_n_versions_yanked_of(db, db_package)

    # Handle the case where this package name wasn't released)
    if last_release is None:
        raise UnknownPackageException()

    # Format the last_release to be human-friendly
    td = datetime.utcnow() - last_release.date
    if td < timedelta(hours=24):
        h = max(td.seconds // 3600, 1)
        last_release = f"{h}h ago"
    elif td < timedelta(days=30):
        last_release = f"{td.days} day{'s' if td.days > 1 else ''} ago"
    else:
        last_release = f"{last_release.date:%d %b %Y}"

    return last_release, n_versions, n_versions_yanked


def get_package_info(db: Session, pkg_name: str) -> Tuple[str, int, int]:
    """Main function to retrieve informations about a PyPi package.

    This function will first check if the informations is cached locally. If
    it's not cached locally, the data is retrieved from the PyPi API and cached
    locally.
    The cache is valid for 24h.

    Args:
        db (Session): DB Session.
        pkg_name (str): Name of the package for which we want data.

    Returns:
        Tuple[str, int, int]: The statistics for the package. This is a tuple
            with :
            * The release date in a human-readable format
            * The number of versions released
            * The number of versions yanked
    """
    # Check the database to see if we already have that package's infos locally cached
    db_package = crud.get_package_by_name(db, pkg_name)

    if db_package is None or db_package.last_updated < datetime.now() - CACHE_TTL:
        # This package is not cached locally, or the cache is stale
        # Call the PyPi API to retrieve its informations and update our local cache
        releases = get_package_info_from_pypi(pkg_name)

        if db_package is not None:
            db_package = crud.update_package(db, db_package, releases)
        else:
            db_package = crud.create_package(db, pkg_name)
            crud.create_releases(db, releases, db_package.id)

    # Retrieve the numbers we are interested in
    return get_stats_for(db, db_package)
