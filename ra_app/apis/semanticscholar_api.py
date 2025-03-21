from django.conf import settings
import requests
import pandas as pd
import time


class SemanticScholar(object):
    def __init__(self):
        self.base_url = "https://api.semanticscholar.org/graph/v1"
        self.headers = {"x-api-key": settings.SS_API_KEY}
        self.common_fields = "title,authors,year,venue,abstract,tldr,url,openAccessPdf"

    def send_request(self, method, endpoint, **kwargs):
        #delays for exponential backoff in seconds
        retry_delays = [1, 2, 4, 8]
        for delay in retry_delays:
            response = requests.request(method, endpoint, headers=self.headers, **kwargs)
            if response.status_code == 200:
                return response
            elif response.status_code == 429:
                # Rate limit exceeded retry after delay
                print(f"Rate limit exceeded. Retrying in {delay} seconds.")
                time.sleep(delay)
            else:
                self.log_error(response)
                break
        return None

    def fetch_papers(self, search_query):
        endpoint = f"{self.base_url}/paper/search"
        params = {
            "query": search_query,
            "fields": self.common_fields
        }

        response = self.send_request('GET', endpoint, params=params)
        if response:
            response_json = response.json()
            papers_list = self.process_papers_response(response_json.get("data", []))
            return pd.DataFrame(papers_list)
        else:
            print("Failed to fetch papers after retries.")
            return pd.DataFrame()

    def fetch_batch_doi(self, doi_list):
        endpoint = f"{self.base_url}/paper/batch"
        params = {"fields": self.common_fields}
        payload = {"ids": doi_list}
        response = self.send_request('POST', endpoint, params=params, json=payload)
        if response:
            papers_list = self.process_papers_response(response.json())
            return pd.DataFrame(papers_list)
        else:
            print("Failed to batch fetch DOIs after retries.")
            return pd.DataFrame()

    def process_papers_response(self, papers):
        papers_list = []
        for paper in papers:
            if paper is None:
                continue
            authors = paper.get("authors", [])
            authors_str = ', '.join([author.get("name", "") for author in authors])
            publication_info = f"{paper.get('year', '')}/{paper.get('venue', '')}"
            tldr = paper.get("tldr")
            link = self.get_paper_link(paper)

            papers_list.append({
                "Title": paper.get("title", ""),
                "Authors": authors_str,
                "Publication Info": publication_info,
                "Abstract": paper.get("abstract", ""),
                "Link": link,
                "TLDR": tldr.get("text", "") if tldr else ""
            })
        return papers_list

    def get_paper_link(self, paper):
        open_access_pdf_info = paper.get("openAccessPdf", {}) or {}
        pdf_url = open_access_pdf_info.get("url")

        if pdf_url:
            return pdf_url
        else:
            return paper.get("url", "Not available")

    def log_error(self, response):
        # Log error with status code and message
        print(f"Error {response.status_code}: {response.text}")