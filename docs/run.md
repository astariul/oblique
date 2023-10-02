# Running the app

This page explains how to run the demo web-application.


## Clone the repository

```bash
git clone https://github.com/astariul/oblique.git
cd clothion
```


## Create the database

Create a folder where you will keep your SQLite database :

```bash
mkdir ~/data
```

---

Then install `alembic` :

```bash
pip install alembic
```

---

Then create the database and initialize the tables :

```bash
OBLIQUE_DB_PATH="~/data/oblique.sql" alembic upgrade head
```


## Run with Docker

If you have Docker installed, running the web-app is easy. First, build the Docker image :

```bash
docker build -t oblique .
```

---

Then run the container, linking the database we created earlier :

```bash
docker run -p 9810:9810 -v ~/data:/oblique/data -e OBLIQUE_DB_PATH="/oblique/data/oblique.sql" oblique
```

## Run from the command line

If you don’t have Docker, you can also install `oblique` locally and run it from the command line :

```bash
pip install -e .
OBLIQUE_DB_PATH="~/data/oblique.sql" oblique
```

!!! info
    Note that if you use the command line instead of Docker, you need to build TailwindCSS yourself. You can do this by running :

    ```bash
    pip install pytailwindcss
    tailwindcss -o oblique/static/tailwind.css --minify
    ```
