from flask import (Blueprint, current_app)

auth_bp = Blueprint('auth', __name__)


# LOGGING
def logger(data):
    current_app.logger.info(data)


from . import login
from . import logout
from . import register
from . import status
from . import profile
from . import password
