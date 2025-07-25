from . import auth_bp, logger

from flask import abort, request, redirect, url_for, session


@auth_bp.route("/logout", methods=["GET"])
def user_logout():
    try:
        username = session["username"]

        session.pop("username")
        return redirect(url_for("auth.user_login"))

    except KeyError as error:
        logger(error)
        return redirect(url_for("auth.user_login"))

    except Exception as error:
        logger(error)
        abort(500)
