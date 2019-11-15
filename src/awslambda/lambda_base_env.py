# -*- coding: utf-8 -*-
"""Lambda Base Environment Variables
This is the class that implements a Lambda Base configuration using
environment variables.
"""

import os
from abc import abstractmethod
from .lambda_base import LambdaBase


class LambdaBaseEnv(LambdaBase):
    """Implements the Lambda Base parameters using environment variables"""

    def __init__(self, environ_vars: dict):
        """Initialization of the Lambda Base using environment variables.
        Args:
            environ_vars (dict): Environment variables used by the lambda.
        """

        super().__init__()

        for environ_var, environ_type in environ_vars.items():
            value = os.environ.get(environ_var)
            if value:
                self._parameters[environ_var] = environ_type(value)

    @abstractmethod
    def handle(self, event, context) -> dict:
        pass
