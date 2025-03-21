from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class TestRepeatedQueries(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_repeated_queries_result_in_identical_responses(self):
        self.selenium.get('http://127.0.0.1:8000/feed/')

        # Perform the first search
        search_input = self.selenium.find_element(By.CSS_SELECTOR, '#search-container input[name="query"]')
        search_button = self.selenium.find_element(By.CSS_SELECTOR, '#search-container button[type="submit"]')
        query = "quantum computing and cryptography"
        search_input.send_keys(query)
        search_button.click()
        time.sleep(2)  # Allow time for results to load

        # Capture results
        results1 = self.selenium.find_elements(By.CSS_SELECTOR, '.card')  # Modify selector as needed

        # Perform the second search
        self.selenium.get('http://127.0.0.1:8000/feed/')  # Reload the page to reset state
        search_input = self.selenium.find_element(By.CSS_SELECTOR, '#search-container input[name="query"]')
        search_button = self.selenium.find_element(By.CSS_SELECTOR, '#search-container button[type="submit"]')
        search_input.send_keys(query)
        search_button.click()
        time.sleep(2)

        # Capture results
        results2 = self.selenium.find_elements(By.CSS_SELECTOR, '.card')  # Modify selector as needed

        # Compare results
        assert len(results1) == len(results2), "The number of results should be the same"
        for r1, r2 in zip(results1, results2):
            assert r1.text == r2.text, "The result contents should be identical"


if __name__ == "__main__":
    TestRepeatedQueries()
