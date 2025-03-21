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
        search_term_with_typo = "quantum compoting and cryptography"
        search_input.send_keys(search_term_with_typo)
        search_button.click()
        wait = WebDriverWait(self.selenium, 30)
        results_with_typo = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.search-results-container .card .card-title')))
        results_with_typo_set = set([result.text for result in results_with_typo])

        # Wait for the page to load after the first search
        search_input = wait.until(EC.presence_of_element_located((By.NAME, 'query')))
        search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))

        # Input the correctly spelled search term
        search_input.clear()
        search_term_correct = "quantum computing and cryptography"
        search_input.send_keys(search_term_correct)
        search_button.click()
        results_correct = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.search-results-container .card .card-title')))
        results_correct_set = set([result.text for result in results_correct])

        # Calculate Jaccard similarity
        intersection = results_with_typo_set.intersection(results_correct_set)
        union = results_with_typo_set.union(results_correct_set)
        jaccard_similarity = len(intersection) / len(union) if union else 0

        # Count the number of identical results
        num_identical_results = len(intersection)

        # Assert that the Jaccard similarity and number of identical results are above a certain threshold
        assert jaccard_similarity > 0.7, f"Jaccard similarity ({jaccard_similarity}) is too low"
        assert num_identical_results > 0.5 * len(results_correct), "Too few identical results"

        # Additional assertions for suggestions or result count
        suggestions = self.selenium.find_elements(By.CSS_SELECTOR, '.search-suggestion')
        assert len(suggestions) > 0 or len(results_with_typo) > 0, "Search should handle typos by suggesting corrections or showing results"