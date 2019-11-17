# -*- coding: utf-8 -*-

__author__ = "Mark McClain"
__copyright__ = "Mark McClain"
__license__ = "mit"

import os
from unittest import TestCase
from unittest.mock import patch
from awslambda import Clients


class TestClients(TestCase):

    def test_client_cached(self) -> None:

        with patch.object(Clients, '_build_args', wraps=Clients.instance()._build_args) as mock:
            s3_client_1 = Clients.client('s3', region='test-cached')
            s3_client_2 = Clients.client('s3', region='test-cached')

            self.assertEqual(1, mock.call_count)
            self.assertEqual(s3_client_1, s3_client_2)

    def test_client_multi_client(self) -> None:

        with patch.object(Clients, '_build_args', wraps=Clients.instance()._build_args) as mock:
            Clients.client('s3', region='multi-client')
            Clients.client('lambda', region='multi-client')

            self.assertEqual(2, mock.call_count)

    @patch.dict(os.environ, {'S3_ENDPOINT_URL': 'http://localhost:4585'})
    def test_client_endpoint_url(self) -> None:
        client = Clients.client('s3', region='s3-endpoint-url')

        self.assertEqual(client._endpoint.host, 'http://localhost:4585')

    @patch.dict(os.environ, {'LOCALSTACK_URL': 'http://localhost'})
    def test_client_localstack(self) -> None:
        for service, port in Clients._localstack_ports.items():
            client = Clients.client(service, region='localstack')

            self.assertEqual(client._endpoint.host, '{}:{}'.format('http://localhost', port))
