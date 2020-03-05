FROM python:3.8-slim

COPY entrypoint.sh /entrypoint.sh
COPY scanforstring.py /scanforstring.py

