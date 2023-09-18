"""File containing the main function, serving the app."""
import uvicorn
from fastapi import FastAPI

from oblique import __version__, config
from oblique.api import handler as api_handler
from oblique.api import router as api_router
from oblique.app import handler as app_handler
from oblique.app import router as app_router
from oblique.database import crud


def serve():
    """The function called to run the server.

    It will simply run the FastAPI app. Also, if the selected DB is in-memory,
    it will ensure the tables are created.
    """
    if config.db == "memory":
        crud.create_tables()

    root_app = FastAPI(title="Oblique", version=__version__, redoc_url=None)

    root_app.add_exception_handler(*api_handler)
    root_app.add_exception_handler(*app_handler)

    root_app.include_router(app_router, tags=["HTML"])
    root_app.include_router(api_router, prefix="/api", tags=["API"])

    uvicorn.run(root_app, host=config.host, port=config.port)
