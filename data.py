import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
my_url = 'https://www.goodreads.com/list/show/83612.NY_Times_Fiction_Best_Sellers_2015'
my_url

# opening dan connection to website
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# graps the product
tds = page_soup.findAll("td", {"width": "100%", "valign": "top"})

# prepare CSV
file = "data.csv"
header = "Index, Title, Author, Rating, Score, Vote, Link, Author_Link \n"
f = open(file, "w")
f.write(header)

index = 1
for td in tds:
    link = td.a.get("href")
    books = td.a.select("span")
    title = books[0].text.replace("á", "a").replace("í", "i")
    authors = td.div.select("a")
    author = authors[0].text.replace('é', 'e')
    author_link = td.div.select("a")[0].get("href")
    ratings = td.findAll("span", {"class": "greyText smallText uitext"})
    rating = ratings[0].text.strip().replace(",", ".").replace("—", "-")
    scores = td.findAll("div", {"style": "margin-top: 5px"})
    score = scores[0].span.a.text.strip().replace(
        "score:", "").replace(",", ".").replace(" ", "")
    voted = scores[0].span.select("a:nth-child(3)")[0].text.replace(
        "people voted", "").replace("person voted", "").strip()

    print("index: ", index)
    print("name: " + title)
    print("author: " + author)
    print("author_link: " + author_link)
    print("rating: " + rating)
    print("score: " + score)
    print("vote: " + voted)
    print("link: " + "https://www.goodreads.com" + link)
    print("\n")

    f.write(str(index) + ", " + title.replace(",", "") + ", " +
            author + ", " + rating + ", " + score + ", " + voted + ", " + "https://www.goodreads.com" + link + ", " + author_link + "\n")

    index = index + 1

f.close()
