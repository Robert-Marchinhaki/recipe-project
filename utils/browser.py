import os.path
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

HOMEDIR = os.path.expanduser("~")
CHROMEDRIVER_PATH = f"{HOMEDIR}/chromedriver/stable/chromedriver"

def make_chrome_browser(*options):
    chrome_options = Options()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser

if __name__ == '__main__':
    browser = make_chrome_browser('--headless')
    browser.get('https://www.youtube.com.br/')
    sleep(3)
    browser.quit()
