import os
import boto3
from .singleton import Singleton


class Clients(object, metaclass=Singleton):

    _localstack_ports = {
        'stepfunctions': 4585,
        's3': 4572,
        'lambda': 4574,
        'sns': 4575,
        'sqs': 4576,
        'cloudwatch': 4578,
        'ssm': 4583
    }

    def __init__(self):
        self._clients = {}

    @classmethod
    def instance(cls):
        return cls()

    @classmethod
    def client(cls, service,  region=None, endpoint_url=None):
        return cls.instance()._client(service,  region=region, endpoint_url=endpoint_url)

    def _localstack_url(self, service):
        localstack_url = os.environ.get('LOCALSTACK_URL')
        if localstack_url:
            localstack_port = self._localstack_ports.get(service)
            if localstack_port:
                return '{}:{}'.format(localstack_url, localstack_port)

    def _build_args(self, service, region, endpoint_url):
        args = {'region_name': region} if region else {}
        endpoint_url = (
                endpoint_url or
                os.environ.get(service.upper() + "_ENDPOINT_URL") or
                self._localstack_url(service)
        )

        if endpoint_url:
            args['endpoint_url'] = endpoint_url
        return args

    def _client(self, service,  region=None, endpoint_url=None):
        region or os.environ.get('AWS_REGION')
        if service in self._clients:
            if region in self._clients[service]:
                return self._clients[service][region]
        else:
            self._clients[service] = {}

        self._clients[service][region] = boto3.client(service, **self._build_args(service, region, endpoint_url))

        return self._clients[service][region]
