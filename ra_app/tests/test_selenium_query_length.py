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

    def test_search_term_length_and_success(self):
        self.selenium.get(self.live_server_url + '/feed/')
        search_input = self.selenium.find_element(By.NAME, 'query')
        search_button = self.selenium.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

        # Perform the initial search
        initial_search_term = "quantum"
        search_input.send_keys(initial_search_term)
        search_button.click()
        wait = WebDriverWait(self.selenium, 60)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search-results-container')))

        search_terms = [
            "quantum computing",
            "quantum computing error correction",
            "implementation of quantum error correction techniques in scalable quantum computing architectures",
            "How does the implementation of quantum error correction techniques in scalable quantum computing architectures influence the overall system stability",
        ]

        for search_term in search_terms:
            search_input = self.selenium.find_element(By.NAME, 'query')
            search_button = self.selenium.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

            search_input.clear()
            search_input.send_keys(search_term)
            start_time = time.time()  # Record the start time
            search_button.click()
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search-results-container')))
            end_time = time.time()  # Record the end time
            response_time = end_time - start_time  # Calculate the response time

            # Check for the presence of results
            results = self.selenium.find_elements(By.CSS_SELECTOR, '.search-results-container .card')
            num_results = len(results)

            # Check for the presence of error messages
            error_message = self.selenium.find_elements(By.CSS_SELECTOR, '.error-message')

            # Define your success criteria (e.g., at least one result)
            success = num_results > 5

            # Record the search term length, number of results, success status, and response time
            print(f"Search term: '{search_term}' (length: {len(search_term.split())} words)")
            print(f"Number of results: {num_results}")
            print(f"Success: {success}")
            print(f"Response time: {response_time:.2f} seconds")
            print("---")

            # Add assertions or additional checks as needed
            assert success or len(error_message) > 0, "Should handle search terms gracefully"