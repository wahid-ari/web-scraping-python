import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
# my_url = 'https://www.goodreads.com/list/show/83612.NY_Times_Fiction_Best_Sellers_2015'
my_url = 'https://www.goodreads.com/list/show/184936.Fairytale_Courtyard'

# opening an connection to website
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# prepare CSV
file = "pagination.csv"
header = "Index, Title, Author, Rating, Score, Vote, Link, Author_Link, Image, Image_Small \n"
f = open(file, "w")
f.write(header)

# index of product 
index = 1

# first page scrap
# here we are graps the product
trs = page_soup.findAll(
    "tr", {"itemscope": "", "itemtype": "http://schema.org/Book"})

# iterate by each product in first page
for tr in trs:
    image_small = tr.findAll("td", {"width": "5%", "valign": "top"})[
        0].img.get("src")
    image = tr.findAll("td", {"width": "5%", "valign": "top"})[0].img.get("src").replace("https://i.gr-assets.com/images/S/compressed.photo.goodreads.com",
                                                                                            "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com").replace("._SY75_", "").replace("._SX50_", "")
    box = tr.findAll("td", {"width": "100%", "valign": "top"})
    link = box[0].a.get("href")
    books = box[0].a.select("span")
    title = books[0].text.replace("á", "a").replace("í", "i").replace('"', "'")
    authors = box[0].div.select("a")
    author = authors[0].text.replace('é', 'e')
    author_link = box[0].div.select("a")[0].get("href")
    ratings = box[0].findAll(
        "span", {"class": "greyText smallText uitext"})
    rating = ratings[0].text.strip().replace(
        ",", ".").replace("—", "-")
    scores = box[0].findAll("div", {"style": "margin-top: 5px"})
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
    print("image: ", image)
    print("image_small: ", image_small)
    print("\n")

    f.write(str(index) + ", " +
            title.replace(",", "") + ", " +
            author + ", " +
            rating + ", " +
            score + ", " +
            voted + ", " +
            "https://www.goodreads.com" + link + ", " +
            author_link + ", " +
            image + ", " +
            image_small +
            "\n")

    index = index + 1

# get the pagination link 
pagination = page_soup.find(
    "div", {"class": "pagination"})

# second to last page 
for p in pagination.findAll('a'):
    if (p.get('class') == None):
        next_url = "https://www.goodreads.com" + p.get("href")
        # call get method to request next url
        # opening an connection to website
        nextClient = uReq(next_url)
        next_page_html = nextClient.read()
        nextClient.close()
        # create soup for next url
        # html parsing
        next_page_soup = soup(next_page_html, "html.parser")
        # we can scrap any thing of the
        # next page here we are graps the product
        trs = next_page_soup.findAll(
            "tr", {"itemscope": "", "itemtype": "http://schema.org/Book"})
        # iterate by each product in next page
        for tr in trs:
            image_small = tr.findAll("td", {"width": "5%", "valign": "top"})[
                0].img.get("src")
            image = tr.findAll("td", {"width": "5%", "valign": "top"})[0].img.get("src").replace("https://i.gr-assets.com/images/S/compressed.photo.goodreads.com",
                                                                                                 "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com").replace("._SY75_", "").replace("._SX50_", "")
            box = tr.findAll("td", {"width": "100%", "valign": "top"})
            link = box[0].a.get("href")
            books = box[0].a.select("span")
            title = books[0].text.replace("á", "a").replace(
                "í", "i").replace('"', "'")
            authors = box[0].div.select("a")
            author = authors[0].text.replace('é', 'e')
            author_link = box[0].div.select("a")[0].get("href")
            ratings = box[0].findAll(
                "span", {"class": "greyText smallText uitext"})
            rating = ratings[0].text.strip().replace(
                ",", ".").replace("—", "-")
            scores = box[0].findAll("div", {"style": "margin-top: 5px"})
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
            print("image: ", image)
            print("image_small: ", image_small)
            print("\n")

            f.write(str(index) + ", " +
                    title.replace(",", "") + ", " +
                    author + ", " +
                    rating + ", " +
                    score + ", " +
                    voted + ", " +
                    "https://www.goodreads.com" + link + ", " +
                    author_link + ", " +
                    image + ", " +
                    image_small +
                    "\n")

            index = index + 1

f.close()