FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
RUN export DEBIAN_FRONTEND=noninteractive
# 필수 패키지 설치
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y sudo

RUN sudo adduser airflow && \
    sudo usermod -aG sudo airflow && \
    sudo su airflow

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN sudo apt-get update -y && \
    sudo apt-get upgrade -y && \
    sudo apt-get install -y build-essential checkinstall && \
    sudo apt-get install -y libreadline-gplv2-dev \
        libncursesw5-dev \
        libssl-dev \
        libsqlite3-dev \
        tk-dev \
        libgdbm-dev \
        libc6-dev \
        libbz2-dev \
        libffi-dev \
        zlib1g-dev \
        liblzma-dev \
        gcc


# 파이썬 설치
RUN sudo apt-get install -y wget

RUN cd /opt && \
    sudo wget https://www.python.org/ftp/python/3.6.12/Python-3.6.12.tar.xz && \
    sudo tar -xvf Python-3.6.12.tar.xz

RUN cd /opt/Python-3.6.12 && \
    sudo ./configure --enable-optimizations && \
    sudo make altinstall

# 파이썬 3.8을 python커맨드의 디폴트로 설정하기
RUN sudo update-alternatives --install /usr/bin/python python /usr/local/bin/python3.6 1
RUN sudo update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip3.6 1


# airflow 설치
RUN sudo DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
        freetds-bin \
        krb5-user \
        libpam-krb5 \
        ldap-utils \
        libffi6 \
        libsasl2-2 \
        libsasl2-modules \
        libssl1.1 \
        locales  \
        lsb-release \
        sasl2-bin \
        sqlite3 \
        unixodbc \
        libmysqlclient-dev \
        libpq-dev

COPY ./requirements.txt /home/airflow/requirements.txt
COPY ./constraints.txt /home/airflow/constraints.txt

RUN pip install --upgrade pip

RUN pip install cython
RUN pip install wheel

RUN pip install -r /home/airflow/requirements.txt
#RUN pip install -c /home/airflow/constraints.txt

RUN pip install apache-airflow==1.10.12 \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.6.txt"
#
#RUN pip install \
#    apache-airflow[aws]==1.10.12 \
#    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.7.txt"
#
RUN pip install \
    apache-airflow[all_dbs]==1.10.12 \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.6.txt"

#RUN pip install \
#    apache-airflow[slack]==1.10.12 \
#    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.7.txt"
#
##RUN pip install \
##    apache-airflow[mysql]==1.10.12 \
##    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.7.txt"
#
#RUN pip install \
#    apache-airflow[celery]==1.10.12 \
#    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.7.txt"