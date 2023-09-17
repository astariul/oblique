import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


with open("oblique/__init__.py") as f:
    v = [line for line in f if line.startswith("__version__")][0].split('"')[1]


reqs = [
    "fastapi[all]~=0.103",
    "omegaconf~=2.3",
    "sqlalchemy~=2.0",
    "jinjax~=0.25",
]

extras_require = {
    "admin": ["alembic~=1.12"],
    "test": ["pytest~=7.0", "pytest-cov~=4.1", "coverage-badge~=1.0"],
    "hook": ["pre-commit~=3.0"],
    "lint": ["black~=23.1", "ruff~=0.0.272"],
    "docs": ["mkdocs-material~=9.0", "mkdocstrings[python]~=0.18", "mike~=1.1"],
}
extras_require["all"] = sum(extras_require.values(), [])
extras_require["dev"] = (
    extras_require["test"] + extras_require["hook"] + extras_require["lint"] + extras_require["docs"]
)

setuptools.setup(
    name="oblique",
    version=v,
    author="Nicolas REMOND",
    author_email="remondnicola@gmail.com",
    description="A template for building your webapp with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/astariul/oblique",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=reqs,
    extras_require=extras_require,
    entry_points={"console_scripts": ["oblique=oblique.app:serve"]},
)
