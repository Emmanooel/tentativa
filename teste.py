from selenium import webdriver
from bs4 import BeautifulSoup
import time
import psycopg2
import smtplib

from soupsieve import select


class Product:
    name = ''
    price = 0.0
    url = ''
    priceIsValid = False


# configuração banco de dados

def db_connect():
    _host = "localhost"
    _port = "5432"
    _user = "postgres"
    _pass = 1234

    return psycopg2.connect(host=_host, port=_port, user=_user, password=_pass)


# def execute_query_insert(query):
#     conn = db_connect()
#     try:
#         cursor = conn.cursor()
#         cursor.execute(query)
#         conn.commit()
#     finally:
#         conn.close()


def execute_query_select(query):
    conn = db_connect()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        list = []
        for element in records:
            product = Product()
            product.name = element[0]
            product.price = element[1]
            product.url = element[2]
            list.append(product)
        return list
    except Exception as e:
        print(e)
    finally:
        conn.close()


def insert_products(products):
    for product in products:
        query = f"INSERT INTO public.products ( name, price, url) VALUES ('{product.name}', {product.price}, '{product.url}')"
        execute_query_insert(query)


def search(driver, item):
    driver.find_element('xpath', '//*[@id="search-key"]').send_keys(item)
    driver.find_element('xpath', '//*[@id="form-searchbar"]/div[1]/input').click()

    for roll in range(6):
        driver.execute_script(f'window.scrollTo(0, {roll * 1080});')
        time.sleep(1.5)


def getItensInPage(driver):
    page = BeautifulSoup(driver.page_source, 'html.parser')
    listProducts = []
    time.sleep(1.5)

    elements = page.find('div', attrs={'class': 'JIIxO'}).find_all('a', attrs={'class': '_3t7zg _2f4Ho'})

    for element in elements:
        spans = element.find('div', attrs={'class': 'mGXnE _37W_B'}).find_all('span')
        price = ''

        for span in spans:
            price = price + span.getText()

        product = Product()
        product.name = element.find('h1').getText()
        product.url = element.attrs['href'].replace('//', 'https://')

        if len(price) > 3:
            product.price = float(price.replace('R$', '').replace('.', '').replace(',', '.'))

        listProducts.append(product)

    return listProducts


def send_email(select_list):
    smtp = smtplib.SMTP_SSL('smtpgmail.com', 465)
    mensagem_email = f'segue a lista de itens adquiridas no site, segue a lista: {select_list}'
    
    msg = email.message.Message(mensagem_email)
    assunto = msg['Assunto'] = 'Lista de itens solicitada para a aula do dia 10/10'
    de = msg['De'] = 'emmanoelk@gmail.com'
    para = msg['Para'] = 'braullio.goncalves@easyc.com.br'
    password = 'wfcjukmewmcqaloy'
    email = 'emmanoelk@gmail.com'

    smtp.login(email, password)
    smtp.sendmail(de, para, assunto)
    smtp.quit


def main():
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get('https://pt.aliexpress.com/?spm=a2g0o.productlist.1000002.1.3cc16dbfvgZy5D&gatewayAdapt=glo2bra')
    search(driver, 'redmi')
    listProducts = getItensInPage(driver)
    insert_products(listProducts)
    select_list = execute_query_select('SELECT name, price, url from public.products  order by price limit 5')

    # TODO: Criar um metodo para envio de email ( para braullio.goncalves@easyc.com.br ) com o raking dos 5
    send_email(select_list)

if __name__ == "__main__":
    main()
