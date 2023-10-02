"""Root of the `oblique` package."""
import pathlib


COMPONENTS_DIR = pathlib.Path(__file__).parent.resolve() / "components"
ASSETS_DIR = pathlib.Path(__file__).parent.resolve() / "static"
__version__ = "0.1.0"


# isort: off

from .configuration import config  # noqa: E402
from .server import run  # noqa: E402
