import requests

url = "https://openlibrary.org/search.json"

params = {
    "title": "the hobbit",
    "limit": 5,
}

headers = {
    "User-Agent": "MyBookApp (you@example.com)"
}

response = requests.get(url, params=params, headers=headers)
response.raise_for_status()

data = response.json()

for book in data["docs"]:
    print(book.get("title"))
    print(book.get("author_name", ["Unknown author"])[0])
    print(book.get("first_publish_year"))
    print("---")