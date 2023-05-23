import json
from file_merge_book_and_author import books
from genre import genres

# prepare CSV
path = "merge/merge_book_and_genre"
# header = "id, quote_id, tags_id \n"
# f = open(f'{path}{".csv"}', "w", encoding="utf-8")
# f.write(header)

book_genre = []

index = 1
for book in books:
    # print(index)
    # print(book["id"])
    for a in book["genre_array"]:
        # print(a)
        for genre in genres:
            if (a.lower() == genre["name"].lower()):
                book_genre.append({
                    "id": index,
                    "book_id": book["id"],
                    "genre_id": genre["id"]
                })
                index = index + 1
    # print("\n")

with open(f'{path}{".json"}', "w") as outfile:
    json.dump(book_genre, outfile, indent=4)

for item in book_genre:
    print(item["id"])
    print(item["book_id"])
    print(item["genre_id"])
    print("\n")

# f.close()
