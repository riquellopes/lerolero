# coding: utf-8
import urllib2
import re
import facebook
import json
import hashlib
from flask import Flask, render_template, request, session,\
 url_for, redirect, jsonify, make_response, Response
from flask_mongoengine import QuerySet, ValidationError, MongoEngine, MongoEngineSessionInterface
from flask_debugtoolbar import DebugToolbarExtension
from decorator import login_required

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
app.session_interface = MongoEngineSessionInterface(db)
toolbar = DebugToolbarExtension(app)

class LeroLeroException(Exception):
	pass

class LeroLero(db.Document):
	id = db.StringField(primary_key=True)
	text = db.StringField(required=True)
	
	@staticmethod
	def get():
		"""Método recupera um novo lerolero::"""
		rs=urllib2.urlopen(__URL__).read()
		if not re.search("frase_aqui", rs):
			raise LeroLeroException('LeroLero not online.')
		return (''.join( re.findall('(?s)<blockquote id="frase_aqui">(.*?)</blockquote>', rs) )).decode('utf-8')
	
#	def __repr__(self):
#		"""
#			Caso o pensamento não exista em nossa base o sistema tenta criar um, se o for necessario
#			recupera algum especifico e não for encotrado o sistema vai levantar uma exception.
#		"""
#		if self.id is not None:
#			self.objects(id=self.id).to_json()
#			
#		text = LeroLero.get()
#		id = hashlib.md5(text).hexdigest()
#		if self.id == id:
#			self.text = text
#		return json.dumps(self._data)
	
	@classmethod
	def random(cls, **kwargs):
		from random import randint
		if randint(0,1):
			"""
				Caso o seja 1 o valor deve ser recuperado do banco
			"""
			return cls.objects(**kwargs)
		else:
			"""
				Valor recuperado da web e parseado e salvo.
			"""
			cls.text = LeroLero.get()
			cls.id = hashlib.md5(text).hexdigest()
			
			return 'Web'
		
		
import datetime
now = datetime.datetime.now
	
class Pensador(db.Document):
	"""
		Content responsável em armazenar todos os pensadores::
	"""
	id = db.StringField(primary_key=True)
	name = db.StringField(required=True)
	email = db.EmailField(required=True, unique=True)
	date_created=db.DateTimeField(default=now())
	profile_url = db.URLField(required=True)
	access_token = db.StringField(required=True)

class Agendamento(db.Document):
	"""
		Content responsável por todos os agendamentos de pensamentos::
	"""
	pensador=db.ReferenceField(Pensador, primary_key=True)
	times_tag=db.ListField(required=True)
	
	@staticmethod
	def create_tags(times=None):
		"""
			Método cria tags com os horários que foram selecionandos pelo pensador::
		"""
		if times is None or times is "":
			return []
		tags=[]
		for time in times:
			if times[time]:
				tags.append("{0}|{1}".format(time, times[time]))
		tags.sort()
		return tags
	
	@staticmethod
	def create_times(tags=None):
		"""
			Método cria times para a template.
		"""
		if tags is None or tags is "":
			return {}
		times = {}
		for tag in tags:
			index,value = tag.encode('utf8').split('|')
			times[index] = value.encode('utf8').split(',')
		return times
		
@app.route('/')
def home():
	if app.config['DEBUG'] == True:
		app.logger.info("Em modo teste.")
		lerolero = "Evidentemente, a execucao dos pontos do programa agrega valor ao estabelecimento dos modos de operacao convencionais.";
	else:
		lerolero=LeroLero.get()
	url_lerolero=__URL__
	url_original=__URL_ORIGINAL__
	url_git=__URL_GIT__
	try:
		pensador = Pensador.objects(id=session['user']['id']).first()
		agendamento = Agendamento.objects(pensador=pensador).first()
		times = Agendamento.create_times(agendamento.times_tag)
	except:
		times = []
	return render_template('template.html', **locals())
	
@app.route('/login/authorized')
def facebook_authorized():
	cookie = facebook.get_user_from_cookie(request.cookies, app.config['FACEBOOK_CONSUMER_KEY'], app.config['FACEBOOK_CONSUMER_SECRET'])
	if cookie:
		pensador = Pensador.objects(id=cookie["uid"]).first()
		if not pensador:
			graph = facebook.GraphAPI(cookie['access_token'])
			me = graph.get_object('me')
			pensador = Pensador(id=str(me["id"]), name=me['name'], email=me['email'], profile_url=me['link'], access_token=cookie['access_token'])
			pensador.save()
		elif pensador.access_token != cookie["access_token"]:
			pensador.acess_token = cookie["access_token"];
			pensador.save()
		session.permanent = True
		session['user']=dict(name=pensador.name, profile_url=pensador.profile_url, id=pensador.id, acess_token=pensador.access_token)
	return redirect(url_for('home'))
	
@app.route('/generate')
def generate():
	app.logger.info("Gerando um novo pensamento.")
	return LeroLero.get()

@app.route('/logout')
def logout():
	session.clear()
	app.logger.info("End session.")
	return redirect(url_for('home'))

@app.route('/weeks.json')
def weeks():
	app.logger.info("Dias da semana recuperado")
	return Response( json.dumps((app.config['WEEKS'])), mimetype='application/json')
	
@app.route('/times.json')
def times():
	app.logger.info("Horarios recuperado")
	return Response( json.dumps((app.config['TIMES'])), mimetype='application/json')

@app.route('/schedule', methods=['POST', 'GET'])
@login_required
def schedule():
	app.logger.info("start schedule")
	if request.method == 'POST':
		try:
			tags = Agendamento.create_tags(request.form)
			pensador = Pensador.objects(id=session['user']['id']).first()
			Agendamento(pensador=pensador, times_tag=tags).save()
			app.logger.info("salved schedule")
		except ValidationError:
			return jsonify(message='Houve um error ao tentar realizar o agendamento.', status=500)
	return jsonify(message='Agendamento realizado com sucesso.', status=200)
	
@app.context_processor
def user_loggend():
	return dict(user_loggend=session.get('user'))