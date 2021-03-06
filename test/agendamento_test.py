# coding: utf-8
import unittest
from nose.tools import assert_true, assert_raises, assert_equals
from pymongo.errors import DuplicateKeyError
from app import Agendamento, Pensador

class AgendamentoTest(unittest.TestCase):
	
	def setUp(self):
		p = Pensador(id='00005', name='Jonas', email='joca@gmail.com', access_token="123456", profile_url="http://j.com")
		p.save()
		self.pensador = p
	
	def tearDown(self):
		Pensador.objects(id='00005').delete()
			
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
	
	def test_e_necessario_relisar_a_engenharia_reversa_das_tags(self):
		times = {
			'time-0':['1'],
			'time-1':['1','0'],
			'time-2':['2','1','0']
		}
		tags = [
			'time-0|1', 'time-1|1,0', 'time-2|2,1,0',
		]
		times_created = Agendamento.create_times(tags)
		assert_equals(times, times_created)
	
	def test_caso_seja_passado_tags_em_branco_uma_lista_vazia_e_recuperada(self):
		times = {}
		tags = []
		times_created = Agendamento.create_times(times)
		assert_equals(times, times_created)
	
	def test_caso_seja_passado_none_tambem_deve_ser_recuperado_uma_lista_vazia(self):
		assert_equals({}, Agendamento.create_times(None))
				
	def test_caso_um_tempo_seja_passado_sem_uma_marcacao_ele_deve_ser_despensado(self):
		"""
			Caso um tempo seja passado sem uma marcação ele de ser despensado.
		"""
		times = {
			'time-0':'1',
			'time-1':'',
			'time-2':''
		}
		tags = [
			'time-0|1',
		]
		tags_created = Agendamento.create_tags(times)
		assert_equals(tags, tags_created)
		
	def test_caso_todas_as_informacoes_esteja_ok_um_agendamento_deve_ser_criado(self):
		"""
			Caso todos as informações estejam ok um agendamento deve ser criado.
		"""
		tags = [
			'time-0|1', 'time-1|1,0', 'time-2|2,1,0',
		]
		Agendamento(pensador=self.pensador, times_tag=tags).save()
		assert_equals(Agendamento.objects(pensador=self.pensador).count(), 1)
		Agendamento.objects(pensador=self.pensador).delete()