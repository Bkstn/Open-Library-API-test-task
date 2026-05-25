# Open-Library-API-test-task

This test Web service is made to fetch information (books and their editions) from Open Library, using Open Library API, format and display it and allow user to add it to their list of favorites.

Key features:

- Searching books by title
- Detailed book information page
- Adding books to "favorites"
- Search history
- Visited book's page history
- API responses caching

Technologies and tools used:

Backend: Python 3, Flask library
API: Open Library API
Frontend: JavaScript, Jinja templates, CSS

How to start:
1. Clone the repository (https://github.com/Bkstn/Open-Library-API-test-task)
cd book-search or click on the folder.

2. Create virtual environment

python -m venv venv
venv\Scripts\activate if Windows
#source venv/bin/active if macOS/Linux 

2. Install the needed dependency:

pip install -r requirements.txt

3. Open main.py file and run it. In terminal output, click on a given link (http://127.0.0.1:5000).


Project structure:

Open-Library-API-test-task/
├── book-search/
    ├──app/
        ├── __pycache__
        ├── static/
        |   ├── base.css
        |   ├── book_detail.css
        |   ├── favorites.css
        |   ├── favorites.js
        |   ├── history.css
        |   ├── history.js
        |   ├── index.css
        ├── templates/
        |   ├── book_detail.html
        |   |── favorites.html
        |   ├── history.html
        |   ├── index.html
        ├── book.py
        ├── main.py
        ├── utilities.py
        ├── requirements.txt
    ├── README.md