"""Main file, containing the FastAPI app definition and where the routes are declared."""
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from jinjax import Catalog
from sqlalchemy.orm import Session

from oblique import ASSETS_DIR, COMPONENTS_DIR, __version__, config
from oblique.core import UnknownPackageException, get_package_info
from oblique.database import SessionLocal, crud


app = FastAPI(title="Oblique", version=__version__, redoc_url=None)

catalog = Catalog()
catalog.add_folder(COMPONENTS_DIR)


def get_db() -> SessionLocal:
    """FastAPI dependency to create a DB Session.

    Yields:
        SessionLocal: DB Session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.exception_handler(HTTPException)
async def browser_exception_handler(request, exc):
    """Define the exception handler for HTML exceptions."""
    return HTMLResponse(
        status_code=exc.status_code, content=catalog.render("Error", status_code=exc.status_code, error_msg=exc.detail)
    )


@app.get("/", response_class=HTMLResponse)
async def home():
    """Main route, sending the home page."""
    return catalog.render("HomePage")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Favicon."""
    return FileResponse(ASSETS_DIR / "logo.svg")


@app.get("/search", response_class=HTMLResponse)
async def search(pkg: str, db: Session = Depends(get_db)):
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


@app.route("/{full_path:path}")
async def unknown_path(request: Request):
    """Catch-all route, if the user tries to access an unknown page, we display
    a 404.
    """
    raise HTTPException(status_code=404, detail="Sorry, we couldn't find this page.")


def serve():
    """The function called to run the server.

    It will simply run the FastAPI app. Also, if the selected DB is in-memory,
    it will ensure the tables are created.
    """
    if config.db == "memory":
        crud.create_tables()

    uvicorn.run(app, host=config.host, port=config.port)
