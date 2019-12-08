FROM python:3-alpine

WORKDIR /usr/src/app
COPY src/ /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "-u", "app.py" ]
