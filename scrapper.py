import requests
import lxml.html as html

HOME_URL = 'https://www.crisol.com.pe/'

XPATH_LINK_TO_BOOK = '//div[@class = "item product product-item"]/div[@class = "product-item-info"]/div[@class = "image-product"]/a[@class = "product photo product-item-photo"]/@href'
XPATH_TITLE = '//h1[@class = "page-title"]/span[@itemprop = "name"]/text()'
XPATH_AUTHOR = '//div[@class = "author"]/span/text()'
XPATH_SYNOPSIS = '//div[@class = "additional-attributes-wrapper custom-synopsis"]/p/text()'
XPATH_PRICE = '//div[@class = "product-info-price"]/div/span[@class = "special-price"]/span[@class = "price-container price-final_price tax"]/span[@data-price-type = "finalPrice"]/span/text()'

# Función para extraer los links de los libros en el home page de la página. Función que consideré un try y except en caso de error.
def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_books = parsed.xpath(XPATH_LINK_TO_BOOK)
            print(links_to_books)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()


if __name__ == '__main__':
    run()