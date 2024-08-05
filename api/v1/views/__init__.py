#!/usr/bin/python3
"""

"""
from Flask import register_blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *