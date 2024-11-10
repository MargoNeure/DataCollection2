
from bs4 import BeautifulSoup  # Правильный импорт
import requests
import pandas as pd
from pprint import pprint
from fake_useragent import UserAgent
import re
import json

ua = UserAgent()

url = "https://books.toscrape.com"
headers = {"User-Agent": ua.random}
params = {"page-": 1}


session = requests.session()
url_2 = []
books = []
i = 1

for page in range(1, 51):  # страницы 1-50
    # books = []
    # url_2 = []
    current_url = f"{url}/catalogue/page-{page}.html"
    response = session.get(current_url,  headers=headers, params=params)
    soup = BeautifulSoup(response.text, features="html.parser")
    rows = soup.find_all('li', {'class': 'col-lg-3'})


    for row in rows:
        link = row.find('a')
        if link:
            href = link.get('href')
            if href:
                # if page == 1:
                #     full_url = url  + '/' + href if not href.startswith('http') else href
                # else:
                full_url = url  + '/catalogue/' + href if not href.startswith('http') else href
                url_2.append(full_url) # все ссылуи на книги

    # pprint(url_2)

#


    print(f"Обработана {page} страница")
    page += 1

for full_url in url_2:
    try:
        response1 = requests.get(full_url)  # Используем link вместо first_link
        soup1 = BeautifulSoup(response1.content, 'html.parser')
        result = soup1.find('div', {'class': 'product_main'})  # Используем find вместо find_all

        book = {}
        book['№'] = i
        # Собираем данные о книге
        book['name'] = soup1.find('h1').text.strip()

        price = result.find('p', {'class': 'price_color'}).getText()
        book['price'] = float(price.replace('£', ''))

        stock_info = soup1.find('p', {'class': 'instock availability'})
        stock_text = stock_info.text.strip()
        stock_number = re.search(r'\d+', stock_text)
        stock = int(stock_number.group())
        book['inStock'] = stock

        # book['page'] = page

        books.append(book)  # Все данные по всей 1000 книг
        print(f"Записана {i} книга")
        i += 1
    except Exception as e:
        print(f"Ошибка при обработке {full_url}: {e}")
        continue

pprint(books)



# сохранение данных в JSON-файл
with open('books_DZ2_1.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, indent=4)



