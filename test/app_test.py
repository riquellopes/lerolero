# coding: utf-8
import unittest
from nose.tools import assert_true, assert_raises
from mock import Mock, patch
from app import app as _app
from app import LeroLero, LeroLeroException

class MockUrllib(object):

        def __init__(self, file_test):
                self.file_test = file_test

        def read(self):
                handle = open(self.file_test)
                html = "".join( handle )
                return html

class LeroLeroTest(unittest.TestCase):

	@patch('app.urllib2.urlopen')
	def test_uma_quisicao_ao_site_deve_traser_um_lero(self, lero):
		lero.return_value = MockUrllib('lero.html')
		le = LeroLero.get()
		assert_true('Não obstante,' in str(le))
#
#	@patch('app.urllib2.urlopen')
#	def test_uma_quisicao_ao_site_deve_traser_um_lero(self, lero):
#		lero.return_value = MockUrllib('lero_2.html')
#		le = LeroLero.get()
#		assert_true('Todavia,' in le)
#
#	@patch('app.urllib2.urlopen')	
#	def test_caso_o_lero_nao_seja_encotrado_sistema_deve_levar_exception(self, lero):
#		lero.return_value = MockUrllib('lero_3.html')
#		assert_raises(LeroLeroException, LeroLero.get)

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
		assert_true('Não obstante,' in str(rs.data))
	
	def _test_criar_um_novo_agendamento(self):
		data = {
			'time-0':'1',
			'time-1':'1,0',
			'time-2':'2,1,0'
		}
		self.app.post('/schedule', data=data, follow_redirects=True)