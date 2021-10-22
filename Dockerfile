FROM python:3.9-buster AS base

WORKDIR /usr/src/app

COPY Pipfile* ./

RUN apt-get update && apt-get -y install python3-pip

RUN ["pip3", "install", "pipenv"]

RUN ["pipenv", "install", "--system", "--deploy", "--ignore-pipfile"]

COPY . .

FROM base AS dev

ENV FLASK_ENV=development
ENV FLASK_APP=app.py

EXPOSE 5000

# run api server
CMD  ["flask", "run", "--host=0.0.0.0"]

FROM base AS prod

ENV FLASK_ENV=production
ENV FLASK_APP=app.py

EXPOSE 5000

# run api server
CMD  ["waitress-serve", "--port=5000" ,"app:app"]