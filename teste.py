from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait

def pesquisaItem(driver):
    driver.find_element('xpath', '//*[@id="search-key"]').send_keys('redmi')
    driver.find_element('xpath', '//*[@id="form-searchbar"]/div[1]/input').click()


def inspencionaElemento(driver):
    driver.scroll_by_amount("window.scrollTo(0, 920)")
    driver.scroll_by_amount("window.scrollTo(0, 1080)")
    driver.scroll_by_amount("window.scrollTo(0, 1900)")

    site = driver.page_source
    pagina = BeautifulSoup(site, 'html.parser')
    print(pagina.prettify())



def main():
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
    driver.get('https://best.aliexpress.com/?lan=pt-br')
    pesquisaItem(driver)
    inspencionaElemento(driver)


if __name__ == "__main__":
    main()
