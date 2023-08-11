FROM python:3.10-slim

LABEL maintainer=liubochong@pwrd.com

SHELL [ "/bin/bash", "-ceuxo", "pipefail" ]

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ='Asia/Shanghai'

ENV DEBAIN_FRONTEND=nointeractive PIP_PREFER_BINARY=1 PIP_NO_CACHE_DIR=1

RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

RUN --mount=type=cache,target=/var/cache/apt \    
    apt-get update -q

# https://stackoverflow.com/questions/40234847/docker-timezone-in-ubuntu-16-04-image
RUN echo $TZ > /etc/timezone && \
    apt-get install -q -y --allow-unauthenticated tzdata && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get install -q -y --allow-unauthenticated --no-install-recommends \
    build-essential \
    ca-certificates \
    ccache \
    cmake \
    curl \
    git \
    gcc \
    moreutils \
    fonts-dejavu-core \
    libfreetype6-dev \
    tk \
    libjpeg-dev \
    libpng-dev \
    bzip2 \
    ca-certificates \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    mercurial \
    subversion \
    wget \
    vim \
    libzbar-dev \
    sox \
    ffmpeg 

RUN mkdir -p ~/.pip && echo $'\n\
[global] \n\
no-cache-dir = true \n\
index-url = http://pypi.tuna.tsinghua.edu.cn/simple \n\
trusted-host = pypi.tuna.tsinghua.edu.cn \n\
\n' > ~/.pip/pip.conf

RUN python -m pip install --upgrade pip

RUN pip install \
    gradio==3.27.0 \
    loguru==0.7.0 \
    Pillow==9.5.0 \
    numpy==1.24.3

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 7865

ARG LOG_DIR=/web/tomcat/logs/aigc.label.com
ARG PROJECT_DIR=/web/www/aigc.label.com

RUN mkdir -p ${LOG_DIR} && \
    mkdir -p ${PROJECT_DIR}

WORKDIR ${PROJECT_DIR}
COPY . ${PROJECT_DIR}

RUN echo $'#!/bin/bash \n\
set -euxo pipefail \n\
python ui.py "$@" & \n\
tail -f /dev/null' > /usr/bin/start_entrypoint.sh \
&& chmod +x /usr/bin/start_entrypoint.sh

ENTRYPOINT ["/usr/bin/start_entrypoint.sh"]