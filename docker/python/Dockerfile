# Python image with necessary system dependencies
FROM python:3.11

# Set up the working directory
WORKDIR /project

# Install system dependencies for X11 and PyQt6
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

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code to the container
COPY . ./project

# Command to run the application
CMD ["python", "./project/get_data.py"]
