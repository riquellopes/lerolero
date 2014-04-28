# coding: utf-8
import urllib2
import re
import json
import hashlib
from math import ceil
from random import random, choice
import facebook
from flask import Flask, render_template, request, session,\
 url_for, redirect, jsonify, make_response, Response, abort
from flask_mongoengine import QuerySet, ValidationError, MongoEngine, MongoEngineSessionInterface
from flask_debugtoolbar import DebugToolbarExtension
from decorator import login_required

"""
	Crédito aos autores::
		Essa applicação foi escrita originalmente por http://www.suicidiovirtual.net/dados/lerolero.html,
		e aprimorado por http://www.lerolero.com.
		Parabéns => Juan Pujol e Felippe Nardi \0/
"""
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
	
	@classmethod
	def get(cls):
		"""Método recupera um novo lerolero na web."""
		rs=urllib2.urlopen(app.config['URL']).read()
		if not re.search("frase_aqui", rs):
			raise LeroLeroException('LeroLero not online.')
		return (''.join( re.findall('(?s)<blockquote id="frase_aqui">(.*?)</blockquote>', rs) )).decode('utf-8')
		
	@classmethod
	def random(cls):
		if choice([True, False]):
			"""
				1- Caso o seja 1 o valor deve ser recuperado do banco
			"""
			return cls.objects().limit(1).skip( cls._rand() )
		else:
			"""
				2- Valor recuperado da web parseado e salvo na nossa base
			"""
			__text = cls.get()
			__id = hashlib.md5(__text.encode('utf8')).hexdigest()
			cls.objects.insert(LeroLero(text=__text, id=__id))
			return cls.objects(id=__id)
	
	@classmethod
	def _rand(cls):
		count = cls.objects().count()
		return int( random() * count )
	
	def to_json(self, *args, **kwargs):
		"""
			Sobrescrever método para alterar propriedade _id por id.
		"""
		to_json_result = super(LeroLero, self).to_json(*args, **kwargs)
		to_json_result = json.loads(to_json_result)
		if '_id' in to_json_result:
			to_json_result['id'] = to_json_result.pop('_id')
		return json.dumps(to_json_result, *args, **kwargs)
	
	def postMenssage(self, pensador=None, host=""):
		"""
			Método utilizado para relizar poste na timeline do usuario.
		"""
		if pensador is None:
			raise LeroLeroException("Nenhum pensador foi informado.")
		
		if host.strip() is "":
			raise LeroLeroException("Host está em branco.")
						
		attachment={'caption': 'Pensamento do dia', 
					'link': "http://{0}/{1}".format(host, self.id),
					#'media': [{
						#'src':"http://{0}/static/img/platao.jpg".format(host),
						#'type':'image',
						#'href':host
					#}],
					'picture':"http://{0}/static/img/platao.jpg".format(host),
					'name': 'Pensamento do dia',
					'description':self.text.encode('utf-8').strip()}
		try:
			g = facebook.GraphAPI(pensador.access_token)
			g.put_wall_post(profile_id=pensador.id, message="", attachment=attachment)
			return True
		except Exception as e:
			raise LeroLeroException(e)
			
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
	times_tag=db.ListField()
	
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
@app.route('/<leroid>')
def home(leroid=None):
	if leroid:
		app.logger.info("Select specific an object.")
		oo = LeroLero.objects(id=leroid)
	else:
		app.logger.info("Get random information.")
		oo = LeroLero.random()
	lero = oo.only("id", "text").first()
	
	if lero is None:
		app.logger.error("Erro 404.")
		abort(404)
	try:
		pensador = Pensador.objects(id=session['user']['id']).first()
		agendamento = Agendamento.objects(pensador=pensador).first()
		times = Agendamento.create_times(agendamento.times_tag)
	except:
		times = []
	app.logger.info("Load informations")
	return render_template('template.html', **locals())
	
@app.route('/login/authorized')
def facebook_authorized():
	cookie = facebook.get_user_from_cookie(request.cookies, app.config['FACEBOOK_CONSUMER_KEY'], app.config['FACEBOOK_CONSUMER_SECRET'])
	if cookie:
		p = Pensador.objects(id=cookie["uid"]).first()
		if not p:
			app.logger.info("Pensador not exist.")
			graph = facebook.GraphAPI(cookie['access_token'])
			me = graph.get_object('me')
			p = Pensador(id=str(me["id"]), name=me['name'], email=me['email'], profile_url=me['link'], access_token=cookie['access_token'])
			p.save()
		elif p.access_token is not cookie["access_token"]:
			app.logger.info("Token don't same. oldToken:{0}".format(p.access_token))
			p = Pensador(id=p.id, name=p.name, email=p.email, profile_url=p.profile_url, access_token=cookie["access_token"])
			p.save()
		session.permanent = True
		session['user']=dict(name=p.name, profile_url=p.profile_url, id=p.id, acess_token=p.access_token)
		app.logger.info("Pesador logado. token:{0}".format( cookie["access_token"] ))
	return redirect(url_for('home'))
	
@app.route('/generate')
@app.route('/generate/<leroid>')
def generate(leroid=None):
	app.logger.info("Gerando um novo pensamento.")
	if leroid:
		app.logger.info("Select specific an object.")
		oo = LeroLero.objects(id=leroid)
	else:
		app.logger.info("Get random information.")
		oo = LeroLero.random()
	try:	
		lero = oo.only("id", "text").first().to_json(ensure_ascii=False)
		return Response( lero, mimetype='application/json; charset=utf-8')
	except:
		app.logger.error(e)
		abort(404)

@app.route('/logout')
def logout():
	session.clear()
	app.logger.info("End session.")
	return redirect(url_for('home'))

@app.route('/weeks.json')
def weeks():
	app.logger.info("Dias da semana recuperado")
	return Response( json.dumps(app.config['WEEKS'], ensure_ascii=False), mimetype='application/json; charset=utf-8')
	
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
		except ValidationError as e:
			app.logger.error(e)
			return jsonify(message='Houve um error ao tentar realizar o agendamento.', status=500)
	return jsonify(message='Agendamento realizado com sucesso.', status=200)

@app.route("/new-thought", methods=['POST'])
@login_required
def new_thought():
	abort(404)

@app.route('/thinking-now/<leroid>', methods=['GET'])
@login_required
def thinking_now(leroid):
	try:
		p = Pensador.objects(id=session['user']['id']).first()
		LeroLero.objects(id=leroid).first().postMenssage(p, request.host)
		app.logger.info("Send menssage - {0}.".format(request.host))
		return jsonify(message='Messagem posta com sucesso.', status=200)
	except Exception as e:
		app.logger.error("{0} - {1}".format(e, request.host))
		return jsonify(message='Houve ao tentar realizar postagem.', status=500)
		
@app.errorhandler(404)
def page_not_found(e):
	return 'Página não encontra.'
	
@app.context_processor
def user_loggend():
	return dict(user_loggend=session.get('user'))