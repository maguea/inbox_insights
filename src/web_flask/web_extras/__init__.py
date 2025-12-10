# __init__.py Tolu Kolade Nov 25, 2025
# This is to add the blueprints and imports the file
# 

from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')
bp_login = Blueprint('login', __name__)

# import file with the blueprint AT THE BOTTOM!!!!
from . import web_api
from . import web_login