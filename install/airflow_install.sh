#!/bin/bash

basis_instll() {
  echo "********************"
  echo "install basic"
  echo "********************"

  #라이브러리 설치
  apt-get update -y
  apt-get upgrade -y
  apt-get install -y sudo

  sudo adduser airflow
  sudo usermod -aG sudo airflow  #make the user sudo
  sudo su airflow  #Login as airflow user

#ENV TZ=Asia/Seoul
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

  sudo apt-get update -y
  sudo apt-get upgrade -y
  sudo apt-get install -y build-essential checkinstall
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
    liblzma-dev
}

python_install() {
  echo "********************"
  echo "install python 3.8.6"
  echo "********************"

  sudo apt-get install -y wget

  cd /opt
  sudo wget https://www.python.org/ftp/python/3.8.6/Python-3.8.6.tar.xz
  sudo tar -xvf Python-3.8.6.tar.xz

  cd Python-3.8.6
  sudo ./configure --enable-optimizations
  sudo make altinstall

  # 파이썬 3.8을 python커맨드의 디폴트로 설정하기
  sudo update-alternatives --install /usr/bin/python python /usr/local/bin/python3.8 1
  sudo update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip3.8 1
}

airflow_install() {
  echo "********************"
  echo "install airflow"
  echo "********************"

  sudo apt-get install -y --no-install-recommends \
        freetds-bin \
        krb5-user \
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

#  파이썬 필수 패키지 설치
  pip install -r requirements.txt

  pip install \
    apache-airflow==1.10.12 \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.7.txt"

  echo "======================"
  echo "======================"
  echo "======================"

  pip install \
    apache-airflow[aws]==1.10.12 \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.7.txt"

  pip install \
    apache-airflow[all_dbs]==1.10.12 \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.7.txt"

  pip install \
    apache-airflow[slack]==1.10.12 \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.7.txt"

  pip install \
    apache-airflow[mysql]==1.10.12 \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.7.txt"

  pip install \
      apache-airflow[celery]==1.10.12 \
      --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.7.txt"
}

airflow_start() {

#  export AIRFLOW_HOME=/home/airflow
  echo 'AIRFLOW_HOME=/home/airflow' >> ~/.bashrc && source ~/.bashrc

  # initialize the database
  airflow initdb

  # start the web server, default port is 8080
  airflow webserver

  # start the scheduler
#  airflow scheduler
}


#basis_instll
#python_install
#airflow_install
airflow_start


##!/bin/bash
#
#install_docker() {
#  echo "********************"
#  echo "install docker"
#  echo "********************"
#
#  sudo apt-get update && sudo apt-get upgrade -y
#  sudo apt-get install -y curl \
#      build-essential
#
#  # 독커 설치
#  curl -fsSL <https://download.docker.com/linux/ubuntu/gpg> | apt-key add -
#
#  sudo add-apt-repository \
#      "deb [arch=amd64] <https://download.docker.com/linux/ubuntu> \
#      $(lsb_release -cs) \
#      stable"
#
#  sudo apt-get update
#  DEBIAN_FRONTEND=noninteractive apt-get install -y docker-ce
#  # usermod -aG docker $USER
#  usermod -aG docker root
#  systemctl enable docker
#
#  # 독커 커포스 설치
#  sudo curl -L <https://github.com/docker/compose/releases/download/1.25.0-rc2/docker-compose-`uname> -s`-`uname -m` -o /usr/local/bin/docker-compose
#  sudo chmod +x /usr/local/bin/docker-compose
#  docker-compose --version
#}
#
#install_docker
