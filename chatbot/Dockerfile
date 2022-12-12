FROM python:3.10-alpine
RUN mkdir /chatbot
WORKDIR /chatbot
COPY . /chatbot
COPY requirements.txt /chatbot
RUN apk update \
  && apk add \
    python3-dev
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 8081
CMD [ "python", "main.py" ]