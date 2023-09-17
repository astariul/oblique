"""CRUD functions to interact with the DB."""
from datetime import datetime
from typing import List, Tuple

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from oblique.database import engine, models


def create_tables():
    """Util function to create the DB tables.

    Warning, this function should be called only if the DB tables aren't
    already created.
    """
    models.Base.metadata.create_all(bind=engine)


def create_package(db: Session, pkg_name: str) -> models.Package:
    """CRUD function to create a new Package.

    Args:
        db (Session): DB Session.
        pkg_name (str): Name of the package to create.

    Returns:
        models.Package: Created Package.
    """
    db_package = models.Package(name=pkg_name, last_updated=func.now())
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    return db_package


def create_release(db: Session, version: str, date: datetime, is_yanked: bool, package_id: int) -> models.Release:
    """CRUD function to create a new Release.

    Args:
        db (Session): DB Session.
        version (str): Version name of this release.
        date (datetime): Release date.
        is_yanked (bool): If this release was yanked (`True`) or not (`False`).
        package_id (int): ID of the package this release is associated with.

    Returns:
        models.Release: Created Release.
    """
    db_release = models.Release(version=version, date=date, is_yanked=is_yanked, package_id=package_id)
    db.add(db_release)
    db.commit()
    db.refresh(db_release)
    return db_release


def create_releases(db: Session, releases_data: List[Tuple[str, datetime, bool]], package_id: int):
    """CRUD function to create several new Releases.

    Args:
        db (Session): DB Session.
        releases_data (List[Tuple[str, datetime, bool]]): List of releases data.
            Each element is a tuple with the version name, the release date,
            and if this release is yanked or not.
        package_id (int): ID of the package this release is associated with.
    """
    for version, date, is_yanked in releases_data:
        create_release(db, version, date, is_yanked, package_id)


def get_package_by_name(db: Session, pkg_name: str) -> models.Package:
    """CRUD function to retrieve a Package from its name.

    Args:
        db (Session): DB Session.
        pkg_name (str): Name of the package to retrieve.

    Returns:
        models.Package: Package with the given name.
    """
    return db.query(models.Package).filter(models.Package.name == pkg_name).first()


def update_package(
    db: Session, db_package: models.Package, releases_data: List[Tuple[str, datetime, bool]]
) -> models.Package:
    """CRUD function to update a Package (changing the `last_updated`
    attribute).

    This will simply update the `last_updated` field, delete all associated
    releases, and recreate them from the given data.

    Args:
        db (Session): DB Session.
        db_package (models.Package): Package to update.
        releases_data (List[Tuple[str, datetime, bool]]): List of releases data.
            Each element is a tuple with the version name, the release date,
            and if this release is yanked or not.

    Returns:
        models.Package: Package updated.
    """
    # Update the element itself
    db_package.last_updated = func.now()
    db.commit()

    # Delete all of its previous releases
    db.query(models.Release).filter(models.Release.package_id == db_package.id).delete()

    # Recreate the releases from the fresh data
    create_releases(db, releases_data, db_package.id)

    db.refresh(db_package)
    return db_package


def get_latest_release_of(db: Session, db_package: models.Package) -> models.Release:
    """CRUD function to retrieve the latest Release of a Package.

    Args:
        db (Session): DB Session.
        db_package (models.Package): Package for which to get the last release
            date.

    Returns:
        models.Release: Latest release for this package.
    """
    return (
        db.query(models.Release)
        .filter(models.Release.package_id == db_package.id)
        .order_by(models.Release.date.desc())
        .first()
    )


def get_n_versions_of(db: Session, db_package: models.Package) -> int:
    """CRUD function to retrieve the number of releases of a Package.

    Args:
        db (Session): DB Session.
        db_package (models.Package): Package for which to get the number of
            versions.

    Returns:
        int: The number of versions for this package.
    """
    return db.query(models.Release).filter(models.Release.package_id == db_package.id).count()


def get_n_versions_yanked_of(db: Session, db_package: models.Package) -> int:
    """CRUD function to retrieve the number of yanked releases of a Package.

    Args:
        db (Session): DB Session.
        db_package (models.Package): Package for which to get the number of
            yanked versions.

    Returns:
        int: The number of yanked versions for this package.
    """
    return (
        db.query(models.Release)
        .filter(models.Release.package_id == db_package.id)
        .filter(models.Release.is_yanked is True)
        .count()
    )
