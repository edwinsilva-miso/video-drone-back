FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
RUN apt-get update -y && apt-get install -y iputils-ping

COPY . .

CMD [ "gunicorn", "-w", "1", "-b", "0.0.0.0:9090", "main:app" ]
