# Python image with necessary system dependencies
FROM python:3.11

# Set up the working directory
WORKDIR /project

# Install system dependencies for X11 and PyQt6
RUN apt-get update && apt-get install -y \
    libxkbcommon-x11-0 \
    libxcb-xinerama0 \
    libgl1-mesa-glx \
    python3-pyqt6 \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code to the container
COPY . ./project

# Command to run the application
CMD ["python", "./project/get_data.py"]
