## About
This research project introduces a tool “Research Assistant” that can find relevant publications for your research question,
collecting data from three different resources: ACM Digital Library, Semantic Scholar Database, and ArXiv Database.
It provides links to the publications, details about the authors, other publication information and summaries of their abstracts.
Additionally, it offers a “combined summary” of the abstracts from three papers to provide an overview of the presented research topic.

## Installation
(use a virtual environment)
Install the requirements
pip install -r requirements.txt


## Usage
To run the project, run the following command:
```python manage.py runserver```

1. Click get started or scroll down.
2. Log in or sign up
3. Enter your research question click search
4. Read more links direct you to the pdf or the website of the paper.
5. Click save button to save an article to your favourites
6. Click library on right top corner to see your saved articles
7. Unsave with the unsave button
8. You can enter any other research question, enjoy using the tool!



## Code of Conduct
Research Assistant is committed to providing a friendly, safe and welcoming environment for all participants.
We expect all participants to abide by this Code of Conduct in all community interactions and events.
The development of this project adheres to the Code of Conduct established by the British Computing Society,
prioritising the protection of public health, privacy, security, and the welfare of individuals and the environment.
The lawful rights of third parties have been taken into consideration throughout the development process.
Furthermore, risks were regularly viewed and mitigating actions were revised accordingly.
Underpinning the dedication to ethical practices and social responsibility in the use of information technology, inclusivity of all sectors of society were taken into consideration.

## Run Tests
To run the tests, run the following commands:

python manage.py test ra_app.tests.test_data_processing
python manage.py test ra_app.tests.test_performance_metrics
python manage.py test ra_app.tests.test_selenium_query_length
python manage.py test ra_app.tests.test_selenium_incorrect_terms

pytest ra_app/tests/test_lsa_summarizer.py
pytest ra_app/tests/test_evaluation_rogue.py


## Unit Testing
python manage.py test ra_app.tests.test_views
python manage.py test ra_app.tests.test_models
python manage.py test ra_app.tests.test_forms


## first run the following command to start the server: python manage.py runserver, then on another terminal run the following command:
pytest ra_app/tests/test_data_completeness.py
python manage.py test ra_app.tests.test_selenium_page_refresh
pytest ra_app/tests/test_data_completeness.py
