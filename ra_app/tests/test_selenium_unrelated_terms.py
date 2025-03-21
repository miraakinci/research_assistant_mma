from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestPageRefresh(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_handling_incorrectly_written_terms(self):
        self.selenium.get(self.live_server_url + '/feed/')
        search_input = self.selenium.find_element(By.NAME, 'query')
        search_button = self.selenium.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

        # Input an incorrectly spelled search term
        search_term = "quantom compoting"
        search_input.send_keys(search_term)
        search_button.click()
        time.sleep(2)

        # Verify if the search suggests corrections or still returns relevant results
        suggestions = self.selenium.find_elements(By.CSS_SELECTOR, '.search-suggestion')
        results = self.selenium.find_elements(By.CSS_SELECTOR, '.result-item')

        assert len(suggestions) > 0 or len(
            results) > 0, "Search should handle typos by suggesting corrections or showing results"
