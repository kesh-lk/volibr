from . import home_bp, logger

from flask import abort, render_template, session, redirect, url_for

from lib.sqlitedb import db, FETCH_ALL


def users_query():
    return db.execute(
        """
            SELECT name, username, created_on, last_active, status
            FROM users
            WHERE username != 'admin'
        """,
        (),
        FETCH_ALL
    )


@home_bp.route("/", methods=["GET"])
def home_page():
    try:
        username = session["username"]

        if username == "admin":

            rows = users_query()
            users = [dict(row) for row in rows]
            logger(users)

            return render_template("admin.html", users=users)
        else:

            return render_template("home.html")

    except KeyError as error:
        logger(error)
        return redirect(url_for("auth.user_login"))

    except Exception as error:
        logger(error)
        abort(500)
