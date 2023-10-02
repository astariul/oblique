"""Main file, containing the FastAPI web-app definition and its routes."""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from jinjax import Catalog
from sqlalchemy.orm import Session

from oblique import ASSETS_DIR, COMPONENTS_DIR
from oblique.core import UnknownPackageException, get_package_info
from oblique.dependencies import get_db


router = APIRouter()

catalog = Catalog()
catalog.add_folder(COMPONENTS_DIR)


class HTMLException(HTTPException):
    """Exception raised by the web-app.

    Args:
        status_code (int): HTTP code to return.
        detail (str, optional): Error description. Defaults to `None`.
    """

    pass


async def html_exception_handler(request: Request, exc: HTTPException):
    """Define the exception handler for HTMLException."""
    return HTMLResponse(
        status_code=exc.status_code, content=catalog.render("Error", status_code=exc.status_code, error_msg=exc.detail)
    )


handler = (HTMLException, html_exception_handler)


async def htmx(request: Request):
    """Dependency, to make sure the received request is a HTMX request.
    If it's not a HTMX request, a 404 is returned.

    Args:
        request (Request): Request to check.
    """
    if "hx-request" not in request.headers or request.headers["hx-request"] != "true":
        raise HTMLException(status_code=404, detail="Sorry, we couldn't find this page.")


@router.get("/", response_class=HTMLResponse)
async def home():
    """Main route, sending the home page."""
    return catalog.render("HomePage")


@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Favicon."""
    return FileResponse(ASSETS_DIR / "logo.svg")


@router.get("/tailwind.css", include_in_schema=False)
async def tailwind():
    """TailwindCSS."""
    return FileResponse(ASSETS_DIR / "tailwind.css")


@router.get("/search", response_class=HTMLResponse)
async def search(pkg: str, db: Session = Depends(get_db), h: None = Depends(htmx)):
    """Search route, to display the search results."""
    try:
        last_release, n_versions, n_versions_yanked = get_package_info(db, pkg)
        return catalog.render(
            "SearchResult",
            pkg_name=pkg,
            last_release=last_release,
            n_versions=n_versions,
            n_versions_yanked=n_versions_yanked,
        )
    except UnknownPackageException:
        return catalog.render("UnknownPackage", pkg_name=pkg)


@router.route("/{full_path:path}")
async def unknown_path(request: Request):
    """Catch-all route, if the user tries to access an unknown page, we display
    a 404.
    """
    raise HTMLException(status_code=404, detail="Sorry, we couldn't find this page.")
