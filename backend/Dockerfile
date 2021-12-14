# syntax = docker/dockerfile:1.2
# Dockerfile
# Django 최상위 루트에서 작성
FROM python:3.8
# 컨테이너 내에서 코드가 실행될 경로 설정
WORKDIR /usr/src/app


# Install Dependencies of Miniconda
RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install miniconda3
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda create -n venv" >> ~/.bashrc && \
    echo "conda activate venv" >> ~/.bashrc

# requirements.txt에 명시된 필요한 packages 설치
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Project를 /usr/src/app으로 복사
COPY . .
# 포트 설정
#EXPOSE 8000
#CMD ["python3", "manage.py", "runserver", "0:8000"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["python", "manage.py", "runserver"]

