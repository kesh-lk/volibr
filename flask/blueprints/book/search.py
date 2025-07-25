from . import book_bp, logger
import json

from flask import abort, jsonify, session, request
from rapidfuzz import fuzz

from lib.sqlitedb import db, FETCH_ALL


def books_query(username):
    return db.execute(
        """
            SELECT books.id, books.title, books.author, books.genre, books.page_count, books.is_private, progress.page, users.username
            FROM books
            LEFT JOIN progress
                ON books.id = progress.book_id
            JOIN users
                ON users.id = books.user_id
        """,
        (),
        FETCH_ALL
    )


@book_bp.route("/search", methods=["GET"])
def book_search():
    try:
        # PARSE
        username = session["username"]

        search_value = request.args.get("search")
        search_genre = request.args.get("genre")

        # DATABASE
        rows = books_query(username)
        saved_books = [dict(row) for row in rows]

        # FUZZY SEARCH
        for book in saved_books:
            score = fuzz.ratio(
                search_value.lower(),
                book["title"].lower()
            )
            book["score"] = score

        # PROCESS
        processed_books = []
        for book in saved_books:
            book_data = {}
            book_data["owner"] = True if username == book["username"] else False
            book_data["id"] = book["id"]
            book_data["title"] = book["title"]
            book_data["author"] = book["author"]
            book_data["page_count"] = book["page_count"]
            book_data["page"] = book["page"]

            if book["is_private"] and not book_data["owner"]:
                continue

            if search_genre not in json.loads(book["genre"]) and search_genre != "":
                continue

            if search_value != "" and book["score"] < 20:
                continue

            processed_books.append(book_data)

        return jsonify(processed_books)
    except Exception as error:
        logger(error)
        abort(500)
