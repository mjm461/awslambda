# -*- coding: utf-8 -*-

__author__ = "Mark McClain"
__copyright__ = "Mark McClain"
__license__ = "mit"

from unittest import TestCase
from awslambda import LambdaBaseEnv
from unittest.mock import patch


class LambdaBaseEnvImpl(LambdaBaseEnv):

    def handle(self, event, context) -> dict:
        return event.update({})


class TestLambdaBaseEnv(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    def test_parameter_not_found(self) -> None:
        with self.assertRaises(KeyError):
            lambda_base_env_impl = LambdaBaseEnvImpl({})
            lambda_base_env_impl.get_parameter('param1')

    def test_parameter_default(self) -> None:
        lambda_base_env_impl = LambdaBaseEnvImpl({})
        self.assertEqual('value', lambda_base_env_impl.get_parameter('param', 'value'))

    @patch.dict('os.environ', {'PARAM1': 'param1', 'PARAM2': '1'})
    def test_create_with_prameters(self) -> None:
        lambda_base_env_impl = LambdaBaseEnvImpl({'PARAM1': str, 'PARAM2': int})

        self.assertEqual(lambda_base_env_impl.get_parameter('PARAM1'), 'param1')
        self.assertTrue(isinstance(lambda_base_env_impl.get_parameter('PARAM1'), str))

        self.assertEqual(lambda_base_env_impl.get_parameter('PARAM2'), 1)
        self.assertTrue(isinstance(lambda_base_env_impl.get_parameter('PARAM2'), int))
