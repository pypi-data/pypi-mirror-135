FROM python:3.9-slim

ARG EXAMPLE

COPY examples/$EXAMPLE/example.py /
COPY examples/$EXAMPLE/requirements.txt /
RUN pip install -r requirements.txt
ENTRYPOINT python example.py
