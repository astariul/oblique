# Oblique

## Introduction

Welcome to the documentation of `oblique`.

`oblique` is a template repository, containing a small web-application using FastAPI and HTMX, to help you get started writting your own application / API.

`oblique` uses the following stack :

* **`FastAPI`** for the web API
* **`HTMX`** to have interactivity without JS
* **`JinjaX`** for clean server-side components
* **`TailwindCSS`** for component's design
* **`SQLite`**, **`sqlalchemy`**, and **`alembic`** for the database
* **`Docker`** of course

If you want to use this template, follow the instructions at the [Usage](usage.md) page.

## Installation

### Local

`oblique` isn't published as a package in PyPi. Install it locally by :

```bash
git clone https://github.com/astariul/oblique.git
cd oblique
pip install -e .
```

or :

```bash
pip install git+https://github.com/astariul/oblique.git
```

### Extra dependencies

You can also install extras dependencies, for example :

```bash
pip install -e .[docs]
```

Will install necessary dependencies for building the docs.

!!! hint
    If you installed the package directly from github, run :
    ```bash
    pip install "oblique[docs] @ git+https://github.com/astariul/oblique.git"
    ```

---

List of extra dependencies :

* **`admin`** : Dependencies for managing the database.
* **`test`** : Dependencies for running unit-tests.
* **`hook`** : Dependencies for running pre-commit hooks.
* **`lint`** : Dependencies for running linters and formatters.
* **`docs`** : Dependencies for building the documentation.
* **`dev`** : `test` + `hook` + `lint` + `docs`.
* **`all`** : All extra dependencies.

## Contribute

To contribute, install the package locally (see [Installation](#local)), create your own branch, add your code (and tests, and documentation), and open a PR !

### Pre-commit hooks

Pre-commit hooks are set to check the code added whenever you commit something.

When you try to commit your code, hooks are automatically run, and if you code does not meet the quality required by linters, it will not be committed. You then have to fix your code and try to commit again !

!!! important
    If you never ran the hooks before, install it with :
    ```bash
    pre-commit install
    ```

!!! info
    You can manually run the pre-commit hooks with :
    ```bash
    pre-commit run --all-files
    ```

### Unit-tests

When you contribute, you need to make sure all the unit-tests pass. You should also add tests if necessary !

You can run the tests with :

```bash
pytest
```

!!! info
    Tests are not included in the pre-commit hooks, because running the tests might be slow, and for the sake of developpers we want the pre-commit hooks to be fast !

!!! info
    Pre-commit hooks will not run the tests, but it will automatically update the coverage badge !

!!! hint
    To get the coverage report in HTML format, run :
    ```bash
    pytest --cov-report=html
    ```
    And then open the file `htmlcov/index.html` with your browser.

### Documentation

When you contribute, make sure to keep the documentation up-to-date.

You can visualize the documentation locally by running :

```bash
mkdocs serve
```
