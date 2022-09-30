import re

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep


def search(driver, itemSearch):
    driver.find_element('xpath', '//*[@id="search-key"]').send_keys(itemSearch)
    driver.find_element('xpath', '//*[@id="form-searchbar"]/div[1]/input').click()


def inspencionaElemento(driver):
    page = BeautifulSoup(driver.page_source, 'html.parser')
    pageItem = page.find('div', attrs={'class': 'JIIxO'})
    listName = []
    listPrice = []
    listURL = []
    for element in pageItem:
        nameElement = element.find('div', attrs={'class': '_1tu1Z Vgu6S'})
        price = pageItem.find_all('div', attrs={'class': 'mGXnE _37W_B'})

        name = nameElement.getText()
        url = itemURL
        listName.append(name)
        listURL.append(url)

        for value in price:
            listValue = value.getText()
            listPrice.append(listValue)

    print(listPrice)
    print(listName)
    print(listURL)







def main():
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
    driver.get('https://pt.aliexpress.com/?spm=a2g0o.productlist.1000002.1.3cc16dbfvgZy5D&gatewayAdapt=glo2bra')
    search(driver, 'redmi')
    inspencionaElemento(driver)


if __name__ == "__main__":
    main()
