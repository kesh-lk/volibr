from . import auth_bp, logger
from time import time

from flask import abort, request, render_template, redirect, url_for, session

from lib.sqlitedb import db, FETCH_ONE
from lib.hash import hash_password, check_password


def database_query(username):
    return db.execute(
        """
            SELECT id, password, status
            FROM users
            WHERE username = ?
        """,
        (username,),
        FETCH_ONE
    )


def default_admin(password_hash):
    db.execute(
        """
            INSERT INTO users (username, password, status)
            VALUES (?, ?, ?);
        """,
        ("admin", password_hash, True)
    )


def database_update(username, last_active):
    db.execute(
        """
            UPDATE users
            SET last_active = ?
            WHERE username = ?
        """,
        (last_active, username)
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def user_login():
    try:
        if request.method == "GET":
            return render_template("login.html")

        elif request.method == "POST":
            # PARSE
            username = request.form["email"]
            password = request.form["password"]

            # DATABASE QUERY
            query = database_query(username)

            # DEFAULT ADMIN
            if username == "admin" and query is None:
                password_hash = hash_password("admin")
                default_admin(password_hash)
                session["username"] = username
                return redirect(url_for("home.home_page"))

            # QUERY CHECK
            if not query:
                return render_template("login.html", auth_error=True)

            # PROCESS
            user_data = dict(query)
            if not user_data["status"]:
                return render_template("login.html", disabled=True)

            if check_password("", user_data["password"]):
                session["username"] = username
                return render_template("onboard.html")

            if check_password(password, user_data["password"]):
                session["username"] = username

                database_update(username, int(time()))
                return redirect(url_for("home.home_page"))

            return render_template("login.html", auth_error=True)

    except Exception as error:
        logger(error)
        abort(500)
