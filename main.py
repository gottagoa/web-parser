import re

from bs4 import BeautifulSoup
import requests
from db import engine


# HTTP протокол имеет несколько видов методов запросов. Например: 
# GET - запрос на получение данных
# POST - запрос на отправку данных
# DELETE - запрос на удаление
# PATCH - запрос на частичное обновление
# PUT - запрос на полное обновление 

def get_html(url):
    r = requests.get(url)
    html = r.text
    return html

def get_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    main = soup.find("div", {"class":"main-content"})
    listing = main.find("div", {"class":"listings-wrapper"})
    posts = listing.find_all("div", {"class":"listing"})

    links = []
    for p in posts:
        info = p.find("div", {"class":"right-info"})
        top = info.find("div", {"class":"top-info"})
        title = top.find("p", {"class":"title"})
        link = title.find("a").get("href")
        full_link = "https://www.house.kg" + link
        links.append(full_link)
    return links


def get_post_data(html):
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("div", {"class":"main-content"})
    header = main.find("div",{"class":"details-header"})
    left = header.find("div", {"class":"left"})
    title = left.find("h1").text.strip()
    address = left.find("div", {"class":"address"}).text.strip()
    price_som = header.find("div",{"class":"price-som"}).text.strip()
    price_dollar = header.find("div", {"class":"price-dollar"}).text.strip()
    # Block phone
    phone_number = main.find("div", {"class":"phone-fixable-block"}).find("div", {"class":"number"})
    phone_number = phone_number.text.strip()

    # Block details
    details = main.find("div", {"class":"details-main"})
    description = details.find("div", {"class":"description"})
    description = description.text.strip() if description else ""
    map_2gis = details.find("div", {"id":"map2gis"})
    lat = map_2gis.get("data-lat")
    lon = map_2gis.get("data-lon")
    info = details.find("div", {"class":"left"}).find_all("div", {"class":"info-row"})
    print(title)
    price_som = re.findall(r'\d+', price_som)[0]
    price_dollar = re.findall(r'\d+', price_dollar)[0]
    data = {
        "title":title,
        "address":address,
        "price_som":price_som,
        "price_dollar": price_dollar,
        "phone_number":phone_number,
        "description": description,
        "lat": lat,
        "lon": lon,
        # "info":info
    }
    return data

def get_last_page(html):
    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find("div", {"class":"listings-wrapper"}).find("ul", {"class":"pagination"})
    pages = ul.find_all("a", {"class":"page-link"})
    number = pages[-1].get("data-page")
    return int(number)


def write_csv(data):
    import csv 
    fieldnames = ["title", "address", "phone_number", 
                  "price_som", "price_dollar", "lat", "lon", "description"]
    with open("house.csv", "a", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(data)

def write_db(data):
    from models import PostManager
    manager = PostManager()
    manager.insert_data(data)



def main():
    URL = "https://www.house.kg/snyat-kvartiru?rooms=1%2C2%2C3&region=1&town=2&sort_by=upped_at+desc"
    lp = get_last_page(get_html(URL))
    for i in range(1, lp+1):
        print("Страница: ", i)
        URL += f"&page={i}"
        html = get_html(URL)
        post_links = get_pages(html)
        # link - хранит ссылку на страницу одного поста
        for link in post_links:
            post_html = get_html(link)
            data = get_post_data(post_html)
            write_db(data)

if __name__=="__main__":
    from utils import create_tables
    create_tables()
    main()