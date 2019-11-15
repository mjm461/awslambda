# -*- coding: utf-8 -*-

__author__ = "Mark McClain"
__copyright__ = "Mark McClain"
__license__ = "mit"

from unittest import TestCase
from common import LambdaBaseEnv
from unittest.mock import patch
import boto3


class LambdaBaseEnvImpl(LambdaBaseEnv):

    def handle(self, event, context) -> dict:
        return event.update({})


class TestLambdaBase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    def test_parameter_not_found(self) -> None:
        with self.assertRaises(KeyError):
            lambda_base_env_impl = LambdaBaseEnvImpl(set([]))
            lambda_base_env_impl.get_parameter('param1')

    def test_parameter_default(self) -> None:
        lambda_base_env_impl = LambdaBaseEnvImpl(set([]))
        self.assertEqual('value', lambda_base_env_impl.get_parameter('param', 'value'))

    @patch.dict('os.environ', {'PARAM1': 'param1', 'PARAM2': 'param2'})
    def test_create_with_prameters(self) -> None:
        lambda_base_env_impl = LambdaBaseEnvImpl(set(['PARAM1', 'PARAM2']))
        self.assertEqual(lambda_base_env_impl.get_parameter('PARAM1'), 'param1')
        self.assertEqual(lambda_base_env_impl.get_parameter('PARAM2'), 'param2')
        self.assertIsNotNone(lambda_base_env_impl)
