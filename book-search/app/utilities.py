import book

def create_book_from_openlibrary_json(book_json):
    name = book_json.get("title", "Unknown title")

    authors = book_json.get("author_name", [])

    publicationDate = book_json.get("first_publish_year")

    isbn_list = book_json.get("isbn", [])
    ISBN = isbn_list[0] if isbn_list else None

    cover_id = book_json.get("cover_i")
    if cover_id:
        cover_page = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
    else:
        cover_page = None

    key = book_json.get("key")
    if key:
        url = f"https://openlibrary.org{key}"
    else:
        url = None

    description = None

    return Book(
        name=name,
        authors=authors,
        publicationDate=publicationDate,
        ISBN=ISBN,
        cover_page=cover_page,
        description=description,
        url=url
    )