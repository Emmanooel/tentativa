from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep


def pesquisaItem(driver):
    driver.find_element('xpath', '//*[@id="search-key"]').send_keys('redmi')
    driver.find_element('xpath', '//*[@id="form-searchbar"]/div[1]/input').click()


def inspencionaElemento(driver):
    site = driver.page_source
    pagina = BeautifulSoup(site, 'html.parser')

    itensPagina = pagina.find('div', attrs={'class': 'JIIxO'})

    for item in range(10):
        tagA = itensPagina.find('a')
        print(tagA)
        nameItem = tagA.find('div', attrs={'class': '_3GR-w'}).find_all('h1')
        print(nameItem)
        precoItem = tagA.find('div', attrs={'class': '_3GR-w'}).find_all('div', attrs={'class': '_11_8K'})
        print(precoItem)

    print(item)
    

def bot():
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
    driver.get('https://pt.aliexpress.com/?spm=a2g0o.productlist.1000002.1.3cc16dbfvgZy5D&gatewayAdapt=glo2bra')
    pesquisaItem(driver)
    inspencionaElemento(driver)


if __name__ == "__main__":
    bot()
