FROM python:3.10-alpine
WORKDIR /app
COPY ./ /app
COPY requirements.txt /app
RUN apk update \
  && apk add \
    python3-dev
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 8081

RUN apk update && apk add vim
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
CMD ["crond", "-f"]
