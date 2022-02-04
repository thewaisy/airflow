FROM ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.2.3-python3.8}

# install git
USER root
RUN apt-get update
RUN apt-get install -y git wget unzip curl

# install aws_cli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/home/airflow/awscliv2.zip" \
    && unzip /home/airflow/awscliv2.zip -d /home/airflow \
    && /home/airflow/aws/install

# edit /usr/lib/ssl/openssl.cnf
# RUN sed -i 's/system_default = system_default_sect/system_default = ssl_default_sect/' /usr/lib/ssl/openssl.cnf \
#     && echo -e '\n[ssl_default_sect]\nMinProtocol = TLSv1\nCipherString = DEFAULT:@SECLEVEL=1' >> /usr/lib/ssl/openssl.cnf

# sudo 권한
# RUN echo 'airflow ALL=NOPASSWD: ALL' >> /etc/sudoers

USER airflow

#install extra
RUN pip install 'apache-airflow[apache.spark]' \
    && pip install 'apache-airflow[amazon]' \
    && pip install 'apache-airflow-providers-postgres[amazon]' \
    && pip install 'apache-airflow-providers-mysql[amazon]' \
    && pip install 'apache-airflow[elasticsearch]' \
    && pip install 'apache-airflow[presto]' \
    && pip install 'apache-airflow[virtualenv]' \
    && pip install 'apache-airflow[slack]'
    
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

