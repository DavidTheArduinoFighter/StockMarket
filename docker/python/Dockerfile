# Use Python 3.11 as the base image
FROM python:3.11

WORKDIR /project

RUN apt-get update && apt-get install -y \
    libx11-xcb1 \
    libxcb-render0 \
    libxcb-shm0 \
    libxcb-xfixes0 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxcb-util1 \
    libxkbcommon-x11-0 \
    libqt5gui5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

#COPY src /project/docker/python
COPY . /project

ENV PYTHONPATH="/project"

CMD ["python", "/project/get_data.py"]
