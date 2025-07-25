from time import time

from . import auth_bp, logger

from flask import abort, request, redirect, url_for, session

from lib.sqlitedb import db, FETCH_ONE
from lib.hash import hash_password


def database_query(username):
    return db.execute(
        """
            SELECT *
            FROM users
            WHERE username = ?
        """,
        (username,),
        FETCH_ONE
    )


def database_insert(name, username, password, created_on):
    db.execute(
        """
            INSERT INTO users (name, username, password, created_on, status)
            VALUES (?, ?, ?, ?, ?)
        """,
        (name, username, password, created_on, True)
    )


@auth_bp.route("/register", methods=["POST"])
def user_register():
    try:
        username = session["username"]

        if username != "admin":
            raise KeyError("No Permission")

        name = request.form.get("name")
        username = request.form.get("email")

        result = database_query(username)
        if result:
            return redirect(url_for("home.home_page"))

        database_insert(
            name=name,
            username=username,
            password=hash_password(""),
            created_on=int(time())
        )

        return redirect(url_for("home.home_page"))

    except Exception as error:
        logger(error)
        abort(500)
