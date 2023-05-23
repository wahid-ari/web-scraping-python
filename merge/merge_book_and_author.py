import json
from books import books
from book_and_quote_author import authors

# prepare CSV
path = "merge/merge_book_and_author"
# header = "id, author_id, title, isbn, language, pages, published, genre, rating, score, vote, link, image, image_small, description, genre_array \n"
# f = open(f'{path}{".csv"}', "w", encoding="utf-8")
# f.write(header)

book_author = []

for book in books:
    for author in authors:
        if (book["author"].lower() == author["name"].lower()):
            # remove space between each string (a, b) > (a,b)
            # finally split by comma to make list (a,b) > ([a,b])
            genre_array = book["genre"].replace(', ', ',').split(',')
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
                "description": book["description"],
                "genre_array": genre_array,
            })
            # f.write(str(book["id"]) + ", " +
            #         str(author["id"]) + ", " +
            #         str(book["title"]) + ", " +
            #         str(book["isbn"]) + ", " +
            #         str(book["language"]) + ", " +
            #         str(book["pages"]) + ", " +
            #         str(book["published"]) + ", " +
            #         str(book["genre"]).replace(',','*') + ", " +
            #         str(book["rating"]) + ", " +
            #         str(book["score"]) + ", " +
            #         str(book["vote"]) + ", " +
            #         str(book["link"]) + ", " +
            #         str(book["image"]) + ", " +
            #         str(book["image_small"]) + ", " +
            #         str(book["description"]).replace(',', '*') + ", " +
            #         "\n")

with open(f'{path}{".json"}', "w") as outfile:
    json.dump(book_author, outfile, indent=4)

for item in book_author:
    print(item["id"])
    print(item["author_id"])
    print(item["title"])
    print("\n")

# f.close()
