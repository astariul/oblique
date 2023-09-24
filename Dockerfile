FROM python:3.9

WORKDIR /oblique
COPY . .

RUN pip install -e .

CMD ["oblique"]
