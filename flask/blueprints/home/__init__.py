from flask import (Blueprint, current_app)

home_bp = Blueprint('home', __name__)


# LOGGING
def logger(data):
    current_app.logger.info(data)


from . import main
