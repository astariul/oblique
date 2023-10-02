FROM python:3.9

WORKDIR /oblique
COPY . .

RUN pip install -e .

RUN pip install pytailwindcss
RUN tailwindcss -o oblique/static/tailwind.css --minify

CMD ["oblique"]
