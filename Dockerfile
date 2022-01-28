FROM nvidia/cuda:11.3.1-devel-ubuntu20.04

RUN apt update
RUN apt-get install -y git
RUN cd /; \
  git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose.git \
  && cd openpose \
  && git reset --hard 6f0b8868bc4833b4a6156f020dd6d486dcf8a976
WORKDIR /openpose

ENV TZ=America/Los_Angeles
ENV LANG=en_US.UTF-8
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
  cmake \
  ffmpeg \
  ipython3 \
  libcudnn8-dev \
  libopencv-dev \
  libopencv-videoio4.2 \
  lsb-release \
  sudo \
  tzdata \
  vim-tiny \
  wget \
  x11-utils \
  xauth \
  zsh
RUN git submodule update --init --recursive --remote
RUN cd models; ./getModels.sh
RUN /bin/bash /openpose/scripts/ubuntu/install_deps.sh
RUN mkdir build; cd build; cmake -DBUILD_PYTHON=1 ..
RUN cd build; make -j 6
