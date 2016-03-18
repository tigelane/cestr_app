FROM ubuntu:latest

MAINTAINER Tige Phillips <tige@tigelane.com>
# This container runs the application layer of CESTR
# CESTR is a very simple blog tool for demonstrating
# a three tier application

RUN apt-get update
RUN apt-get -y upgrade

EXPOSE 5000

#################
# GIT and MYSQL #
#################
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install git mysql-client

####################
# PYTHON and TOOLS #
####################
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python2.7 python-pip python-dev libmysqlclient-dev
RUN DEBIAN_FRONTEND=noninteractive pip install MySQL-python flask

#################
# cestr install #
#################
ADD cestr_app.py /opt/

# By default when this container runs, simply start the application
CMD /opt/cestr_app.py