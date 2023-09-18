"""File containing the routes of the API."""
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from oblique import __version__
from oblique.core import UnknownPackageException, get_package_info
from oblique.dependencies import get_db


app = FastAPI(title="Oblique API", version=__version__, redoc_url=None)


class PackageParameters(BaseModel):
    """Parameters to pass to identify a package."""

    pkg_name: str


@app.post("/pkg_infos")
def get_pkg_infos(parameters: PackageParameters, db: Session = Depends(get_db)):
    """Route to get the informations of the package requested.

    These informations are :
     * Last release date
     * Number of versions released
     * Number of versions yanked
    """
    try:
        last_release, n_versions, n_versions_yanked = get_package_info(db, parameters.pkg_name)
        return {
            "last_release": last_release,
            "n_versions": n_versions,
            "n_versions_yanked": n_versions_yanked,
        }
    except UnknownPackageException:
        raise HTTPException(status_code=404, detail="This package was not published to PyPi index.")
