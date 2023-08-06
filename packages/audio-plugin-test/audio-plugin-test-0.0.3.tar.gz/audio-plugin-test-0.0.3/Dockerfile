FROM ubuntu:21.10 as ubuntu_base

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -yq \
&& apt-get install -yq --no-install-recommends \
    ca-certificates \
    build-essential \
    cmake \
    libboost-all-dev \
    libboost-python-dev \
    libx11-dev \
    libxrandr-dev \
    libxinerama-dev \
    libxcursor-dev \
    libasound2-dev \
    libcurl4-openssl-dev \
    libfreetype-dev \
    libgtk-4-dev \
    libwebkit2gtk-4.0-dev \
    python3 \
    python3.9-dev \
&& update-ca-certificates \
&& apt-get clean -y

RUN apt-get install -yq python3-pip git libopencv-dev
RUN pip install numpy matplotlib
RUN pip install audio-plugin-test==0.0.3

COPY test.py test.py
COPY AIBase.vst3 AIBase.vst3

RUN python3 test.py
