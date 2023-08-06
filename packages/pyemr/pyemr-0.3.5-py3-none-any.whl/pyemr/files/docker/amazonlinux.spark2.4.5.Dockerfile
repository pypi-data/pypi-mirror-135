FROM public.ecr.aws/amazonlinux/amazonlinux:latest

RUN yum -y update
RUN yum -y install yum-utils
RUN yum -y groupinstall development

RUN yum list python3*
RUN yum -y install python3 python3-dev python3-pip python3-virtualenv
RUN yum -y install deltarpm

RUN mkdir /app
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install poetry venv-pack jupyter
RUN yum install -y which
RUN yum install -y java-1.8.0-openjdk
RUN pip3 install pyspark==2.4.5

COPY . /pyemr
RUN pip3 install pyemr
RUN python3 /pyemr/utils/update_pyemr.py
RUN pyemr install_pyemr_kernel

WORKDIR /app
ENV PATH=/root/.local/bin:$PATH
ENV POETRY_VIRTUALENVS_PATH=./.docker_venv
ENV ARROW_PRE_0_15_IPC_FORMAT=1
ENV PYARROW_IGNORE_TIMEZONE=1
