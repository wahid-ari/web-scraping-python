import json
from file_merge_quote_and_author import quotes
from tags import tags

# prepare CSV
path = "merge/merge_quote_and_tags"
# header = "id, quote_id, tags_id \n"
# f = open(f'{path}{".csv"}', "w", encoding="utf-8")
# f.write(header)

quote_tags = []

index = 1
for quote in quotes:
    # print(index)
    # print(quote["id"])
    for a in quote["tags_array"]:
        # print(a)
        for tag in tags:
            if (a.lower() == tag["name"].lower()):
                quote_tags.append({
                    "id": index,
                    "quote_id": quote["id"],
                    "tags_id": tag["id"]
                })
                index = index + 1
    # print("\n")

with open(f'{path}{".json"}', "w") as outfile:
    json.dump(quote_tags, outfile, indent=4)

for item in quote_tags:
    print(item["id"])
    print(item["quote_id"])
    print(item["tags_id"])
    print("\n")

# f.close()
