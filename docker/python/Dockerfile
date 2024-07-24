FROM python:3.11 as python

WORKDIR /project

COPY requirements.txt ./
RUN pip install -r requirements.txt

# ARG GIT_HASH
# ENV GIT_HASH=${GIT_HASH:-dev}

COPY . .