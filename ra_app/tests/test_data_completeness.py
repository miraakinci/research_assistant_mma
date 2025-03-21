import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_data_completeness(driver):
    driver.get("http://localhost:8000/feed")  # Replace with your application's URL

    # Wait for the page to load completely
    WebDriverWait(driver, 20).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    # Find the search input field and enter a query
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#query-input"))
    )
    search_input.send_keys("quantum computing error correction")
    search_input.send_keys(Keys.RETURN)

    # Wait for the search results container to be present
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results-container"))
    )

    # Get the list of article elements
    article_elements = driver.find_elements(By.CSS_SELECTOR, ".card")

    # Check if all required fields are present for each article
    for article in article_elements:
        title = article.find_element(By.CSS_SELECTOR, ".card-title").text
        abstract = article.find_element(By.CSS_SELECTOR, ".card-text").text
        authors = article.find_element(By.CSS_SELECTOR, ".card-text.text-muted.mb-0").text
        publication_info = article.find_element(By.CSS_SELECTOR, ".card-text.text-muted.mb-0").text
        link = article.find_element(By.CSS_SELECTOR, ".card-link").get_attribute("href")

        # Add assertions to check if all required fields are present
        assert title, "Title is missing for an article"
        assert abstract, "Abstract is missing for an article"
        assert authors, "Authors are missing for an article"
        assert publication_info, "Publication information is missing for an article"
        assert link, "Link is missing for an article"

    # Delay for 5 seconds before the next test
    time.sleep(5)
