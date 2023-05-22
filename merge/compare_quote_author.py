import json
from quotes import quotes
from book_and_quote_author import authors

# prepare CSV
file = "merge_quote_and_author.csv"
header = "id, author_id, quote, tags \n"
f = open(file, "w", encoding="utf-8")
f.write(header)

quote_author = []

for quote in quotes:
    print(quote["name"])
    for author in authors:
        if (quote["name"].lower() == author["name"].lower()):
            quote_author.append({
                "id": quote["id"],
                "author_id": author["id"],
                "quote": quote["quote"],
                "tags": quote["tags"]
            })
            f.write(str(quote["id"]) + ", " +
                    str(author["id"]) + ", " +
                    str(quote["quote"]).replace(',','*') + ", " +
                    str(quote["tags"]).replace(',','*') + 
                    "\n")

with open("merge_quote_and_author.json", "w") as outfile:
    json.dump(quote_author, outfile)

for item in quote_author:
    print(item["id"])
    print(item["author_id"])
    print("\n")

f.close()
