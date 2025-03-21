import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time


class ACM(object):
    def __init__(self):
        pass

    # construct the search query for ACM, pageSize : number of papers per page
    def payload_params(self, keyword, st_page=0, pasize=10):
        params = (
            ("AllField", keyword),
            ("queryID", "45/3852851837"),
            ("sortBy", "relevancy"),
            ("startPage", str(st_page)),
            ("pageSize", str(pasize)),
        )
        response = requests.get(
            "https://dl.acm.org/action/doSearch",
            params=params,
            headers={"accept": "application/json"},
        )
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def soup_lookup_html(self, soup):
        all_papers = []
        main_class = soup.find(
            "div", {"class": "col-lg-9 col-md-9 col-sm-8 sticko__side-content"}
        )
        main_c = main_class.find_all("div", {"class": "issue-item__content"})
        for paper in main_c:
            temp_data = {}
            doi_url = ["https://dl.acm.org", "doi", "pdf"]
            try:
                content_ = paper.find("h5", {"class": "issue-item__title"})
                paper_url = content_.find("a", href=True)["href"].split("/")
                doi_url.extend(paper_url[2:])
                title = content_.text
                temp_data["Title"] = title
                temp_data["Link"] = "/".join(doi_url)
                all_papers.append(temp_data)
            except Exception as e:
                pass
        df = pd.DataFrame(all_papers)
        return df

    def acm(self, keyword, api_wait=5):
        # Fetch data from ACM
        acm_soup = self.payload_params(keyword, st_page=0, pasize=10)
        acm_result = self.soup_lookup_html(acm_soup)
        time.sleep(api_wait)

        return acm_result.reset_index(drop=True)

