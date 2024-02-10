FROM debian:bullseye

RUN apt update 
RUN DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends apt-utils \
    gawk wget git diffstat unzip texinfo gcc \
    build-essential chrpath socat cpio python3 python3-pip \
    python3-pexpect xz-utils debianutils iputils-ping python3-git \
    python3-jinja2 libegl1-mesa libsdl1.2-dev pylint3 xterm \
    python3-subunit mesa-common-dev zstd liblz4-tool file locales


RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8

RUN useradd -ms /bin/bash yocto
USER yocto
WORKDIR /home/yocto
