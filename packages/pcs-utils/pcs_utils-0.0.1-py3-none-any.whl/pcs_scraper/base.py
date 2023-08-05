from pyvirtualdisplay import Display
from selenium import webdriver
import os

from pcs_scraper.utils import Logger


def init_driver(logger: Logger) -> webdriver:
    logger.info("Initializing Chromedriver...")

    # Create a display
    if 'MAC' not in os.environ:
        display = Display(visible=0, size=(1200, 1200))
        display.start()

    # Create a new Chrome session
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver: webdriver = None
    if 'DRIVER' not in os.environ:
        chrome_options.binary_location = '/usr/bin/chromium-browser'
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/usr/lib/chromium-browser/chromedriver')
    else:
        driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(30)
    driver.maximize_window()

    logger.info("Chromedriver started!")

    return driver
