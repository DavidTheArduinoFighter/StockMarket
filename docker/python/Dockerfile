FROM python:3.11 as python
WORKDIR /project
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . ./project
CMD ["python", "./project/get_data.py"]