import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.crisol.com.pe/'

XPATH_LINK_TO_BOOK = '//div[@class = "item product product-item"]/div[@class = "product-item-info"]/div[@class = "image-product"]/a[@class = "product photo product-item-photo"]/@href'
XPATH_TITLE = '//h1[@class = "page-title"]/span[@itemprop = "name"]/text()'
XPATH_AUTHOR = '//div[@class = "author"]/span/text()'
XPATH_SYNOPSIS = '//div[@class = "additional-attributes-wrapper custom-synopsis"]/p/text()'
XPATH_PRICE = '//div[@class = "product-info-price"]/div/span[@class = "special-price"]/span[@class = "price-container price-final_price tax"]/span[@data-price-type = "finalPrice"]/span/text()'

def parse_book(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            book = response.content.decode('utf-8')
            parsed = html.fromstring(book)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                author = parsed.xpath(XPATH_AUTHOR)[0]
                synopsis = parsed.xpath(XPATH_SYNOPSIS)[0]
                price = parsed.xpath(XPATH_PRICE)[0]
            except IndexError:
                return
            
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(author)
                f.write('\n\n')
                f.write(synopsis)
                f.write('\n\n')
                f.write(price)

        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)

# Función para extraer los links de los libros en el home page de la página. Función que consideré un try y except en caso de error.
def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_books = parsed.xpath(XPATH_LINK_TO_BOOK)
            # print(links_to_books) se usó para verificar que la función parse home funcione

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_books:
                parse_book(link, today)


        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()


if __name__ == '__main__':
    run()