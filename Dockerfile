from python:3.11.5

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
VOLUME ["/usr/src/app"]
CMD [ "python", "./main.py" ]