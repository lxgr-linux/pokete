FROM ubuntu:22.04 AS compile-image

WORKDIR /build

RUN apt-get update && \
    DEBIAN_FRONTEND=non-interactive apt-get install -y \
    libasound-dev \
    libpulse-dev \
    pkg-config \
    golang \
    curl

COPY playsound /build/playsound/

RUN curl -o scrap_engine.py "https://raw.githubusercontent.com/lxgr-linux/scrap_engine/master/scrap_engine.py" && \
    cd playsound && \
    go build -ldflags "-s -w" -buildmode=c-shared -buildvcs=false -o ./libplaysound.so && \
    rm -v go.mod go.sum main.go README.md

FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && \
    DEBIAN_FRONTEND=non-interactive apt-get install -y \
    alsa-base \
    pulseaudio \
    python3

RUN mkdir -p /root/.local/share/pokete && \
    ln -s /root/.local/share/pokete /data

COPY . .
COPY --from=compile-image /build /app

VOLUME ["/data"]

CMD [ "python3", "./pokete.py" ]
