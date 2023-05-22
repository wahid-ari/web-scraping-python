import json
from books import books
from book_and_quote_author import authors

# prepare CSV
file = "merge_book_and_author.csv"
header = "id, author_id, title, isbn, language, pages, published, genre, rating, score, vote, link, image, image_small, description \n"
f = open(file, "w", encoding="utf-8")
f.write(header)

book_author = []

for book in books:
    for author in authors:
        if (book["author"].lower() == author["name"].lower()):
            book_author.append({
                "id": book["id"],
                "author_id": author["id"],
                "title": book["title"],
                "isbn": book["isbn"],
                "language": book["language"],
                "pages": book["pages"],
                "published": book["published"],
                "genre": book["genre"],
                "rating": book["rating"],
                "score": book["score"],
                "vote": book["vote"],
                "link": book["link"],
                "image": book["image"],
                "image_small": book["image_small"],
                "description": book["description"]
            })
            f.write(str(book["id"]) + ", " +
                    str(author["id"]) + ", " +
                    str(book["title"]) + ", " +
                    str(book["isbn"]) + ", " +
                    str(book["language"]) + ", " +
                    str(book["pages"]) + ", " +
                    str(book["published"]) + ", " +
                    str(book["genre"]).replace(',','*') + ", " +
                    str(book["rating"]) + ", " +
                    str(book["score"]) + ", " +
                    str(book["vote"]) + ", " +
                    str(book["link"]) + ", " +
                    str(book["image"]) + ", " +
                    str(book["image_small"]) + ", " +
                    str(book["description"]).replace(',', '*') + ", " +
                    "\n")

with open("merge_book_and_author.json", "w") as outfile:
    json.dump(book_author, outfile)

for item in book_author:
    print(item["id"])
    print(item["author_id"])
    print(item["title"])
    print("\n")

f.close()
