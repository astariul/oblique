"""Main file, containing the FastAPI app definition and where the routes are declared."""
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from jinjax import Catalog
from sqlalchemy.orm import Session

from oblique import COMPONENTS_DIR, __version__, config
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


@app.get("/", response_class=HTMLResponse)
async def home():
    """Main route, sending the home page."""
    return catalog.render("HomePage")


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


def serve():
    """The function called to run the server.

    It will simply run the FastAPI app. Also, if the selected DB is in-memory,
    it will ensure the tables are created.
    """
    if config.db == "memory":
        crud.create_tables()

    uvicorn.run(app, host=config.host, port=config.port)
