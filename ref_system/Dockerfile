FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app
EXPOSE 8000
