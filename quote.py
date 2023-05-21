import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
my_url = 'https://www.goodreads.com/quotes?page=10'

# opening an connection to website
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# prepare CSV
file = "quote.csv"
header = "id, name, quote, tags, link, image, born, web, bio \n"
f = open(file, "w", encoding="utf-8")
f.write(header)

# index of product
index = 242

# first page scrap
# here we are graps the product
trs = page_soup.findAll(
    "div", {"class": "quote"})

# iterate by each product in first page
for tr in trs:
    # print(index)
    author = tr.find("span", {"class": "authorOrTitle"}
                     ).text.strip().replace(',', '')
    # print(author)
    is_image_author = tr.find("img")
    image = ''
    if (is_image_author != None):
        image = tr.find("img").get("src")
    # print(image)
    is_author_link = tr.find("a", {"class": "leftAlignedImage"})
    author_link = ''
    if (is_image_author != None):
        if (tr.find("a").get("href").startswith('/') == True):
            author_link = "https://www.goodreads.com" + \
                tr.find("a").get("href")
    # print(author_link)
    quote = tr.find("div", {"class": "quoteText"}).text.strip().split("―")[
        0].replace(',', '*').replace('\n', '').replace('“', '').replace('”', '').strip()
    # print(quote)
    tags_box = tr.find("div", {"class": "quoteFooter"})
    tags_links = tags_box.findAll("a")
    tags = ''
    for i in tags_links[:-1]:
        tags += i.text + "* "
    # print(tags)

    if (author_link != ''):
        # OPEN AUTHOR PAGE
        nextAuthorClient = uReq(author_link)
        book_author_page_html = nextAuthorClient.read()
        nextAuthorClient.close()
        # create soup for next url
        # html parsing
        author_page_soup = soup(book_author_page_html, "html.parser")
        # we can scrap any thing of the
        # next page here we are graps the product
        author_left_layout = author_page_soup.find(
            "div", {"class": "leftContainer authorLeftContainer"})
        author_image = author_left_layout.select("img")[0].get("src")
        # print(author_image)
        author_right_layout = author_page_soup.find(
            "div", {"class": "rightContainer"})
        # print(author_right_layout)
        author_born = author_right_layout.find(
            "div", {"class": "dataTitle"}).next_sibling.text.replace("\n", '').replace('in ', '').replace(',', '*').strip()
        # print(author_born)
        is_author_web = author_right_layout.find("div", {"class": "dataItem"})
        author_web = ''
        if (is_author_web != None):
            author_web = author_right_layout.find(
                "a", {"itemprop": "url"}).text.replace("\n", '').strip()
        elif (is_author_web == None):
            author_web = "null"
        # print(author_web)
        author_about_layout = author_right_layout.find(
            "div", {"class": "aboutAuthorInfo"})
        is_author_bio = author_about_layout.find("span")
        # print(is_author_bio)
        author_bio = ''
        if (is_author_bio != None):
            author_bio = author_about_layout.find(
                "span").text.replace("\n", '').replace(";", '-').replace(",", '*')
        elif (is_author_bio == None):
            author_bio = 'null'
        # Fix Error UnicodeEncodeError: 'charmap' codec can't encode characters in position 1184-1191: character maps to < undefined >
        # author_bio = author_about_layout.find("span").text.replace(
        #     "\n", '').replace("(カズオ・イシグロ or 石黒 一雄)", '').replace(" ,", ',')
        # print(author_bio)

    if (author_link != ''):
        print("index: ", index)
        print("author: " + author)
        print("quote: " + quote)
        print("tags: " + tags)
        print("image: " + image)
        print("author image: " + author_image)
        print("author link: " + author_link)
        print("author born: " + author_born)
        print("author web: ", author_web)
        print("author bio: ", author_bio)
        print("\n")

        f.write(str(index) + ", " +
                author + ", " +
                quote + ", " +
                tags + ", " +
                author_link + ", " +
                author_image + ", " +
                author_born + ", " +
                author_web + ", " +
                author_bio +
                "\n")
        # id, author, quote, tags, link, image, born, web, bio

        index = index + 1

# # get the pagination link
# pagination = page_soup.find(
#     "div", {"class": "pagination"})

# # second to last page
# for p in pagination.findAll('a'):
#     if (p.get('class') == None):
#         next_url = "https://www.goodreads.com" + p.get("href")
#         # call get method to request next url
#         # opening an connection to website
#         nextClient = uReq(next_url)
#         next_page_html = nextClient.read()
#         nextClient.close()
#         # create soup for next url
#         # html parsing
#         next_page_soup = soup(next_page_html, "html.parser")
#         # we can scrap any thing of the
#         # next page here we are graps the product
#         trs = next_page_soup.findAll(
#             "tr", {"itemscope": "", "itemtype": "http://schema.org/Book"})
#         # iterate by each product in next page
#         for tr in trs:
#             image_small = tr.findAll("td", {"width": "5%", "valign": "top"})[
#                 0].img.get("src")
#             image = tr.findAll("td", {"width": "5%", "valign": "top"})[0].img.get("src").replace("https://i.gr-assets.com/images/S/compressed.photo.goodreads.com",
#                                                                                                  "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com").replace("._SY75_", "").replace("._SX50_", "")
#             box = tr.findAll("td", {"width": "100%", "valign": "top"})
#             link = box[0].a.get("href")
#             books = box[0].a.select("span")
#             title = books[0].text.replace("á", "a").replace(
#                 "í", "i").replace('"', "'")
#             authors = box[0].div.select("a")
#             author = authors[0].text.replace('é', 'e')
#             author_link = box[0].div.select("a")[0].get("href")
#             ratings = box[0].findAll(
#                 "span", {"class": "greyText smallText uitext"})
#             rating = ratings[0].text.strip().replace(
#                 ",", ".").replace("—", "-")
#             scores = box[0].findAll("div", {"style": "margin-top: 5px"})
#             score = scores[0].span.a.text.strip().replace(
#                 "score:", "").replace(",", ".").replace(" ", "")
#             voted = scores[0].span.select("a:nth-child(3)")[0].text.replace(
#                 "people voted", "").replace("person voted", "").strip()

#             print("index: ", index)
#             print("name: " + title)
#             print("author: " + author)
#             print("author_link: " + author_link)
#             print("rating: " + rating)
#             print("score: " + score)
#             print("vote: " + voted)
#             print("link: " + "https://www.goodreads.com" + link)
#             print("image: ", image)
#             print("image_small: ", image_small)
#             print("\n")

#             f.write(str(index) + ", " +
#                     title.replace(",", "") + ", " +
#                     author + ", " +
#                     rating + ", " +
#                     score + ", " +
#                     voted + ", " +
#                     "https://www.goodreads.com" + link + ", " +
#                     author_link + ", " +
#                     image + ", " +
#                     image_small +
#                     "\n")

#             index = index + 1

f.close()
