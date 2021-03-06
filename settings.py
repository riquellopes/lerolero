# coding: utf-8
try:
	from local_config import *
except ImportError:
	from os import path, environ
	from datetime import timedelta
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
	DEBUG_TB_ENABLED = False
	PERMANENT_SESSION_LIFETIME=timedelta(minutes=30)
FACEBOOK_URL_TOKEN="https://graph.facebook.com/oauth/access_token?client_id={0}&client_secret={1}&grant_type=client_credentials".format(FACEBOOK_CONSUMER_KEY, FACEBOOK_CONSUMER_SECRET)
WEEKS = [
	{'value':0, 'text':'Domingo'},
	{'value':1, 'text':'Segunda'},
	{'value':2, 'text':'Terça'},
	{'value':3, 'text':'Quarta'},
	{'value':4, 'text':'Quinta'},
	{'value':5, 'text':'Sexta'},
	{'value':6, 'text':'Sábado'},
]

TIMES = (
	{'value':0, 'text':'12:00 AM'},
	{'value':1, 'text':'04:00 AM'},
	{'value':2, 'text':'08:00 AM'},
	{'value':3, 'text':'12:00 PM'},
	{'value':4, 'text':'04:00 PM'},
	{'value':5, 'text':'08:00 PM'},
)
URL='http://www.lerolero.com/'
URL_ORIGINAL='http://www.suicidiovirtual.net/dados/lerolero.html'
URL_GIT='http://henriquelopes.com.br'