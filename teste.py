from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import psycopg2


# configuração banco de dados

def configdb():
    host = "b68b2e5250c1"
    dbname = "teste"
    user = "postgres"
    password = 1234
    sslmode = "require"

    # string de conexão

    conn_string = 'host={0} user ={1} dbname={2} password={3} sslmode={4}'.format(host, user, dbname, password, sslmode)

    conn = psycopg2.connect(conn_string)
    print('conectado')

    cursor = conn.cursor()

    # função para criar tabela
def createTable(configdb):
    cursor = configdb.cursor
    cursor.execute("CREATE TABLE Products (id serial PRIMARY KEY, itens VARCHAR(255);")
    print("tabela criada com sucesso")

    # função para inserir valores no banco de dados
def insertValues (configdb, getItensInPage): 
    cursor = configdb.cursor
    cursor.execute("INSERT INTO Products (itens) VALUES (%s);", (getItensInPage))

def closeDataBase(configdb):
    cursor = configdb.cursor
    conn = configdb.conn
    conn.commit()
    cursor.close()
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
    configdb()
    createTable(configdb)
    insertValues(configdb, getItensInPage)
    closeDataBase(configdb)



if __name__ == "__main__":
    main()
