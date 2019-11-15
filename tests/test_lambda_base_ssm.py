# -*- coding: utf-8 -*-

__author__ = "Mark McClain"
__copyright__ = "Mark McClain"
__license__ = "mit"

from unittest import TestCase
from common import LambdaBaseSsm
from unittest.mock import patch
import boto3
from moto import mock_ssm


class LambdaBaseSsmImpl(LambdaBaseSsm):

    def handle(self, event, context) -> dict:
        return event.update({})


class TestLambdaBase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    @mock_ssm
    def test_parameter_not_found(self) -> None:
        with self.assertRaises(KeyError):
            lambda_base_ssm_impl = LambdaBaseSsmImpl()
            lambda_base_ssm_impl.get_parameter('lambda-base/parameters/param')

    @mock_ssm
    def test_parameter_default(self) -> None:
        lambda_base_ssm_impl = LambdaBaseSsmImpl()
        self.assertEqual('value', lambda_base_ssm_impl.get_parameter('lambda-base/parameters/param', 'value'))

    @mock_ssm
    @patch.dict('os.environ', {'ENV': 'dev', 'CONFIG_PATHS': 'lambda-base'})
    def test_create_with_prameters(self) -> None:
        client = boto3.client('ssm')

        client.put_parameter(
            Name='/dev/lambda-base/parameters',
            Description='A test parameter',
            Value='{"param1": "param1", "param2": "param2"}',
            Type='String')

        lambda_base_ssm_impl = LambdaBaseSsmImpl()
        self.assertEqual('param1', lambda_base_ssm_impl.get_parameter('/lambda-base/parameters/param1'))
        self.assertEqual('param2', lambda_base_ssm_impl.get_parameter('/lambda-base/parameters/param2'))
        self.assertIsNotNone(lambda_base_ssm_impl)

