from . import book_bp, logger

from flask import abort, request, session

from lib.sqlitedb import db, FETCH_ONE


def database_query(username, book_id):
    return db.execute(
        """
            SELECT page
            FROM progress
            WHERE user_id = (SELECT id FROM users WHERE username = ?)
                AND book_id = ?
        """,
        (username, book_id),
        FETCH_ONE
    )


def database_insert(username, book_id, page):
    db.execute(
        """
            INSERT INTO progress (user_id, book_id, page)
            VALUES (
                (SELECT id FROM users WHERE username = ?),
                ?, ?
            )
        """,
        (username, book_id, page)
    )


def database_amend(username, book_id, page):
    db.execute(
        """
            UPDATE progress
            SET page = ?
            WHERE user_id = (SELECT id FROM users WHERE username = ?)
                AND book_id = ?
        """,
        (page, username, book_id)
    )


@book_bp.route("/flip", methods=["POST"])
def book_flip():
    try:
        # PARSE
        username = session["username"]

        book_id = request.json["id"]
        direction = request.json["d"]

        # DATABASE
        row = database_query(username, book_id)

        if not row:
            page = 2
            database_insert(username, book_id, page)

        else:
            page = dict(row)["page"]
            if direction == "next":
                page = page + 1
            elif direction == "prev":
                page = page - 1
            else:
                page = direction
            database_amend(username, book_id, page)

        return "", 200
    except Exception as error:
        logger(error)
        abort(500)
