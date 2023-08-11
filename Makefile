install:
        pip install poetry &&\
        poetry install

start:
        poetry run projectai/telepuzik.py
