# Code structure

This page introduces the technologies used for this template, as well as the overall structure of the repository.


## The demo web-app

This repository is actually a small, working web-application, for displaying various statistics about the releases of a Python package.

Under the hood, it's a simple call to the PyPi API to retrieve the releases data of a given package.

In order to showcase the usage of a database, the data from the PyPi API is cached locally in our database. Only after a certain period of time, the cache is invalidated and updated with fresh data from the PyPi API.

Aside from the web-application, we also offer a REST API so that code can consume our data as well.


## A regular python package

In order to have a clear separation of concerns, the code is organized as a python package :

* We have a `setup.py` file at the root of the repository, so we can install the package and the command line will run from anywhere
* All the code is located in the `oblique` folder
* Tests are in the `tests` folder
* Documentation is in the `docs` folder


## Source code

### Web-application & API

The code for the web-application is defined in `oblique/app.py`. It is defined as a FastAPI router and contains all the routes for the web-application.

The routes defined there are HTMX routes, and for better maintainability, we use `JinjaX`.
`JinjaX` allows us to define components as Jinja templates, and make it easier to reuse these components across files. It's particularly convenient when using HTMX.

The `JinjaX` components are defined in the `oblique/components/` folder.

The `oblique/static/` folder contains static assets used in the web-application, such as the favicon.

---

The code for the REST API is defined in `oblique/api.py`. It is also defined as a FastAPI router and contains all the routes for the API.

---

The API and the web-application might share some code (for example the business logic). The code is located in `oblique/core.py`. So both the web-application and the API can import the code from this file and use it.

---

Finally, the file `oblique/dependencies.py` contains FastAPI dependencies shared by the API and the web-application.


### Configuration & running

The configuration is in `oblique/configuration.py`.

This is where the configuration is defined, with sensible defaults values. This is the main entry point when running the application, where we can define where to run, on which port, etc...

For defining the configuration, we use `OmegaConf`, allowing us to define defaults values for most configuration keys while easily being able to overide these values from the command line or from environment variables.

---

The file `server.py` contains the function `run()`, which is the main entry point of `oblique` : it will gather the routers of the web-application and the API, define the main FastAPI app, and run it using `uvicorn`.


### Database

All the code related to the database is located in the folder `oblique/database/`. It contains the table definitions, as well as the CRUD functions to interact with the database.

The `oblique/database/README.md` file also contains the entity-relationship diagram describing the tables of that database.

For the database we use `SQLite` because it's fast and easy to get started with, and will fill most of the needs until the application really scale.  
Once it scales, it shouldn't be too hard to switch to another database since we are using `sqlalchemy`.

---

For the database migrations, `alembic` is used, and the migrations scripts are located in the folder `alembic/`.

The `alembic/README.md` file also contains more information on how to use `alembic` to create new migrations or to migrate the current database.
