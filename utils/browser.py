import os
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

HOMEDIR = os.path.expanduser("~")
CHROMEDRIVER_PATH = f"{HOMEDIR}/chromedriver/stable/chromedriver"

load_dotenv()


def make_chrome_browser(*options):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if bool(int(os.environ.get('SELENIUM_HEADLESS', 0))):
        chrome_options.add_argument('--headless')

    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == '__main__':
    print(bool(int(os.environ.get('SELENIUM_HEADLESS', 0))))
    browser = make_chrome_browser()
    browser.get('https://www.youtube.com.br/')
    sleep(3)
    browser.quit()
