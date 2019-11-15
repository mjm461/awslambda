# -*- coding: utf-8 -*-
"""Lambda Base
This is the base class for a lambda which includes setting up configuration and loggers.
"""

import os
import logging
from abc import ABC, abstractmethod


def memoize(f):
    """Annotation to memoize a method.  Wras up a method so that it returns
    the same value when it is called.  Used to wrap up the Lambda Base so
    it is only configured once.

    Args:
        f (function): The function to be wrapped.

    Returns:
        function: The wrapped function.
    """

    def wrapped(*args, **kwargs):
        if hasattr(wrapped, '_cached_val'):
            return wrapped._cached_val
        result = f(*args, **kwargs)
        wrapped._cached_val = result
        return result
    return wrapped


class LambdaBase(ABC):
    """Lambda Base for configuration and loggers."""

    def __init__(self, parameters=None):
        """Initialization of the Lambda Base.

        Args:
            parameters (:obj:`dict`, optional): Key/value pairs for saving configuration.
        """

        self._logger = logging.getLogger()
        self._logger.setLevel(os.environ.get('LOGGING_LEVEL', 'INFO'))
        self._parameters = parameters or {}

    @abstractmethod
    def handle(self, event, context) -> dict:
        """Abstract handle will be implemented as the method that is called by the lambda.
        Args:
            event (dict): The lambda event.
            context (object): The lambda context.

        Returns:
            dict: The dictionary returned by the lambda.

        """

        raise NotImplementedError

    @classmethod
    def get_handler(cls, *args, **kwargs):
        """Wraps the handler for the lambda.
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            function: The lambda function.
        """

        @memoize
        def init_handler(*args, **kwargs):
            return cls(*args, **kwargs)

        def handler(event, context):
            return init_handler(*args, **kwargs).handler(event, context)
        return handler

    def validate_event(self, event) -> None:
        """Validate method.
        Args:
            event (dict): lambda event.
        """

        pass

    def handler(self, event, context):
        """Handler method that wraps up handle, so all lambda can do something here.
        Args:
            event (dict): The lambda event.
            context (object): The lambda context.
        """

        self.validate_event(event)
        return self.handle(event, context)

    def get_parameter(self, key, default=None):
        """Used to get parameters from the lambda.
        Args:
            key (str): The name of the parameter.
            default (:obj, optional): Defautl value if key is not found.

        Returns:
            object: The value for this key.
        """

        if not default:
            return self._parameters[key]
        else:
            return self._parameters.get(key, default)
