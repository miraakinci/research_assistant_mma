import unittest
from unittest.mock import patch
from ra_app.apis.helper import normalise_data, eliminate_duplicates_and_combine

class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        self.sample_articles = [
            {
                'Title': 'Article 1',
                'Authors': 'Author A, Author B',
                'Publication Info': 'Journal A, 2022',
                'Abstract': 'This is the abstract for Article 1.',
                'Link': 'https://example.com/article1'
            },
            {
                'Title': 'Article 2',
                'Authors': 'Author C',
                'Publication Info': 'Conference B, 2021',
                'Abstract': 'This is the abstract for Article 2.',
                'Link': 'https://example.com/article2'
            },
            {
                'Title': 'Article 3',
                'Authors': 'Author A, Author D',
                'Publication Info': 'Journal A, 2022',
                'Abstract': 'This is the abstract for Article 3.',
                'Link': 'https://example.com/article3'
            },
            {
                'Title': 'Article 4',
                'Authors': 'Author E',
                'Publication Info': 'Conference B, 2021',
                'Abstract': 'This is the abstract for Article 4.',
                'Link': 'https://example.com/article4'
            }
        ]

    def test_data_normalization_accuracy(self):
        # Normalize the data
        normalized_articles = normalise_data({'source': self.sample_articles})

        # Check if the normalized data matches the original data
        for i, article in enumerate(normalized_articles):
            self.assertEqual(article['Title'], self.sample_articles[i]['Title'])
            self.assertEqual(article['Authors'], self.sample_articles[i]['Authors'])
            self.assertEqual(article['Publication_Info'], self.sample_articles[i]['Publication Info'])  # Corrected key
            self.assertEqual(article['Abstract'], self.sample_articles[i]['Abstract'])
            self.assertEqual(article['Link'], self.sample_articles[i]['Link'])

        # Calculate the data normalization accuracy
        accuracy = len(normalized_articles) / len(self.sample_articles) * 100
        print(f"Data Normalization Accuracy: {accuracy}%")
        self.assertGreaterEqual(accuracy, 95, "Data normalization accuracy should be at least 95%")

    def test_duplicate_detection_rate(self):
        # Normalize the data
        normalized_articles = normalise_data({'source': self.sample_articles})

        # Introduce some duplicate articles explicitly by copying exact entries
        normalized_articles.append(dict(normalized_articles[0]))  # Duplicate of the first article
        normalized_articles.append(dict(normalized_articles[2]))  # Duplicate of the third article

        # Eliminate duplicates and combine the articles
        unique_articles = eliminate_duplicates_and_combine(normalized_articles)

        # Calculate the duplicate detection rate
        total_duplicates = 2  # Since you manually added 2 duplicates
        detected_duplicates = len(normalized_articles) - len(unique_articles)
        duplicate_detection_rate = detected_duplicates / total_duplicates * 100
        print(f"Duplicate Detection Rate: {duplicate_detection_rate}%")
        self.assertGreaterEqual(duplicate_detection_rate, 90, "Duplicate detection rate should be at least 90%")

if __name__ == '__main__':
    unittest.main()
