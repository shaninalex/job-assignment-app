FROM python:3.12.3-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apk update \
#     apk add python3-dev
#
# COPY . .
#
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
#
# RUN chmod +x /usr/src/app/entrypoint.sh
# ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]

# pull official base image
# FROM python:3.12.3-alpine

# set work directory
WORKDIR /usr/src/app

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
