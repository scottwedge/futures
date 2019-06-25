FROM frolvlad/alpine-python3:latest
MAINTAINER evanwht1@gmail.com

RUN apk update && apk add --no-cache git && pip3 install pipenv
WORKDIR /futures
RUN export LC_ALL=C.UTF-8 && export LANG=C.UTF-8 && pipenv install --ignore-pipfile

# Copy futures-cron file to the cron.d directory
COPY futures-cron /etc/crontabs/root

# Run the command on container startup
CMD ["cron", "-f", "-d", "8"]
