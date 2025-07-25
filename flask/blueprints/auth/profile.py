from . import auth_bp, logger

from flask import (abort, request, redirect,
                   url_for, session, jsonify)

from lib.sqlitedb import db, FETCH_ONE


def database_query(username):
    return db.execute(
        """
            SELECT name
            FROM users
            WHERE username = ?
        """,
        (username,),
        FETCH_ONE
    )


def database_update(update_name, update_username, username):
    db.execute(
        """
            UPDATE users
            SET name = ?, username = ?
            WHERE username = ?
        """,
        (update_name, update_username, username)
    )


@auth_bp.route("/profile", methods=["GET", "POST"])
def user_profile():
    try:
        if request.method == "GET":
            # PARSE
            username = session["username"]

            # DATABASE
            row = database_query(username)
            name = dict(row)["name"]

            data = {
                "name": name,
                "email": username
            }
            return jsonify(data)

        else:
            # PARSE
            username = session["username"]

            new_name = request.form.get("name")
            new_username = request.form.get("email")

            # DATABASE QUERY
            row = database_query(username)
            name = dict(row)["name"]

            # USERNAME CHECK
            if new_username != username:
                result = database_query(new_username)
                if result:
                    return redirect(url_for("home.home_page"))

            # PROCESS
            update_name = name if name == new_name else new_name
            update_username = username if username == new_username else new_username

            # DATABASE UPDATE
            database_update(update_name, update_username, username)

            # UPDATE SESSIONS
            session["username"] = update_username

            return redirect(url_for("home.home_page"))

    except Exception as error:
        logger(error)
        abort(500)
