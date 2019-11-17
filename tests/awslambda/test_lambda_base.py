# -*- coding: utf-8 -*-

__author__ = "Mark McClain"
__copyright__ = "Mark McClain"
__license__ = "mit"

from unittest import TestCase
from awslambda import LambdaBase


class LambdaBaseImpl(LambdaBase):

    def handle(self, event, context) -> dict:
        event.update({'test': 'test'})
        return event


class TestLambdaBase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    def test_handler(self) -> None:
        self.assertDictEqual({'test': 'test'}, LambdaBaseImpl.get_handler()({}, None))

    def test_parameter_not_found(self) -> None:
        with self.assertRaises(KeyError):
            lambda_base_impl = LambdaBaseImpl({})
            lambda_base_impl.get_parameter('param1')

    def test_parameter_default(self) -> None:
        lambda_base_impl = LambdaBaseImpl({})
        self.assertEqual('value', lambda_base_impl.get_parameter('param', 'value'))

    def test_create_with_prameters(self) -> None:
        lambda_base_impl = LambdaBaseImpl({'PARAM1': 'param1', 'PARAM2': 1})

        self.assertEqual(lambda_base_impl.get_parameter('PARAM1'), 'param1')
        self.assertTrue(isinstance(lambda_base_impl.get_parameter('PARAM1'), str))

        self.assertEqual(lambda_base_impl.get_parameter('PARAM2'), 1)
        self.assertTrue(isinstance(lambda_base_impl.get_parameter('PARAM2'), int))
