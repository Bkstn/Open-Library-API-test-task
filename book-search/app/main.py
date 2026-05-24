import math
import requests
from flask import Flask, request, render_template, session, redirect, url_for
from utilities import create_book_from_openlibrary_json

app = Flask(__name__)
app.secret_key = "dev-secret-key"


@app.get("/")
def home():
    return render_template("index.html", books=None)


@app.get("/search")
def search_books():
    title = request.args.get("title", "")
    page = request.args.get("page", 1, type=int)

    if page < 1:
        page = 1

    if not title:
        return render_template(
            "index.html",
            books=[],
            search_title=title,
            page=1,
            total_pages=0,
            total_results=0
        )
    
    limit = 10

    response = requests.get(
        "https://openlibrary.org/search.json",
        params={
            "title": title,
            "limit": limit,
            "page": page,
            "fields": "key,title,author_name,first_publish_year,isbn,cover_i"
        },
        headers={
            "User-Agent": "MyBookApp (you@example.com)"
        },
        timeout=10
    )

    response.raise_for_status()
    data = response.json()

    books = []

    for book_json in data["docs"]:
        book = create_book_from_openlibrary_json(book_json)
        books.append(book)

    total_results = data.get("numFound", data.get("num_found", 0))
    total_pages = math.ceil(total_results / limit)

    return render_template(
        "index.html",
        books=books,
        search_title=title,
        page=page,
        total_pages=total_pages,
        total_results=total_results
    )

@app.get("/book/<path:book_key>")
def book_detail(book_key):
    work_response = requests.get(
        f"https://openlibrary.org/{book_key}.json",
        headers={
            "User-Agent": "MyBookApp (you@example.com)"
        },
        timeout=10
    )

    work_response.raise_for_status()
    work_data = work_response.json()

    editions_response = requests.get(
        f"https://openlibrary.org/{book_key}/editions.json",
        params={
            "limit": 20
        },
        headers={
            "User-Agent": "MyBookApp (you@example.com)"
        },
        timeout=10
    )

    editions_response.raise_for_status()
    editions_data = editions_response.json()
    name = work_data.get("title", "Unknown title")
    publicationDate = work_data.get("first_publish_date")
    description_data = work_data.get("description")

    if isinstance(description_data, dict):
        description = description_data.get("value")
    else:
        description = description_data

    authors = []

    for author_item in work_data.get("authors", []):
        author_key = author_item.get("author", {}).get("key")

        if author_key:
            author_response = requests.get(
                f"https://openlibrary.org{author_key}.json",
                headers={
                    "User-Agent": "MyBookApp (you@example.com)"
                },
                timeout=10
            )

            if author_response.status_code == 200:
                author_data = author_response.json()
                author_name = author_data.get("name")

                if author_name:
                    authors.append(author_name)

    ISBN = None
    cover_page = None

    for edition in editions_data.get("entries", []):
        isbn_13 = edition.get("isbn_13", [])
        isbn_10 = edition.get("isbn_10", [])

        if not ISBN:
            if isbn_13:
                ISBN = isbn_13[0]
            elif isbn_10:
                ISBN = isbn_10[0]

        covers = edition.get("covers", [])

        if not cover_page and covers:
            cover_page = f"https://covers.openlibrary.org/b/id/{covers[0]}-L.jpg"

        if ISBN and cover_page:
            break

    work_covers = work_data.get("covers", [])

    if work_covers:
        cover_page = f"https://covers.openlibrary.org/b/id/{work_covers[0]}-L.jpg"

    openlibrary_url = f"https://openlibrary.org/{book_key}"

    book = {
        "name": name,
        "authors": authors,
        "publicationDate": publicationDate,
        "ISBN": ISBN,
        "cover_page": cover_page,
        "description": description,
        "url": openlibrary_url,
        "openlibrary_key": book_key
    }

    return render_template("book_detail.html", book=book)

@app.post("/favorites/add/<path:book_key>")
def add_favorite(book_key):
    favorites = session.get("favorites", [])

    openlibrary_url = f"https://openlibrary.org/{book_key}"

    # Do not add the same book twice
    for favorite in favorites:
        if favorite.get("openlibrary_key") == book_key:
            return redirect(request.referrer or url_for("favorites"))

    work_response = requests.get(
        f"https://openlibrary.org/{book_key}.json",
        headers={
            "User-Agent": "MyBookApp (you@example.com)"
        },
        timeout=10
    )

    work_response.raise_for_status()
    work_data = work_response.json()

    name = work_data.get("title", "Unknown title")
    publicationDate = work_data.get("first_publish_date")

    description_data = work_data.get("description")

    if isinstance(description_data, dict):
        description = description_data.get("value")
    else:
        description = description_data

    authors = []

    for author_item in work_data.get("authors", []):
        author_key = author_item.get("author", {}).get("key")

        if author_key:
            author_response = requests.get(
                f"https://openlibrary.org{author_key}.json",
                headers={
                    "User-Agent": "MyBookApp (you@example.com)"
                },
                timeout=10
            )

            if author_response.status_code == 200:
                author_data = author_response.json()
                author_name = author_data.get("name")

                if author_name:
                    authors.append(author_name)

    cover_page = None
    work_covers = work_data.get("covers", [])

    if work_covers:
        cover_page = f"https://covers.openlibrary.org/b/id/{work_covers[0]}-M.jpg"

    book = {
        "name": name,
        "authors": authors,
        "publicationDate": publicationDate,
        "ISBN": None,
        "cover_page": cover_page,
        "description": description,
        "url": openlibrary_url,
        "openlibrary_key": book_key
    }

    favorites.append(book)
    session["favorites"] = favorites

    return redirect(request.referrer or url_for("favorites"))


@app.post("/favorites/remove/<path:book_key>")
def remove_favorite(book_key):
    favorites = session.get("favorites", [])

    updated_favorites = []

    for favorite in favorites:
        if favorite.get("openlibrary_key") != book_key:
            updated_favorites.append(favorite)

    session["favorites"] = updated_favorites

    return redirect(request.referrer or url_for("favorites"))


@app.get("/favorites")
def favorites():
    favorites = session.get("favorites", [])
    return render_template("favorites.html", favorites=favorites)

if __name__ == "__main__":
    app.run(debug=True)