import requests
import pandas as pd
import time
import xmltodict


class Arxiv(object):
    def __init__(self):
        pass

    def arxiv_query(self, query, max_results=10):
        base_url = "https://export.arxiv.org/api/query?"
        query_params = {
            "search_query": query,
            "start": 0,
            "max_results": max_results
        }

        headers = {
            "Accept": "application/atom+xml",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        }

        response = requests.get(base_url, params=query_params, headers=headers)

        if response.status_code != 200:
            print("Failed:", response.status_code)
            return

        data_dict = xmltodict.parse(response.content)
        articles_df = pd.DataFrame(columns=["Title", "Authors", "Link", "Publication Info", "Abstract"])

        feed_entries = data_dict['feed'].get('entry', [])
        if not isinstance(feed_entries, list):
            feed_entries = [feed_entries]

        for entry in feed_entries:
            title = entry['title'].strip()
            #arxiv api output summary is the abstract of the paper
            abstract = entry['summary'].strip()
            # Normalize links and extract PDF link
            links = entry.get('link', [])
            if not isinstance(links, list):
                links = [links]
            pdf_link = next((link['@href'] for link in links if link.get('@title') == 'pdf'), None)

            pub_info = entry.get('published', "Not Available").strip()

            # Normalize authors to a list and join their names
            authors_data = entry.get('author', [])
            if not isinstance(authors_data, list):
                authors_data = [authors_data]
            authors = ', '.join([author['name'] for author in authors_data])

            new_row = pd.DataFrame([{
                "Title": title,
                "Authors": authors,
                "Link": pdf_link or "No PDF link available",
                "Publication Info": pub_info,
                "Abstract": abstract
            }], index=[0])

            articles_df = pd.concat([articles_df, new_row], ignore_index=True)

        time.sleep(3)
        return articles_df
