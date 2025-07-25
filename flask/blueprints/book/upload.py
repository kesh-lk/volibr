from . import book_bp, logger
import json
import os

from flask import abort, session, redirect, url_for, request
from PyPDF2 import PdfReader

from lib.sqlitedb import db


def database_insert(title, author, year, genre, username, is_private, filename, page_count):
    db.execute(
        """
        INSERT INTO books (title, author, year, genre, is_private, filename, user_id, page_count)
        VALUES (
            ?, ?, ?, ?, ?, ?,
            (SELECT id FROM users WHERE username = ?),
            ?
        )
        """,
        (title, author, year, genre, is_private, filename, username, page_count)
    )


@book_bp.route("/upload", methods=["POST"])
def book_upload():
    try:
        username = session["username"]

        # PARSE
        title = request.form.get("title")
        author = request.form.get("author")
        year = request.form.get("year")
        genre = request.form.get("genre").split(",")
        is_private = request.form.get("is-private")

        uploaded_file = request.files.get("book_file")

        # SAVE FILE
        if uploaded_file and uploaded_file.filename != "":
            save_path = os.path.join("/storage", uploaded_file.filename)
            uploaded_file.save(save_path)

        # PDF PAGE COUNT
        reader = PdfReader(f"/storage/{uploaded_file.filename}")
        page_count = len(reader.pages)

        # DATABASE
        database_insert(
            title=title,
            author=author,
            year=year,
            genre=json.dumps(genre),
            username=username,
            is_private=True if is_private == "on" else False,
            filename=uploaded_file.filename,
            page_count=page_count
        )

        return redirect(url_for("home.home_page"))
    except Exception as error:
        logger(error)
        abort(500)
