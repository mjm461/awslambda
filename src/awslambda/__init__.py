# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound

from .lambda_base import LambdaBase
from .lambda_base_ssm import LambdaBaseSsm
from .lambda_base_env import LambdaBaseEnv
from .clients import Clients
