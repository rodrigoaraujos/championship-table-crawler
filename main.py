from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = 'https://globoesporte.globo.com/futebol/futebol-internacional/futebol-espanhol/'


def setup():
    option = Options()
    option.headless = True
    driver = webdriver.Chrome(options=option)
    return driver


def request(driver, url):
    driver.get(url)
    driver.maximize_window()


def main():
    driver = setup()
    request(driver, URL)


if __name__ == "__main__":
    main()
