import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
my_url = 'https://www.goodreads.com/genres?ref=nav_brws_genres'

# opening dan connection to website
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# graps the product
right_container = page_soup.find(
    "div", {"class": "rightContainer"})
print(right_container)
all_genre = right_container.find_all("a", {"class": "gr-hyperlink"})
print(all_genre)
# prepare CSV
file = "genre.csv"
header = "id, name, link \n"
f = open(file, "w", encoding="utf-8")
f.write(header)

index = 1

for genre in all_genre:
    name = genre.text
    link = genre.get("href")
    # books = td.a.select("span")
    # title = books[0].text.replace("á", "a").replace("í", "i")
    # authors = td.div.select("a")
    # author = authors[0].text.replace('é', 'e')
    # author_link = td.div.select("a")[0].get("href")
    # ratings = td.findAll("span", {"class": "greyText smallText uitext"})
    # rating = ratings[0].text.strip().replace(",", ".").replace("—", "-")
    # scores = td.findAll("div", {"style": "margin-top: 5px"})
    # score = scores[0].span.a.text.strip().replace(
    #     "score:", "").replace(",", ".").replace(" ", "")
    # voted = scores[0].span.select("a:nth-child(3)")[0].text.replace(
    #     "people voted", "").replace("person voted", "").strip()

    print("index: ", index)
    print("name: " + name)
    print("link: " + "https://www.goodreads.com" + link)
    print("\n")

    f.write(
        str(index) + ", " +
        name + ", " +
        "https://www.goodreads.com" + link +
        "\n"
    )

    index = index + 1

f.close()
