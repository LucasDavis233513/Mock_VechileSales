from selenium import webdriver

from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By


# Used for the explicit wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException, TimeoutException

# Used to interpret the exception thrown from the WebDriver
from selenium.common.exceptions import WebDriverException

# Used to add retries with exponential backoff
from retrying import retry

import base64
import io

PROGRAMMER_NAME = "Lucas Davis"

class Scraper():
    def __init__(self):
        """
        Initializes the webscrapper by creating the driver. The driver will only be created once.
        And will remain open until the closeDriver operation is called.
        """
        self.driver = self.__check_browser()

    def __check_browser(self):
        """
        """
        try:
            s = FirefoxService(GeckoDriverManager().install())

            options = FirefoxOptions()
            options.set_preference("permissions.default.image", 2)  # Block images
            options.add_argument("--headless")   # Block the broswer from launching windows
            options.add_argument('--no-sandbox')

            driver = webdriver.Firefox(service=s, options=options)
            
            return driver
        except WebDriverException as e:
            print(f"Error occurred: {e}")
            raise
    
    @retry(wait_exponential_multiplier = 1000, wait_exponential_max = 10000, stop_max_attempt_number = 3)
    def __findImage(self):
        '''
        Find the source of the first image on google images

        Looking for an img tag under this xpath:
            /html/body/div[5]/div/div[6]/div[9]/div/div[2]/div[2]/div/div /div/div/div[1]/div/div/div[1]/div[2]/h3/a/div/div/div/g-img/img
        '''
        try:
            errors = [NoSuchElementException, TimeoutException]
            wait = WebDriverWait(self.driver, timeout = 10, poll_frequency = .2, ignored_exceptions = errors)

            # Explicitly wait until the page is loaded.
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@jsData]')))

            # Scrap the source of the first result from the search query
            first_result = self.driver.find_element(By.XPATH, '//div[@jsData]//img[starts-with(@id, "dimg_")]')
            image_url = first_result.get_attribute('src')

            image_data = io.BytesIO(base64.b64decode(image_url.split(',')[1]))

            return image_data
        except TimeoutException:
            return None
        except Exception as e:
            print(e)
            return None

    def setSearchQuery(self, item: str) -> None:
        """
        Sets the search query into a URL for google images

        Parameter:
        item: the name of the item that you would like to search
        """
        self.URL = f"https://www.google.com/search?tbm=isch&q={item}"

    def closeDriver(self):
        """
        Closes the driver
        """
        if(self.driver):
            self.driver.quit()

    def getData(self):
        """
        Gets the webpage of the search query and returns the requested data
        """
        self.driver.get(self.URL)
        return self.__findImage()