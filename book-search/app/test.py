import requests

url = "https://openlibrary.org/search.json"

params = {
    "title": "the hobbit",
    "limit": 5,
    "fields" : "key,title, author_name, first_publish_year, edition_count, isbn"
}

headers = {
    "User-Agent": "MyBookApp (you@example.com)"
}

response = requests.get(url, params=params, headers=headers)
response.raise_for_status()


data = response.json()

for book in data["docs"]:
    for element in book:
        print(element +": ", book.get(element))
    print("---")