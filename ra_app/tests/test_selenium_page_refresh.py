from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestPageRefresh(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)
        logging.info('Webdriver setup complete.')


    @classmethod
    def tearDownClass(cls):
        logging.info('Closing Webdriver.')
        cls.selenium.quit()
        super().tearDownClass()

    def test_refresh_during_operation(self):
        try:
            # Navigate directly to the known URL:
            self.selenium.get('http://127.0.0.1:8000/feed/')
            logging.info('Page loaded successfully.')

            # Wait for the search input to be visible
            WebDriverWait(self.selenium, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#search-container input[name="query"]'))
            )

            # Find the search input and submit button
            search_input = self.selenium.find_element(By.CSS_SELECTOR, '#search-container input[name="query"]')
            search_button = self.selenium.find_element(By.CSS_SELECTOR, '#search-container button[type="submit"]')

            # Perform the search
            search_input.send_keys('quantum computing and cryptography')
            search_button.click()
            logging.info('Search executed with query: quantum computing and cryptography')

            # Wait a bit and then refresh
            time.sleep(2)
            self.selenium.refresh()
            logging.info('Page refreshed successfully.')

            # Ensure the search input is still there after refresh
            refreshed_search_input = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#search-container input[name="query"]'))
            )
            assert refreshed_search_input is not None
            logging.info('Search input presence confirmed post-refresh.')

        except Exception as e:
            logging.error('Error during test execution: %s', str(e))
            raise e



if __name__ == "__main__":
    TestPageRefresh()