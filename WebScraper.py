from selenium import webdriver

# The following imports are used for the API to scrap Amazon
# Webdrivers for the firefox browser
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

# Webdrivers for the chrome browser
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Used for the explicit wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException, TimeoutException

# Webdriver options, used to specify the headless arguemnt (used so the browsers don't open)
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Used to interpret the exception thrown from the WebDriver
from selenium.common.exceptions import WebDriverException

# Used to add retries with exponential backoff
from retrying import retry

import base64
import io

from Grab_Ini import ini

class Scraper():
    def __init__(self):
        """
        Initializes the webscrapper by creating the driver. The driver will only be created once.
        And will remain open until the closeDriver operation is called.

        Parameter:
        browserName: the name of the browser you would like to use for the scrapper
        This scraper only supports the firefox and chrome browsers. Will return
        None if an unsupported browser is passed.
        """
        browser = ini().grabInfo("config.ini", "browser_settings")
        self.driver = self.__check_browser(browser['name'])

    def __check_browser(self, browserName: str):
        """
        Checks the browser passed durning initialization and creates a driver for the given browser if it is
        supported.

        Parameter:
        browserName: The name of the browser you would like to use
        """
        try:
            if(browserName.lower() == "firefox"):
                s = Service(GeckoDriverManager().install())
                options = FirefoxOptions()
            elif(browserName.lower() == "chrome"):
                s = Service(ChromeDriverManager().install())
                options = ChromeOptions()
            else:
                return None # Return None if firefox or chrome wasn't found

            options.add_argument("--headless")                  # Run in headless mode (browser doesn't open)

            driver = webdriver.Firefox(service=s, options=options) if browserName.lower() == "firefox" else webdriver.Chrome(service=s, options=options)
            
            return driver
        except WebDriverException as e:
            print(f"Error occurred: {e}") # Return error if there was an error opening the browser
            return None
    
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

            # Explicitly wait until the images are visible.
            wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@jsData]//img[starts-with(@id, "dimg_")]')))

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