import time
from selenium import webdriver 
from selenium.webdriver.common import by
from selenium.webdriver.common import keys

def bot():
    DRIVER_PATH = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    site = driver.get('https://best.aliexpress.com/?lan=en')

    pesquisar_item(driver)
    
    inspenciona_elemento(driver)


def pesquisar_item(driver):
    driver.find_element('xpath', '//*[@id="search-key"]').send_keys('redmi')
    time.sleep(5)
    driver.find_element('xpath', '//*[@id="form-searchbar"]/div[1]/input').click()

def inspenciona_elemento(driver):
    name_element = driver.find_element('xpath', '//*[@id="root"]/div[1]/div/div[2]/div[2]/div/div[2]/a[9]/div[2]/div[1]').text
    element = driver.find_element('xpath', '//*[@id="root"]/div[1]/div/div[2]/div[2]/div/div[2]/a[9]/div[2]/div[2]').text
    
    print(element)
    print(name_element)



if(__name__ == "__main__"):
    bot()