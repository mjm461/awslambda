# -*- coding: utf-8 -*-
"""Lambda Base AWS SSM
This is the class that implements a Lambda Base configuration using
AWS SSM.
"""

import os
from abc import abstractmethod
import json
from .lambda_base import LambdaBase

import boto3


class LambdaBaseSsm(LambdaBase):
    """Implements the Lambda Base parameters using AWS SSM"""

    def __init__(self, config_paths=None, env=None, decryption=True, recursive=True):
        """Initialization of the Lambda Base using environment variables.
        Args:
            config_paths (:obj:`set`, optional): Configuration paths to lookup in SSM.
            env (:obj:`str`, optional): env (dev, feature, staging, etc)
            decryption (:obj:`bool`, optional): Use decryption in SSM.
            recursive (:obj:`bool`, optional): Lookup paths recursively in SSM.
        """

        super().__init__()

        # Get SSM parameters
        config_paths = config_paths or os.environ.get('CONFIG_PATHS', '').split(',')
        env = env or os.environ.get('ENV', 'dev')

        if config_paths:
            client = boto3.client('ssm')

            for config_path in config_paths:
                param_details = client.get_parameters_by_path(
                    Path=os.path.join('/', env, config_path),
                    Recursive=recursive,
                    WithDecryption=decryption)

                # Loop through the returned parameters and populate the ConfigParser
                for param in param_details.get('Parameters'):
                    for key, value in json.loads(param.get('Value')).items():
                        self._parameters[os.path.join('/', '/'.join(param.get('Name').split('/')[2:]), key)] = value

    @abstractmethod
    def handle(self, event, context) -> dict:
        pass
