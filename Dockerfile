FROM python:3.10.5-slim-bullseye

WORKDIR /usr/src/app

RUN pip install --no-cache-dir scrap_engine

COPY . .

CMD [ "python", "./pokete.py" ]
