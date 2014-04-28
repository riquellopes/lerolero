# coding: utf-8
import unittest
from nose.tools import assert_true, assert_raises, assert_equals, assert_false
from mock import Mock, patch
from app import app as _app
from app import LeroLero, Pensador, LeroLeroException

class FaceMock(object):
	
	def __init__(self, error=False):
		self.error = error
		
	def put_wall_post(self, *args, **kwargs):
		if self.error:
			raise 'Error generico'
		return None
			
class PostMensageTest(unittest.TestCase):
	
	@patch('app.facebook.GraphAPI')
	def test_deve_ser_possivel_realisar_um_poste_na_time_line_do_pensador(self, fb):
		fb.return_value=FaceMock()
		p = Pensador.objects(id='100000079352090').first()
		l = LeroLero.objects(id='8f596ab15ffaed3c7ff2648c3ceb40b8').first().postMenssage(p, host='http://0.0.0.0:5000/')
		assert_true(l)
	
	@patch('app.facebook.GraphAPI')
	def test_pensamentos_com_caracteres_especias_devem_ser_envidos_com_sucesso(self, fb):
		fb.return_value=FaceMock()
		p = Pensador.objects(id='100000079352090').first()
		l = LeroLero.objects(id='592d6874cca1511cf978d83791ff234d').first().postMenssage(p, host='http://0.0.0.0:5000/')
		assert_true(l)
		
	@patch('app.facebook.GraphAPI')
	def test_caso_a_mensagem_nao_seja_enviada_o_meotodo_deve_levantar_um_exception(self, fb):
		fb.return_value=FaceMock(error=True)
		with assert_raises(LeroLeroException):
			p = Pensador.objects(id='100000079352090').first()
			LeroLero.objects(id='8f596ab15ffaed3c7ff2648c3ceb40b8').first().postMenssage(p, host='http://0.0.0.0:5000/')
	
	@patch('app.facebook.GraphAPI')
	def test_caso_um_dominio_nao_seja_passado_o_post_nao_deve_ser_publicado(self, fb):
		fb.return_value=FaceMock()
		with assert_raises(LeroLeroException):
			p = Pensador.objects(id='100000079352090').first()
			l = LeroLero.objects(id='8f596ab15ffaed3c7ff2648c3ceb40b8').first().postMenssage(p)
			
	@patch('app.facebook.GraphAPI')
	def test_caso_o_metodo_nao_receba_pensador_ela_deve_levantar_ume_exception(self, fb):
		fb.return_value=FaceMock()
		with assert_raises(LeroLeroException):
			LeroLero.objects(id='8f596ab15ffaed3c7ff2648c3ceb40b8').first().postMenssage()
	
	@patch('app.facebook.GraphAPI')
	def test_caso_nao_exista_um_pesamento_carregado_o_metodo_deve_levantar_uma_exceptio(self, fb):
		fb.return_value=FaceMock()
		with assert_raises(AttributeError):
			p = Pensador.objects(id='100000079352090').first()
			LeroLero.objects(id=0).first().postMenssage(p)