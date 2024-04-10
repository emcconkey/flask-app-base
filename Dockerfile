FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN echo "force-unsafe-io" > /etc/dpkg/dpkg.cfg.d/02apt-speedup \
        && echo "Acquire::http {No-Cache=True;};" > /etc/apt/apt.conf.d/no-cache \
        && apt-get update \
        && apt-get -y upgrade \
        && apt-get -y install \
        python3 \
        python3-pip \
        python3-wheel \
        && rm -rf /var/lib/apt

# Set up requirements
COPY requirements.txt /

RUN pip install --upgrade pip && \
    pip install gunicorn && \
    pip install -r /requirements.txt

# Copy the folders necessary
COPY ./app/ /app
COPY scripts/app_start.sh /app

ENV FLASK_APP=app:app

WORKDIR /app
EXPOSE 80
ENTRYPOINT ["./app_start.sh"]
