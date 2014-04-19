# coding: utf-8
try:
	from local_config import *
except ImportError:
	from os import path, environ
	SECRET_KEY=environ.get('SECRET_KEY')
	CONSUMER_SECRET=environ.get('CONSUMER_SECRET')
	CONSUMER_KEY=environ.get('CONSUMER_KEY')
	TEST=environ.get('TEST') == "True"
	DEBUG=environ.get('DEBUG') == "True"
	FACEBOOK_CONSUMER_KEY=environ.get('FACEBOOK_CONSUMER_KEY')
	FACEBOOK_CONSUMER_SECRET=environ.get('FACEBOOK_CONSUMER_SECRET')

	MONGODB_DB=environ.get('MONGODB_DB')
	MONGODB_USERNAME=environ.get('MONGODB_USERNAME')
	MONGODB_PASSWORD=environ.get('MONGODB_PASSWORD')
	MONGODB_HOST=environ.get('MONGODB_HOST')
	MONGODB_PORT=53698