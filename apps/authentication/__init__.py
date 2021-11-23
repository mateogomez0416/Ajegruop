# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint

blueprint = Blueprint(
    'authentication_blueprint',
    __name__,template_folder='templates',
    url_prefix=''
)

from . import routes
