import datetime

class Book:
    name =""
    ISBN = ""
    authors = []
    publicationDate = ""
    cover_page = ""
    description = ""
    url = ""

    def __init__(self, name, authors, publicatonDate = None, ISBN = None, cover_page = None, description = None, url = None):
        self.name = name
        self.authors = authors
        self.publicationDate = publicatonDate
        self.ISBN = ISBN
        self.cover_page = cover_page
        self.description = description
        self.url = url
