import bs4
import json
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
my_url = 'https://www.goodreads.com/list/show/83612.NY_Times_Fiction_Best_Sellers_2015'
# my_url = 'https://www.goodreads.com/list/show/184936.Fairytale_Courtyard'

# opening an connection to website
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# prepare CSV
file = "pagination_detail_book.csv"
header = "Index, Title, Author, ISBN, Language, Pages, Published, Genre, Rating, Score, Vote, Link, Author_Link, Image, Image_Small, Description \n"
f = open(file, "w", encoding="utf-8")
f.write(header)

# index of product
index = 1

# first page scrap
# here we are graps the product
trs = page_soup.findAll(
    "tr", {"itemscope": "", "itemtype": "http://schema.org/Book"})

# iterate by each product in first page
# for tr in trs[33:34]:
for tr in trs:
    image_small = tr.findAll("td", {"width": "5%", "valign": "top"})[
        0].img.get("src")
    image = tr.findAll("td", {"width": "5%", "valign": "top"})[0].img.get("src").replace("https://i.gr-assets.com/images/S/compressed.photo.goodreads.com",
                                                                                         "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com").replace("._SY75_", "").replace("._SX50_", "")
    box = tr.findAll("td", {"width": "100%", "valign": "top"})
    link = box[0].a.get("href")
    books = box[0].a.select("span")
    title = books[0].text.replace("á", "a").replace("í", "i").replace('"', "'").replace(';', " - ")
    authors = box[0].div.select("a")
    author = authors[0].text.replace('é', 'e')
    author_link = box[0].div.select("a")[0].get("href")
    ratings = box[0].findAll(
        "span", {"class": "greyText smallText uitext"})
    rating = ratings[0].text.strip().replace(
        ",", ".").replace("—", "-").replace("really liked it", '')
    scores = box[0].findAll("div", {"style": "margin-top: 5px"})
    score = scores[0].span.a.text.strip().replace(
        "score:", "").replace(",", ".").replace(" ", "")
    voted = scores[0].span.select("a:nth-child(3)")[0].text.replace(
        "people voted", "").replace("person voted", "").strip()
    # opening detail book
    nextClient = uReq("https://www.goodreads.com" + link)
    detail_book_page_html = nextClient.read()
    nextClient.close()
    # create soup for next url
    # html parsing
    detail_page_soup = soup(detail_book_page_html, "html.parser")
    # we can scrap any thing of the
    # next page here we are graps the product
    detail_layout = detail_page_soup.find(
        "div", {"class": "DetailsLayoutRightParagraph__widthConstrained"})
    book_description = detail_layout.text.strip().replace(
        '.', '. ').replace('  ', ' ').replace(";", '').replace("\n", '').replace(",", '*')
    # print(detail_layout.span.text)
    # print(detail_layout.contents)
    # print("description: ", book_description)
    feature_layout = detail_page_soup.find(
        "div", {"class": "FeaturedDetails"})
    book_total_pages = feature_layout.findAll(
        'p')[0].text.replace(" pages, Hardcover", '').replace(" pages, Paperback", '').replace(" pages, Kindle Edition", '').replace(" pages, ebook", '')
    book_published = feature_layout.findAll(
        'p')[1].text.replace("First published ", '').replace(",", '')
    # print("pages: ", book_total_pages)
    # print("published: ", book_published)
    box_genre = detail_page_soup.find(
        'div', {'class': 'BookPageMetadataSection__genres', 'data-testid': 'genresList'})
    all_genre_list = []
    all_genre_links_list = []
    if box_genre != None:
        for a in box_genre.find_all('a'):
            all_genre_list.append(a.text)
            all_genre_links_list.append(a.get('href'))
    # print(all_genre_list)
    # print(all_genre_links_list)
    all_genre_string = '* '.join(all_genre_list)
    # print(all_genre_string)
    box_book_detail = detail_page_soup.findAll(
        "script", {"type": "application/ld+json"})
    site_json = json.loads(box_book_detail[0].text)
    # print(box_book_detail[0].text)
    # print(site_json)
    # json_formatted_str = json.dumps(site_json, indent=2)
    # print(json_formatted_str)
    isbn = ''
    if site_json.get("isbn") == None:
        isbn = 'null'
    else:
        isbn = site_json.get("isbn")
    # print(isbn)
    language = site_json.get("inLanguage").replace(';', '*')
    # print(language)

    print("index: ", index)
    print("name: " + title)
    # print("author: " + author)
    # print("author_link: " + author_link)
    # print("rating: " + rating)
    # print("score: " + score)
    # print("vote: " + voted)
    # print("link: " + "https://www.goodreads.com" + link)
    # print("image: ", image)
    # print("image_small: ", image_small)
    print("\n")

    f.write(str(index) + ", " +
            title.replace(",", "") + ", " +
            author + ", " +
            str(isbn) + ", " +
            language + ", " +
            book_total_pages + ", " +
            book_published + ", " +
            all_genre_string + ", " +
            rating + ", " +
            score + ", " +
            voted + ", " +
            "https://www.goodreads.com" + link + ", " +
            author_link + ", " +
            image + ", " +
            image_small + ", " +
            book_description +
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
                "í", "i").replace('"', "'").replace(';', " - ")
            authors = box[0].div.select("a")
            author = authors[0].text.replace('é', 'e')
            author_link = box[0].div.select("a")[0].get("href")
            ratings = box[0].findAll(
                "span", {"class": "greyText smallText uitext"})
            rating = ratings[0].text.strip().replace(
                ",", ".").replace("—", "-").replace("really liked it", '')
            scores = box[0].findAll("div", {"style": "margin-top: 5px"})
            score = scores[0].span.a.text.strip().replace(
                "score:", "").replace(",", ".").replace(" ", "")
            voted = scores[0].span.select("a:nth-child(3)")[0].text.replace(
                "people voted", "").replace("person voted", "").strip()
            # opening detail book
            nextClient = uReq("https://www.goodreads.com" + link)
            detail_book_page_html = nextClient.read()
            nextClient.close()
            # create soup for next url
            # html parsing
            detail_page_soup = soup(detail_book_page_html, "html.parser")
            # we can scrap any thing of the
            # next page here we are graps the product
            detail_layout = detail_page_soup.find(
                "div", {"class": "DetailsLayoutRightParagraph__widthConstrained"})
            book_description = detail_layout.text.strip().replace(
                '.', '. ').replace('  ', ' ').replace(";", '').replace("\n", '').replace(",", '*')
            # print(detail_layout.span.text)
            # print(detail_layout.contents)
            # print("description: ", book_description)
            feature_layout = detail_page_soup.find(
                "div", {"class": "FeaturedDetails"})
            book_total_pages = feature_layout.findAll(
                'p')[0].text.replace(" pages, Hardcover", '').replace(" pages, Paperback", '').replace(" pages, Kindle Edition", '').replace(" pages, ebook", '')
            book_published = feature_layout.findAll(
                'p')[1].text.replace("First published ", '').replace(",", '')
            # print("pages: ", book_total_pages)
            # print("published: ", book_published)
            box_genre = detail_page_soup.find(
                'div', {'class': 'BookPageMetadataSection__genres', 'data-testid': 'genresList'})
            all_genre_list = []
            all_genre_links_list = []
            if box_genre != None:
                for a in box_genre.find_all('a'):
                    all_genre_list.append(a.text)
                    all_genre_links_list.append(a.get('href'))
            # print(all_genre_list)
            # print(all_genre_links_list)
            all_genre_string = '* '.join(all_genre_list)
            # print(all_genre_string)
            box_book_detail = detail_page_soup.findAll(
                "script", {"type": "application/ld+json"})
            site_json = json.loads(box_book_detail[0].text)
            # print(box_book_detail[0].text)
            # print(site_json)
            # json_formatted_str = json.dumps(site_json, indent=2)
            # print(json_formatted_str)
            isbn = ''
            if site_json.get("isbn") == None:
                isbn = 'null'
            else:
                isbn = site_json.get("isbn")
            # print(isbn)
            language = site_json.get("inLanguage").replace(';', '*')
            # print(language)

            print("index: ", index)
            print("name: " + title)
            # print("author: " + author)
            # print("author_link: " + author_link)
            # print("rating: " + rating)
            # print("score: " + score)
            # print("vote: " + voted)
            # print("link: " + "https://www.goodreads.com" + link)
            # print("image: ", image)
            # print("image_small: ", image_small)
            print("\n")

            f.write(str(index) + ", " +
                    title.replace(",", "") + ", " +
                    author + ", " +
                    str(isbn) + ", " +
                    language + ", " +
                    book_total_pages + ", " +
                    book_published + ", " +
                    all_genre_string + ", " +
                    rating + ", " +
                    score + ", " +
                    voted + ", " +
                    "https://www.goodreads.com" + link + ", " +
                    author_link + ", " +
                    image + ", " +
                    image_small + ", " +
                    book_description +
                    "\n")

            index = index + 1

f.close()