from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')
bp_login = Blueprint('login', __name__)

# import file with the api AT THE BOTTOM!!!!
from . import web_api