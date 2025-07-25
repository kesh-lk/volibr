from . import book_bp, logger

from flask import abort, session, request, Response
from bs4 import BeautifulSoup

from lib.sqlitedb import db, FETCH_ONE
from lib.convert import convert_pdf_to_html


def query_filename(book_id):
    return db.execute(
        """
            SELECT title, filename, page_count
            FROM books
            WHERE id = ?
        """,
        (book_id,),
        FETCH_ONE
    )


def query_progress(username, book_id):
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


@book_bp.route('/view', methods=["GET"])
def book_view():
    try:
        # PARSE
        username = session["username"]
        book_id = request.args.get("id")

        # DATABASE
        row = query_filename(book_id)
        title = dict(row)["title"]
        filename = dict(row)["filename"]
        page_count = dict(row)["page_count"]

        row = query_progress(username, book_id)
        page = 1
        if row:
            page = dict(row)["page"]

        # GENERATE PAGE
        convert_pdf_to_html(
            pdf_path=f"/storage/{filename}",
            page_from=int(page),
            page_to=int(page)
        )

        # PAGE CONTENT
        with open('/tmp/pdf.html') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')

        soup.title.string = title

        # HOVER
        # with open("static/js/hover.js", "r") as file:
        #     script = soup.new_tag("script")
        #     script.string = file.read()
        #     soup.body.append(script)

        # with open("static/css/hover.css", "r") as file:
        #     style = soup.new_tag("style", type="text/css")
        #     style.string = file.read()
        #     soup.head.append(style)

        with open("static/js/page.js", "r") as file:
            script = soup.new_tag("script")
            script.string = file.read()
            soup.body.append(script)

        # return Response(str(soup), mimetype="text/html")

        # PAGE CHANGE
        with open("static/css/page.css", "r") as file:
            style = soup.new_tag("style", type="text/css")
            style.string = file.read()
            soup.head.append(style)

        with open("static/css/button.css", "r") as file:
            style = soup.new_tag("style", type="text/css")
            style.string = file.read()
            soup.head.append(style)

        with open("templates/page.html", "r") as file:
            element_string = file.read()
            element = BeautifulSoup(element_string, "html.parser").div
            page_container = soup.find("div", id="page-container")
            page_body = page_container.find("div")
            page_body.append(element)

        # RENDER
        page_body.find(id="pageInput")["value"] = page
        page_body.find('span', id="pageCount").string = str(page_count)

        # EDIT
        outline = soup.find('div', id="outline")
        if outline:
            outline.clear()

        sidebar = soup.find("div", id="sidebar")
        sidebar["style"] = """
            display: none;
            background-color: transparent;
            background-image: none;
        """

        page_container = soup.find("div", id="page-container")
        page_container["style"] = """
            background-color: #1e1e1e;
            background-image: none;
        """

        return Response(str(soup), mimetype='text/html')

    except Exception as error:
        logger(error)
        abort(500)
