import unittest
import time
import psutil
from ra_app.apis.acm_api import ACM
from ra_app.apis.arxiv_api import Arxiv
from ra_app.apis.semanticscholar_api import SemanticScholar
from django.test import TestCase,Client
from django.urls import reverse


from ra_app.views import search_results_view

class TestPerformanceMetrics(unittest.TestCase):
    def setUp(self):
        # Create an instance of the client for our tests
        self.client = Client()
    def test_response_time(self):
        start_time = time.time()

        acm = ACM()
        arxiv = Arxiv()
        ss = SemanticScholar()

        # Run each function synchronously and handle their output
        df_acm = acm.acm("machine learning")
        df_arxiv = arxiv.arxiv_query("machine learning")
        df_ss = ss.fetch_papers("machine learning")

        end_time = time.time()

        # Calculate the duration
        duration = end_time - start_time
        print(f"Duration: {duration} seconds")
        acceptable_duration = 30  # Set to your acceptable threshold in seconds
        self.assertLessEqual(duration, acceptable_duration,
                             f"API request and web crawling should complete within {acceptable_duration} seconds. Actual time: {duration} seconds.")

    def test_resource_utilization(self):
        # Define the URL for your view (you may need to set up a URL in urls.py if not already done)
        url = reverse('search_results')  # Assume 'search_results' is the name of the URL pattern

        # Prepare POST data as expected by the view
        post_data = {'query': 'machine learning'}

        # Starting the measurement
        initial_cpu = psutil.cpu_percent(interval=1)
        initial_memory = psutil.virtual_memory().percent

        # Execute the function by sending a POST request
        response = self.client.post(url, post_data)

        # Ending the measurement
        final_cpu = psutil.cpu_percent(interval=1)
        final_memory = psutil.virtual_memory().percent

        # Define acceptable thresholds
        max_cpu_usage = 50  # percentage
        max_memory_usage = 60  # percentage

        print(f"Final cpu usage: {final_cpu}")
        print(f"Final memory usage: {final_memory}")

        self.assertLessEqual(final_cpu, max_cpu_usage,
                             f"CPU usage should not exceed {max_cpu_usage}%. Actual usage: {final_cpu}%.")
        self.assertLessEqual(final_memory, max_memory_usage,
                             f"Memory usage should not exceed {max_memory_usage}%. Actual usage: {final_memory}%.")