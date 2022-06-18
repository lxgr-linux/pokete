FROM python:3.10-alpine

WORKDIR /usr/src/app

RUN pip install --no-cache-dir scrap_engine

COPY . .

CMD [ "python", "./pokete.py" ]
