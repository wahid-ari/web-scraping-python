import json
from quotes import quotes
from book_and_quote_author import authors

# prepare CSV
path = "merge/merge_quote_and_author"
# header = "id, author_id, quote, tags \n"
# f = open(f'{path}{".csv"}', "w", encoding="utf-8")
# f.write(header)

quote_author = []

for quote in quotes:
    print(quote["name"])
    for author in authors:
        if (quote["name"].lower() == author["name"].lower()):
            # first, remove last comma in tags string (a, b,) > (a, b)
            # then remove space between each string (a, b) > (a,b)
            # finally split by comma to make list (a,b) > ([a,b])
            tags_array = quote["tags"][:-1].replace(' ', '').split(',')
            quote_author.append({
                "id": quote["id"],
                "author_id": author["id"],
                "quote": quote["quote"],
                "tags": quote["tags"],
                "tags_array": tags_array
            })
            # f.write(str(quote["id"]) + ", " +
            #         str(author["id"]) + ", " +
            #         str(quote["quote"]).replace(',', '*') + ", " +
            #         str(quote["tags"]).replace(',', '*') +
            #         "\n")

with open(f'{path}{".json"}', "w") as outfile:
    json.dump(quote_author, outfile, indent=4)

for item in quote_author:
    print(item["id"])
    print(item["author_id"])
    print("\n")

# f.close()
