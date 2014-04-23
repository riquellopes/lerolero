# coding: utf-8
import unittest
from nose.tools import assert_true, assert_raises, assert_equals
from pymongo.errors import DuplicateKeyError
from app import Agendamento, Pensador

class AgendamentoTest(unittest.TestCase):
	
	def setUp(self):
		self.pensador = Pensador.objects.filter(id='1').first()
		
	def test_caso_uma_lista_de_horarios_tags_devem_ser_criadas(self):
		"""
			Caso uma lista de horarios seja passada ela deve ser transformada em tags.
		"""
		times = {
			'time-0':'1',
			'time-1':'1,0',
			'time-2':'2,1,0'
		}
		tags = [
			'time-0|1', 'time-1|1,0', 'time-2|2,1,0',
		]
		tags_created = Agendamento.create_tags(times)
		assert_equals(tags, tags_created)
	
	def test_caso_nenhuma_horario_seja_passado_nehuma_tag_deve_se_criada(self):
		"""
			Caso nenhuma lista de horario seja passada nenhuma tag será criada.
		"""
		times = {}
		tags = []
		tags_created = Agendamento.create_tags(times)
		assert_equals(tags, tags_created)
	
	def test_caso_um_none_seja_passado_uma_lista_em_branco_deve_ser_passado(self):
		"""
			Caso um none seja passado uma lista me branco deve ser criada.
		"""
		assert_equals([], Agendamento.create_tags(None))
	
	def test_caso_todas_as_informacoes_esteja_ok_um_agendamento_deve_ser_criado(self):
		tags = [
			'time-0|1', 'time-1|1,0', 'time-2|2,1,0',
		]
		Agendamento(pensador=self.pensador, times_tag=tags).save()
		assert_equals(Agendamento.objects(pensador=self.pensador).count(), 1)
		Agendamento.objects(pensador=self.pensador).delete()