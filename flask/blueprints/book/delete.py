from . import book_bp, logger
import os

from flask import abort, session, request

from lib.sqlitedb import db, FETCH_ONE


def database_query(book_id):
    return db.execute(
        """
            SELECT users.username
            FROM books
            JOIN users
                ON users.id = books.user_id
            WHERE books.id = ?
        """,
        (book_id,),
        FETCH_ONE
    )


def database_delete(book_id):
    return db.execute(
        """
            DELETE FROM books
            WHERE id = ?
            RETURNING *
        """,
        (book_id,),
        FETCH_ONE
    )


@book_bp.route("/delete", methods=["POST"])
def book_delete():
    try:
        # PARSE
        username = session["username"]
        book_id = request.json["id"]

        # DATABASE QUERY
        row = database_query(book_id)
        query_username = dict(row)["username"]
        if username != query_username:
            abort(500)

        # DATABASE DELETE
        row = database_delete(book_id)
        filename = dict(row)["filename"]

        # STORAGE
        os.remove(f"/storage/{filename}")

        return "", 200
    except Exception as error:
        logger(error)
        abort(500)
