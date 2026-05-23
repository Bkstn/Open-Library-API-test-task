import datetime

class Book:
    def __init__(
        self,
        name,
        authors,
        publicationDate=None,
        ISBN=None,
        cover_page=None,
        description=None,
        url=None,
        openlibrary_key=None
    ):
        self.name = name
        self.authors = authors
        self.publicationDate = publicationDate
        self.ISBN = ISBN
        self.cover_page = cover_page
        self.description = description
        self.url = url
        self.openlibrary_key = openlibrary_key
