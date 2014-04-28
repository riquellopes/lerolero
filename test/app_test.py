# coding: utf-8
import unittest
from nose.tools import assert_true, assert_raises, assert_equals
from mock import Mock, patch
from app import app as _app
from app import LeroLero, LeroLeroException, Pensador
import json
from bson import json_util

class MockUrllib(object):

        def __init__(self, file_test):
            self.file_test = file_test

        def read(self):
			handle = open(self.file_test)
			html = "".join(handle)
			return html

class LeroLeroTest(unittest.TestCase):
	
	@patch('app.urllib2.urlopen')
	def test_uma_requisicao_ao_site_deve_traser_um_lero(self, lero):
		lero.return_value = MockUrllib('lero.html')
		le = LeroLero.get()
		assert_true('Nao obstante,' in str(le))

	@patch('app.urllib2.urlopen')
	def test_uma_requisicao_ao_site_deve_traser_um_lero(self, lero):
		lero.return_value = MockUrllib('lero_2.html')
		le = LeroLero.get()
		assert_true('Todavia,' in le)

	@patch('app.urllib2.urlopen')	
	def test_caso_o_lero_nao_seja_encotrado_sistema_deve_levar_exception(self, lero):
		lero.return_value = MockUrllib('lero_3.html')
		assert_raises(LeroLeroException, LeroLero.get)
	
	@patch('app.urllib2.urlopen')
	def test_deve_existir_a_possibilidade_criar_um_objeto_json(self, lero):
		lero.return_value = MockUrllib('lero.html')
		rs = json_util.dumps({"id": "8f596ab15ffaed3c7ff2648c3ceb40b8", "text": "Nao obstante, o fenomeno da Internet estimula a padronizacao das diretrizes de desenvolvimento para o futuro."})
		assert_equals(rs, LeroLero.objects(id='8f596ab15ffaed3c7ff2648c3ceb40b8').only("id", "text").first().to_json())
		
class AppTest(unittest.TestCase):

	def setUp(self):
		self.app = _app.test_client()
		self.app.application.config['TESTING'] = True
		self.app.application.config['TEST'] = True
		self.app.application.config['DEBUG'] = False
		
	def test_home_gerar_lerolero(self):
		rs = self.app.get('/')
		assert_true('<title>Gerador de LeroLero</title>' in str(rs.data))

	@patch('app.urllib2.urlopen')	
	def test_gerar_lero(self, lero):
		lero.return_value = MockUrllib('lero.html')
		rs = self.app.get('/generate')
		assert_true('Nao obstante,' in str(rs.data))
	
	def test_caso_o_usuario_nao_esteja_logado_deve_ser_direcionando_para_a_home(self):
		data = {
			'time-0':'1',
			'time-1':'1,0',
			'time-2':'2,1,0'
		}
		r = self.app.post('/schedule', data=data, follow_redirects=True)
		assert_true('<title>Redirecting...</title>' in str(r.data))
		assert_equals(r.status, '403 FORBIDDEN')
	
	def test_caso_o_usuario_esteje_logado_ele_deve_ser_agendar_seus_pensamentos(self):
		data = {
			'time-0':'1',
			'time-1':'1,0',
			'time-2':'2,1,0'
		}
		with self.app as c:
			with c.session_transaction() as sess:
				sess['user'] = dict(id='100000079352090')	
			r = self.app.post('/schedule', data=data, follow_redirects=True)
			assert_equals(r.data, '{\n  "message": "Agendamento realizado com sucesso.", \n  "status": 200\n}')
	
	def test_caso_o_pensador_informado_nao_existe_o_retorno_deve_ser_error(self):
		data = {
			'time-0':'1',
			'time-1':'1,0',
			'time-2':'2,1,0'
		}
		with self.app as c:
			with c.session_transaction() as sess:
				sess['user'] = dict(id='8188181')	
			r = self.app.post('/schedule', data=data, follow_redirects=True)
			assert_equals(r.data, '{\n  "message": "Houve um error ao tentar realizar o agendamento.", \n  "status": 500\n}')