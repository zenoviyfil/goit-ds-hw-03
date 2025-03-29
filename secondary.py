import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient

BASE_URL = "http://quotes.toscrape.com"

client: MongoClient = MongoClient(
    "mongodb+srv://filzenoviy:e3SJs6CErAZbRwMy@cluster0.hyrtfpe.mongodb.net/"
)

authors_db = client["authors_db"]
authors_collection = authors_db["authors"]

quotes_db = client["quotes_db"]
quotes_collection = quotes_db["quotes"]


def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def scrape_quotes():
    quotes_list = []
    authors_set = {}
    page = 1

    while True:
        soup = get_soup(f"{BASE_URL}/page/{page}/")
        quotes = soup.select(".quote")

        if not quotes:
            break

        for quote in quotes:
            text = quote.select_one(".text").get_text(strip=True)
            author = quote.select_one(".author").get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.select(".tags .tag")]

            quotes_list.append({"tags": tags, "author": author, "quote": text})

            if author not in authors_set:
                author_url = BASE_URL + quote.select_one(".author + a")["href"]
                authors_set[author] = author_url

        page += 1

    return quotes_list, authors_set


def scrape_authors(authors_set):
    authors_list = []
    for name, url in authors_set.items():
        soup = get_soup(url)
        born_date = soup.select_one(".author-born-date").get_text(strip=True)
        born_location = soup.select_one(".author-born-location").get_text(strip=True)
        description = soup.select_one(".author-description").get_text(strip=True)

        authors_list.append(
            {
                "fullname": name,
                "born_date": born_date,
                "born_location": born_location,
                "description": description,
            }
        )

    return authors_list


def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_to_mongo(collection, data):
    if data:
        collection.insert_many(data)
        print(f"Додано {len(data)} записів у {collection.name}")


def main():
    quotes, authors_set = scrape_quotes()
    authors = scrape_authors(authors_set)

    save_json(quotes, "quotes.json")
    save_json(authors, "authors.json")
    print("Дані збережено у quotes.json та authors.json")

    save_to_mongo(authors_collection, authors)
    save_to_mongo(quotes_collection, quotes)
    print("Дані збережено у MongoDB")


if __name__ == "__main__":
    main()
