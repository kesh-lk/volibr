from . import book_bp, logger

from flask import abort, session, send_file, request

from lib.sqlitedb import db, FETCH_ONE


def database_query(book_id):
    return db.execute(
        """
            SELECT books.filename, users.username, books.is_private
            FROM books
            JOIN users
                ON users.id == books.user_id
            WHERE books.id = ?
        """,
        (book_id,),
        FETCH_ONE
    )


@book_bp.route("/download", methods=["GET"])
def book_download():
    try:
        # PARSE
        username = session["username"]

        book_id = request.args.get("id")

        # DATABASE
        row = database_query(book_id)
        data = dict(row)
        filename = data["filename"]
        saved_username = data["username"]
        is_private = data["is_private"]

        # CHECK PERMISSIONS
        if is_private and username != saved_username:
            abort(500)

        return send_file(f"/storage/{filename}", as_attachment=True)
    except Exception as error:
        logger(error)
        abort(500)
