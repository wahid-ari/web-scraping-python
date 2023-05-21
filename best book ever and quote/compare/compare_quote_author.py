from quotes import quotes
from quotes_authors import authors

# prepare CSV
file = "merge_quote_and_author.csv"
header = "id, quote_id, author_id \n"
f = open(file, "w", encoding="utf-8")
f.write(header)

quote_author = []

index = 1
for quote in quotes:
    print(quote["name"])
    for author in authors:
        if (quote["name"].lower() == author["name"].lower()):
            quote_author.append({
                "id": index,
                "quote_id": quote["id"],
                "author_id": author["id"],
            })
            f.write(str(index) + ", " +
                    str(quote["id"]) + ", " +
                    str(author["id"]) +
                    "\n")
            index = index + 1

for item in quote_author:
    print(item["id"])
    print(item["quote_id"])
    print(item["author_id"])
    print("\n")

f.close()
