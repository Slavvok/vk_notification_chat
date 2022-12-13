FROM python:3.10-alpine

WORKDIR /chatbot
COPY . /chatbot
COPY requirements.txt /chatbot
RUN apk update \
  && apk add \
    python3-dev
RUN python3 -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
CMD [ "python3", "main.py" ]