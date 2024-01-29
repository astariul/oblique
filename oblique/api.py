"""File containing the routes of the API."""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from pydantic import BaseModel
from sqlalchemy.orm import Session

from oblique.core import UnknownPackageException, get_package_info
from oblique.dependencies import get_db


router = APIRouter()


class APIException(HTTPException):
    """Exception raised by the API.

    Args:
        status_code (int): HTTP code to return.
        detail (str, optional): Error description. Defaults to `None`.
    """

    pass


async def api_exception_handler(request: Request, exc: HTTPException):
    """Define the exception handler for APIException."""
    return await http_exception_handler(request, exc)


handler = (APIException, api_exception_handler)


class PackageParameters(BaseModel):
    """Parameters to pass to identify a package.

    * pkg_name (str): Name of the package to get.
    * force_refresh (bool, optional): If set to `True`, the local cache is
        ignored and the PyPi API is called. Note that it might be slower.
        Defaults to `False`.
    """

    pkg_name: str
    force_refresh: bool = False


@router.post("/pkg_infos")
def get_pkg_infos(parameters: PackageParameters, db: Session = Depends(get_db)):
    """Route to get the informations of the package requested.

    These informations are :
     * Last release date
     * Number of versions released
     * Number of versions yanked
    """
    try:
        last_release, n_versions, n_versions_yanked = get_package_info(
            db, parameters.pkg_name, human_readable=False, force_refresh=parameters.force_refresh
        )
        return {
            "last_release": last_release,
            "n_versions": n_versions,
            "n_versions_yanked": n_versions_yanked,
        }
    except UnknownPackageException:
        raise APIException(status_code=404, detail="This package was not published to PyPi index.")
