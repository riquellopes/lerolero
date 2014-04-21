# coding: utf-8
import urllib2
import re
import facebook
from flask import Flask, render_template, request, session, url_for, redirect
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
	profile_url = db.StringField(required=True)
	access_token = db.StringField(required=True)
	
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
	
@app.route('/login/authorized')
def facebook_authorized():
	cookie = facebook.get_user_from_cookie(request.cookies, app.config['FACEBOOK_CONSUMER_KEY'], app.config['FACEBOOK_CONSUMER_SECRET'])
	if cookie:
		pensador = Pensador.objects(id=cookie["uid"]).first()
		if not pensador:
			graph = facebook.GraphAPI(cookie['access_token'])
			me = graph.get_object('me')
			Pensador(id=str(me["id"]), name=me['name'], email=me['email'], profile_url=me['link'], access_token=me['access_token']).save()
		elif pensador.access_token != cookie["access_token"]:
			pensador.acess_token = cookie["access_token"];
			pensador.save()
		session['user']=dict(name=pensador.name, profile_url=pensador.profile_url, id=pensador.id, acess_token=pensador.access_token)	
	return redirect(url_for('home'))
	
@app.route('/generate')
def generate():
	return LeroLero.get()

@app.route('/timeline-post', methods=['POST'])
def timeline_post():
	return request.form['lero']

@app.context_processor
def user_loggend():
	return dict(user_loggend=session.get('user'))