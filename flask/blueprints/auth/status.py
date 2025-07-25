from . import auth_bp, logger

from flask import abort, request, redirect, url_for, session

from lib.sqlitedb import db


def database_update(status, username):
    db.execute(
        """
            UPDATE users
            SET status = ?
            WHERE username = ?
        """,
        (status, username)
    )


@auth_bp.route("/status", methods=["POST"])
def user_status():
    try:
        username = session["username"]

        if username != "admin":
            KeyError("No Permission")

        set_username = request.form.get("username")
        set_status = int(request.form.get("status"))
        set_status = 0 if set_status else 1

        database_update(
            status=set_status,
            username=set_username
        )

        return redirect(url_for("home.home_page"))

    except Exception as error:
        logger(error)
        abort(500)
