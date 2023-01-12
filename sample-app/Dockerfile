ARG TARGET_DIR="/target"

FROM python:3.8-alpine3.13 as python-alpine

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --src /usr/local/src

COPY flaskapi.py /app/flaskapi.py

EXPOSE 5000
CMD [ "python", "/app/flaskapi.py" ]
