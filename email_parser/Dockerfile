FROM python:3.10-alpine
WORKDIR /app
COPY . /app
COPY requirements.txt /app
RUN apk update \
  && apk add \
    python3-dev
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 8081
CMD [ "python", "app.py" ]