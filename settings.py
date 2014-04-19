# coding: utf-8
from os import path, environ

SECRET_KEY=environ.get('SECRET_KEY')
CONSUMER_SECRET=environ.get('CONSUMER_SECRET')
CONSUMER_KEY=environ.get('CONSUMER_KEY')
TEST=environ.get('TEST') == "True"
DEBUG=environ.get('DEBUG') == "True"
FACEBOOK_CONSUMER_KEY=environ.get('FACEBOOK_CONSUMER_KEY')
FACEBOOK_CONSUMER_SECRET=environ.get('FACEBOOK_CONSUMER_SECRET')