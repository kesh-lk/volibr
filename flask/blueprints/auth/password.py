from . import auth_bp, logger

from flask import abort, request, redirect, url_for, session

from lib.sqlitedb import db, FETCH_ONE
from lib.hash import hash_password, check_password


def database_query(username):
    return db.execute(
        """
            SELECT password
            FROM users
            WHERE username = ?
        """,
        (username,),
        FETCH_ONE
    )


def database_update(username, password):
    db.execute(
        """
            UPDATE users
            SET password = ?
            WHERE username = ?
        """,
        (password, username)
    )


@auth_bp.route("/password", methods=["POST"])
def user_password():
    try:
        # PARSE
        username = session["username"]

        current_password = request.form.get("current-password")
        new_password = request.form.get("new-password")

        # DATABASE QUERY
        row = database_query(username)
        saved_hash = dict(row)["password"]

        # CHECK
        if not check_password(current_password, saved_hash):
            raise KeyError("Invalid Password")

        # HASH
        new_hash = hash_password(new_password)

        # DATABASE UPDATE
        database_update(username, new_hash)

        return redirect(url_for("home.home_page"))

    except Exception as error:
        logger(error)
        abort(500)
