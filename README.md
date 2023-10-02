<h1 align="center">oblique</h1>
<p align="center">
A template for building your webapp with Python
</p>

<p align="center">
    <a href="https://github.com/astariul/oblique/releases"><img src="https://img.shields.io/github/release/astariul/oblique.svg" alt="GitHub release" /></a>
    <a href="https://github.com/astariul/oblique/actions/workflows/pytest.yaml"><img src="https://github.com/astariul/oblique/actions/workflows/pytest.yaml/badge.svg" alt="Test status" /></a>
    <a href="https://github.com/astariul/oblique/actions/workflows/lint.yaml"><img src="https://github.com/astariul/oblique/actions/workflows/lint.yaml/badge.svg" alt="Lint status" /></a>
    <img src=".github/badges/coverage.svg" alt="Coverage status" />
    <a href="https://astariul.github.io/oblique"><img src="https://img.shields.io/website?down_message=failing&label=docs&up_color=green&up_message=passing&url=https%3A%2F%2Fastariul.github.io%2Foblique" alt="Docs" /></a>
    <a href="https://github.com/astariul/oblique/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="licence" /></a>
</p>

<p align="center">
  <a href="#description">Description</a> •
  <a href="#install">Install</a> •
  <a href="#usage">Usage</a> •
  <a href="#use-this-template">Use this template</a> •
  <a href="#docker">Docker</a> •
  <a href="#contribute">Contribute</a>
  <br>
  <a href="https://astariul.github.io/oblique/" target="_blank">Documentation</a>
</p>


<h2 align="center">Description</h2>

**`oblique`** is a template repository for building your web application with FastAPI and HTMX.

Here is the list of tools used in this template :

* **`FastAPI`** for the web API
* **`HTMX`** to have interactivity without JS
* **`JinjaX`** for clean server-side components
* **`TailwindCSS`** for component's design
* **`SQLite`**, **`sqlalchemy`**, and **`alembic`** for the database
* **`Docker`** of course


<h2 align="center">Install</h2>

Install `oblique` with :

```
git clone https://github.com/astariul/oblique.git
cd oblique
pip install -e .
```

---

You also need to build Tailwind CSS file :

```bash
pip install pytailwindcss
tailwindcss -o oblique/static/tailwind.css --minify
```


<h2 align="center">Usage</h2>

This template is a simplistic web-application that retrieve some statistics from the PyPi API and display it to the user.

Just for demonstration purpose, you can check if the package is correctly installed by running :

```bash
oblique
```

You can then navigate to [http://0.0.0.0:9810/](http://0.0.0.0:9810/) and try the application.


<h2 align="center">Use this template</h2>

To use this template, click the button "Use this template" :

<p align="center">
  <a href="https://github.com/astariul/oblique/generate"><img src="https://img.shields.io/badge/%20-Use%20this%20template-green?style=for-the-badge&color=347d39" alt="Use template" /></a>
</p>

It will prompt you to create a new Github repository.

Then replace the content in your freshly created repository, with your own code.  
Check the exhaustive list of things to change in the [documentation](https://astariul.github.io/oblique/latest/usage/).


<h2 align="center">Docker</h2>

`oblique` provides a Dockerfile, so it's super easy to run.

First, clone the repository :

```bash
git clone https://github.com/astariul/oblique.git
cd clothion
```

Then create the database with alembic :

```bash
mkdir ~/data
pip install alembic
OBLIQUE_DB_PATH="~/data/oblique.sql" alembic upgrade head
```

And finally build the Docker image and run it :

```bash
docker build -t oblique .
docker run -p 9810:9810 -v ~/data:/oblique/data -e OBLIQUE_DB_PATH="/oblique/data/oblique.sql" oblique
```


<h2 align="center">Contribute</h2>

To contribute, install the package locally, create your own branch, add your code (and tests, and documentation), and open a PR !

### Pre-commit hooks

Pre-commit hooks are set to check the code added whenever you commit something.

If you never ran the hooks before, install it with :

```bash
pre-commit install
```

---

Then you can just try to commit your code. If your code does not meet the quality required by linters, it will not be committed. You can just fix your code and try to commit again !

---

You can manually run the pre-commit hooks with :

```bash
pre-commit run --all-files
```

### Tests

When you contribute, you need to make sure all the unit-tests pass. You should also add tests if necessary !

You can run the tests with :

```bash
pytest
```

---

Tests are not included in the pre-commit hooks, because running the tests might be slow, and for the sake of developpers we want the pre-commit hooks to be fast !

Pre-commit hooks will not run the tests, but it will automatically update the coverage badge !

If you want to get the coverage report in HTML format, run :

```bash
pytest --cov-report=html
```

And then open the file `htmlcov/index.html` with your browser.

### Documentation

The documentation should be kept up-to-date. You can visualize the documentation locally by running :

```bash
mkdocs serve
```
