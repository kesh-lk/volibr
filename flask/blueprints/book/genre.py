from . import book_bp, logger

from flask import abort, jsonify


@book_bp.route("/genre", methods=["GET"])
def book_genre():
    try:
        genres = [
            "Fantasy",
            "Science Fiction",
            "Horror",
            "Mystery",
            "Thriller",
            "Romance",
            "Young Adult",
            "Children’s",
            "Historical Fiction",
            "Literary Fiction",
            "Action & Adventure",
            "Biography & Memoir",
            "History",
            "Self-Help",
            "Psychology",
            "Business & Economics",
            "Religion & Spirituality",
            "Science & Nature",
            "Travel",
            "Cookbooks",
            "Art & Photography",
            "Politics & Social Sciences",
            "Education & Reference"
        ]

        return jsonify(genres)
    except Exception as error:
        logger(error)
        abort(500)
