FROM nimmis/ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive

# set default java environment variable
ENV JAVA_VERSION_MAJOR=8 \
    JAVA_VERSION_MINOR=111 \
    JAVA_HOME=/usr/lib/jvm/default-jvm \
    PATH=${PATH}:/usr/lib/jvm/default-jvm/bin/

RUN add-apt-repository ppa:openjdk-r/ppa -y && \
    # update data from repositories
    apt-get update && \
    # upgrade OS
    apt-get -y dist-upgrade && \
    # Make info file about this build
    printf "Build of nimmis/java:openjdk-8-jdk, date: %s\n"  `date -u +"%Y-%m-%dT%H:%M:%SZ"` > /etc/BUILDS/java && \
    # install application
    apt-get install -y --no-install-recommends openjdk-8-jdk && \
    # fix default setting
    ln -s java-8-openjdk-amd64  /usr/lib/jvm/default-jvm && \
    # remove apt cache from image
    apt-get clean all

# Check Java version
RUN java -version && \
    javac -version

# Install linux packages & GCC
RUN apt-get update
RUN apt-get -qq -y install git curl build-essential subversion perl wget unzip vim bc

# to use gcov
ENV COMPILE_PARAMETERS "--coverage -DHAVE_SYS_SIGLIST -DSYS_SIGLIST_DECLARED -DHAVE_ALLOCA_H"

ENV experiment_root "/root"

# Install Python
RUN add-apt-repository -y ppa:fkrull/deadsnakes
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3.6 python3.6-dev python3-pip python3-setuptools python3-wheel gcc
RUN python3.6 -m pip install pip --upgrade

# Check Java version
RUN java -version && \
    javac -version

COPY ./targets/gzip_1.5.tar.gz /root/gzip.tar.gz
COPY ./targets/grep_1.2.tar.gz /root/grep.tar.gz
COPY ./targets/sed_2.0.tar.gz /root/sed.tar.gz
COPY ./targets/flex_1.1.tar.gz /root/flex.tar.gz

RUN cd /root
RUN tar -xzvf gzip.tar.gz
RUN tar -xzvf grep.tar.gz
RUN tar -xzvf sed.tar.gz
RUN tar -xzvf flex.tar.gz

WORKDIR /root/workspace