"""Root of the `oblique` package."""
import pathlib


COMPONENTS_DIR = pathlib.Path(__file__).parent.resolve() / "components"
__version__ = "1.0.0.dev0"


# isort: off

from .configuration import config
