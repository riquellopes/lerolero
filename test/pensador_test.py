# coding: utf-8
import unittest
from nose.tools import assert_true, assert_raises
from app import Pensador

class PensadorTest(unittest.TestCase):
	
	def test_caso_um_novo_pensador_se_log_ele_deve_ser_registrado(self):
		p = Pensador(id='1', name='henrique', email='riquellopes@gmail.com')
		p.save()
		p2 = Pensador.objects(id='1').first()
		assert_true(p.name, p2.name)