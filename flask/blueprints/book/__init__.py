from flask import (Blueprint, current_app)

book_bp = Blueprint('book', __name__)


# LOGGING
def logger(data):
    current_app.logger.info(data)


from . import search
from . import upload
from . import cover
from . import download
from . import delete
from . import view
from . import flip
from . import genre
