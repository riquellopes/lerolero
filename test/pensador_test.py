# coding: utf-8
import unittest
from nose.tools import assert_true, assert_raises, assert_equals, assert_false
from mongoengine import NotUniqueError
from app import Pensador

class PensadorTest(unittest.TestCase):
	
	def test_caso_parametros_ok_um_pensador_e_criado(self):
		"""
			Caso todos os parâmetros estejam ok, um novo pensador deve ser criado.
		"""
		p = Pensador(id='1', name='henrique', email='jj@gmail.com', access_token="123456", profile_url="http://g.com")
		p.save()
		p2 = Pensador.objects(id='1').first()
		assert_true(p.name, p2.name)
		
	def test_caso_seja_necessario_apenas_alguns_paramentros_seram_editados(self):
		"""
			Caso seja necessário apenas alguns parâmetros seram editados.
		"""
		p = Pensador.objects(id='1').first()
		p.access_token = '00000000'
		p.save()
		p2 = Pensador.objects(id='1').first()
		assert_equals(p.access_token, p2.access_token)
		Pensador.objects(id='1').delete()
		
	def test_os_emails_devem_ser_unicos(self):
		"""
			Um email só pode ser utilizado por um unico pensador.
		"""
		with assert_raises(NotUniqueError):
			p = Pensador(id='2', name='henrique', email='riquellopes@gmail.com', access_token="123456", profile_url="http://gs.com")
			p.save()
	
	def _test_a_url_do_profile_deve_ser_unica(self):
		"""
			A url do profile do pensador deve ser única.
		"""
		with assert_raises(NotUniqueError):
			p = Pensador(id='3', name='henrique', email='ex@gmail.com', access_token="123456", profile_url="http://g.com")
			p.save()
	
	def test_caso_os_tokens_nao_seja_iguais_o_metodo_deve_retornar_false(self):
		"""
			Caso os tokens não sejam iguais o método deve retornar False.
		"""
		p = Pensador.objects(id='100008212631327').first().tokenEqual('CAAI4X3G2nz4BAHm001gL0h4AV3klTSuWoL7U4QO3BthDDNyDSclfZA0SEtoV8M3vtIWWDabSWLdvWaMOAQVnJB0fidtSYE83f6SkP1GwTyICXaPjNOatDacBxApAde43x56JZCNyuKlDZBMVGr5exblcPorACz0jEBbdefCXT24ZBTEkoa8GlnlXBhynNjnoafduGAmxMgZDZD')
		assert_false(p)
	
	def test_caso_os_tokens_sejam_iguais_o_metodo_deve_retornar_true(self):
		"""
			Caso os tokens não sejam iguais o método deve retorna True.
		"""
		p = Pensador.objects(id='100000079352090').first().tokenEqual('CAAI4X3G2nz4BAHm001gL0h4AV3klTSuWoL7U4QO3BthDDNyDSclfZA0SEtoV8M3vtIWWDabSWLdvWaMOAQVnJB0fidtSYE83f6SkP1GwTyICXaPjNOatDacBxApAde43x56JZCNyuKlDZBMVGr5exblcPorACz0jEBbdefCXT24ZBTEkoa8GlnlXBhynNjnoafduGAmxMgZDZD')
		assert_true(p)