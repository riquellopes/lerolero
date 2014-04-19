# coding: utf-8
import urllib2
import re
from flask import Flask, render_template, request, session, url_for, redirect
from flask.ext.oauth import OAuth
from flask_mongoengine import QuerySet, ValidationError, MongoEngine

"""
	Crédito aos autores::
		Essa applicação foi escrita originalmente por http://www.suicidiovirtual.net/dados/lerolero.html,
		e aprimorado por http://www.lerolero.com.
		Parabéns => Juan Pujol e Felippe Nardi \0/
"""

__URL__='http://www.lerolero.com/'
__URL_ORIGINAL__='http://www.suicidiovirtual.net/dados/lerolero.html'
__URL_GIT__='http://henriquelopes.com.br'

app = Flask(__name__)
app.config.from_object('settings')
db=MongoEngine(app)

class LeroLeroException(Exception):
	pass

class LeroLero(object):

	@staticmethod
	def get():
		"""Método recupera um novo lerolero::"""
		rs=urllib2.urlopen(__URL__).read()
		if not re.search("frase_aqui", rs):
			raise LeroLeroException('LeroLero not online.')
		return (''.join( re.findall('(?s)<blockquote id="frase_aqui">(.*?)</blockquote>', rs) )).decode('utf-8')

# Date current:
import datetime
now = datetime.datetime.now
		
class Pensador(db.Document):
	id = db.StringField(primary_key=True)
	name = db.StringField(required=True)
	email = db.EmailField(required=True, unique=True)
	date_created=db.DateTimeField(default=now())
	
oauth = OAuth()
facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=app.config['FACEBOOK_CONSUMER_KEY'],
    consumer_secret=app.config['FACEBOOK_CONSUMER_SECRET'],
    request_token_params={'scope':'email, publish_actions'}
)

@app.route('/')
def home():
	if app.config['TEST'] == True:
		lerolero = "Evidentemente, a execucao dos pontos do programa agrega valor ao estabelecimento dos modos de operacao convencionais.";
	else:
		lerolero=LeroLero.get()
	url_lerolero=__URL__
	url_original=__URL_ORIGINAL__
	url_git=__URL_GIT__
	return render_template('template.html', **locals())

@app.route('/login')
def login():
	return facebook.authorize(callback=url_for('facebook_authorized', next=request.args.get('next') or request.referrer or None, _external=True))
	
@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
	if resp is None:
		return 'Access denied: reason=%s error=%s' (
			request.args['error_reason'],
			request.args['error_description']
		)
	session['oauth_token'] = (resp['access_token'], '')
	me = facebook.get('/me')
	#Pensador(id=me.data['id'], email=me.data['email'], name=me.data['email']).save()
	return redirect(url_for('home'))
	
@app.route('/generate')
def generate():
	return LeroLero.get()

@app.route('/timeline-post', methods=['POST'])
def timeline_post():
	return request.form['lero']

@facebook.tokengetter
def get_facebook_token():
	return session.get('facebook_token')

@app.context_processor
def user_loggend():
	return dict(user_loggend=session.get('facebook_token'))