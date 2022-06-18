FROM python:3.10-alpine

WORKDIR /usr/src/app

RUN pip install --no-cache-dir scrap_engine && \
    mkdir -p /root/.cache/pokete && \
    ln -s /root/.cache/pokete /data

COPY . .

VOLUME ["/data"]

CMD [ "python", "./pokete.py" ]
