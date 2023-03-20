# pull official base image
FROM python:3.9.6-alpine

# set working directory
WORKDIR /usr/src/maradomadstore

# environment variables
ENV PYTHONDONTWRITEBYTECODE 1
# DON'T BUFFER STDOUT AND STDERR
ENV PYTHONUNBUFFERED 1

# psycopg deps
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# weasyprint
RUN apk add py3-pip python3-dev pango zlib-dev jpeg-dev openjpeg-dev g++ libffi-dev
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/maradomadstore/entrypoint.sh
RUN chmod +x /usr/src/maradomadstore/entrypoint.sh
# copy project
COPY . .
RUN ls /usr/src/maradomadstore

# run entrypoint
ENTRYPOINT [ "/usr/src/maradomadstore/entrypoint.sh" ]
