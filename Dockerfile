FROM alpine:3.15 AS compile-image

RUN apk add \
    python3-dev \
    py3-pip \
    py3-gst \
    gobject-introspection-dev \
    cairo-dev \
    build-base

RUN python3 -m pip install --user scrap_engine playsound pygobject

FROM alpine:3.15

RUN apk add --no-cache \
    python3-dev \
    py3-gst

COPY --from=compile-image /root/.local /root/.local
ENV PATH="/root/.local/bin:$PATH"

RUN mkdir -p /root/.cache/pokete && \
    ln -s /root/.cache/pokete /data

COPY . .

VOLUME ["/data"]

CMD [ "python3", "./pokete.py" ]
