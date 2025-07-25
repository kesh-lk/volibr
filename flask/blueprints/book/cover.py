from . import book_bp, logger
from io import BytesIO

from flask import abort, send_file, request
from pdf2image import convert_from_path

from lib.sqlitedb import db, FETCH_ONE


def database_query(book_id):
    return db.execute(
        """
            SELECT filename
            FROM books
            WHERE id = ?
        """,
        (book_id),
        FETCH_ONE
    )


@book_bp.route("/cover", methods=["GET"])
def book_cover():
    try:
        # PARSE
        book_id = request.args.get("id")

        # DATABASE
        row = database_query(book_id)
        filename = dict(row)["filename"]

        # CONVERT
        images = convert_from_path(f"/storage/{filename}", first_page=1, last_page=1)
        img = images[0]

        # Save image to a BytesIO stream
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        # Return image directly as response
        return send_file(img_io, mimetype='image/png')

    except Exception as error:
        logger(error)
        abort(500)
