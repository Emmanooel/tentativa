from selenium import webdriver
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


def execute_query_insert (query): 
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

def search(driver, searchItem):
    driver.find_element('xpath', '//*[@id="search-key"]').send_keys(searchItem)
    driver.find_element('xpath', '//*[@id="form-searchbar"]/div[1]/input').click()


def getItensInPage(driver):
    page = BeautifulSoup(driver.page_source, 'html.parser')
    listProducts = []
    elements = page.find('div', attrs={'class': 'JIIxO'}).find_all('a', attrs={'class': '_3t7zg _2f4Ho'})

    for element in elements:
        spans = element.find('div', attrs={'class': 'mGXnE _37W_B'}).find_all('span')
        price = ''

        for span in spans:
            price = price + span.getText()

        product = Product()
        product.name = element.find('h1').getText()

        if len(price) > 3:
            product.price = float(price.replace('R$', '').replace('.', '').replace(',', '.'))
            product.priceIsValid = True

        listProducts.append(product)

    return listProducts


def main():
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
    driver.get('https://pt.aliexpress.com/?spm=a2g0o.productlist.1000002.1.3cc16dbfvgZy5D&gatewayAdapt=glo2bra')
    search(driver, 'redmi')
    getItensInPage(driver)

#chamando as funções para banco de dados




if __name__ == "__main__":
    main()
