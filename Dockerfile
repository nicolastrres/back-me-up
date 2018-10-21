FROM python:3.6.3-alpine3.6
MAINTAINER Nicolas Agustin Torres <nicolastrres@gmail.com>


ENV APP_HOME /backmeup/

RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY requirements.txt           $APP_HOME

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ci                         $APP_HOME/ci/
COPY back_me_up                 $APP_HOME/back_me_up
COPY tests                      $APP_HOME/tests
