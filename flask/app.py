import secrets
from datetime import datetime

from flask import Flask, url_for
from flask_session import Session

from lib.sqlitedb import db

from blueprints.home import home_bp
from blueprints.auth import auth_bp
from blueprints.book import book_bp

# FLASK
app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/'
)
app.secret_key = secrets.token_hex(32)
app.debug = True
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

# FLASK SESSIONS
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# DATABASE
db.set_config("db.sql")
db.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_on INTEGER,
        last_active INTEGER,
        password_changed INTEGER,
        status INTEGER
    );
    """
)
db.execute(
    """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        year INTEGER,
        author TEXT,
        genre TEXT,
        user_id INTEGER NOT NULL,
        is_private INTEGER,
        filename TEXT,
        page_count INTEGER
    )
    """
)
db.execute(
    """
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        page INTEGER NOT NULL
    )
    """
)

# BLUEPRINTS
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(book_bp, url_prefix="/book")


# LOGGING
def logger(data):
    app.logger.info(data)


@app.template_filter('datetime')
def datetime_filter(epoch):
    if not epoch:
        return "Nil"
    return datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')


@app.route("/favicon.ico")
def favicon():
    return url_for('static', filename='data:,')


# Execute Flask App
if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
