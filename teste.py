from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import psycopg2


# configuração banco de dados

def dbConnect():
    _host = "localhost"
    _port = "5432"
    _user = "postgres"
    _pass = 1234

    return psycopg2.connect(host=_host, port=_port, user=_user, password=_pass)


def execute_query_insert(query):
    conn = dbConnect()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    finally:
        conn.close()


def execute_query_select(TODO):
    conn = dbConnect()
    try:
        cursor = conn.cursor()
        cursor.execute(TODO)
        conn.commit()
    finally:
        conn.close()


class Product:
    name = ''
    price = 0.0
    url = ''
    priceIsValid = False


def search(browser, searchItem):
    browser.find_element('xpath', '//*[@id="search-key"]').send_keys(searchItem)
    browser.find_element('xpath', '//*[@id="form-searchbar"]/div[1]/input').click()

    scroll = 1080
    for roll in range(5):
        script_roll = browser.execute_script(f'window.scrollTo(0, {scroll});')
        scroll += 1080


def getItensInPage(browser):
    page = BeautifulSoup(browser.page_source, 'html.parser')
    listProducts = []
    elements = page.find('div', attrs={'class': 'JIIxO'}).find_all('a', attrs={'class': '_3t7zg _2f4Ho'})

    for element in elements:
        spans = element.find('div', attrs={'class': 'mGXnE _37W_B'}).find_all('span')
        price = ''

        for span in spans:
            price = price + span.getText()

        product = Product()
        product.name = element.find('h1').getText()
        product.url = element.attrs['href'].replace('//', '')

        if len(price) > 3:
            product.price = float(price.replace('R$', '').replace('.', '').replace(',', '.'))
            product.priceIsValid = True

        listProducts.append(product)

    return listProducts


def main():
    browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
    browser.get('https://pt.aliexpress.com/?spm=a2g0o.productlist.1000002.1.3cc16dbfvgZy5D&gatewayAdapt=glo2bra')
    search(browser, 'redmi')
    getItensInPage(browser)


# chamando as funções para banco de dados


if __name__ == "__main__":
    main()
