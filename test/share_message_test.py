# coding: utf-8
import unittest
from nose.tools import assert_true, assert_raises, assert_equals, assert_false
from mock import Mock, patch
from app import app as _app
from app import LeroLero, Pensador, LeroLeroException

class ShareMessageTest(unittest.TestCase):
	
	def test_quanto_o_metodo_share_count_for_invocado_ele_deve_incremetar_a_quantidade(self):
		"""
			Quando o método _share_count for invocado ele deve incrementar a quantidade.
		"""
		one = LeroLero.objects(id='cb6cd342ac92b6572f6574a3b7ced18c').first()
		LeroLero.objects(id='cb6cd342ac92b6572f6574a3b7ced18c').first()._share_count()
		two = LeroLero.objects(id='cb6cd342ac92b6572f6574a3b7ced18c').first()
		assert_equals(two.share_count, 1)
		LeroLero(id='cb6cd342ac92b6572f6574a3b7ced18c', text=one.text, share_count=0).save()
		