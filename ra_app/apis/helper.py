from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from habanero import Crossref
from sumy.models.dom import ObjectDocumentModel, Paragraph, Sentence
from sumy.nlp.tokenizers import Tokenizer
from os.path import dirname, join, abspath
from pycountry import languages
import sys

"""This module contains helper methods for testing Latent Semantic Analysis (LSA) summarizer obtained from sumy library.
https://github.com/miso-belica/sumy
build_document, build_sentence, expand_resource_path, load_resource, to_string, to_unicode, instance_to_unicode, to_bytes,
instance_to_bytes, get_stop_words, normalize_language, parse_stop_words
"""

_TOKENIZER = Tokenizer("czech")



PY3 = sys.version_info[0] == 3

if PY3:
    unicode = str
else:
    unicode = unicode

string_types = (str,) if PY3 else (bytes, unicode)


def normalise_data(articles):
    # Normalize the data
    normalized_articles = []
    for source, articles in articles.items():
        for article in articles:
            try:
                title = article['Title']
            except KeyError:
                raise

            normalized_articles.append({
                'Title': title,
                'Authors': article.get('Authors', ''),
                'Publication_Info': article.get('Publication Info', ''),
                'Abstract': article.get('Abstract', ''),
                'Link': article.get('Link', ''),
            })
    return normalized_articles


def eliminate_duplicates_and_combine(normalized_articles):
    unique_articles = []
    titles_seen = set()
    for article in normalized_articles:
        title = article['Title']
        if title not in titles_seen:
            unique_articles.append(article)
            titles_seen.add(title)
    return unique_articles


def find_doi(article_titles):
    cr = Crossref()
    dois = []
    for title in article_titles:
        search_results = cr.works(query=title, limit=1)
        for item in search_results['message']['items']:
            doi = item.get('DOI')
            dois.append(doi)
    return dois


def summarize_abstracts(combined_abstracts, model, tokenizer):
    summaries = []
    for abstract in combined_abstracts:
        inputs = tokenizer([abstract], max_length=1024, return_tensors="pt", truncation=True)
        summary_ids = model.generate(inputs["input_ids"], num_beams=4, max_length=300, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary)

    return summaries


def build_document(*sets_of_sentences):
    paragraphs = []
    for sentences in sets_of_sentences:
        sentence_instances = []
        for sentence_as_string in sentences:
            sentence = build_sentence(sentence_as_string)
            sentence_instances.append(sentence)

        paragraphs.append(Paragraph(sentence_instances))

    return ObjectDocumentModel(paragraphs)


def build_sentence(sentence_as_string, is_heading=False):
    return Sentence(sentence_as_string, _TOKENIZER, is_heading)


def expand_resource_path(path):
    base_dir = abspath(dirname(__file__) + "/../../")
    return join(base_dir, path)

def load_resource(path):
    path = expand_resource_path(path)
    with open(path, "rb") as file:
        return to_unicode(file.read())


def to_string(object):
    return to_unicode(object) if PY3 else to_bytes(object)

def to_unicode(object):
    if isinstance(object, unicode):
        return object
    elif isinstance(object, bytes):
        return object.decode("utf-8")
    else:
        # try decode instance to unicode
        return instance_to_unicode(object)


def instance_to_unicode(instance):
    if PY3:
        if isinstance(instance, str):
            return instance
        elif hasattr(instance, "__str__"):
            return str(instance)
    else:
        if hasattr(instance, "__unicode__"):
            return unicode(instance)
        elif hasattr(instance, "__str__"):
            return bytes(instance).decode("utf-8")

    return to_unicode(repr(instance))

def to_bytes(object):
    if isinstance(object, bytes):
        return object
    elif isinstance(object, unicode):
        return object.encode("utf-8")
    else:
        # try encode instance to bytes
        return instance_to_bytes(object)


def instance_to_bytes(instance):
    if PY3:
        if hasattr(instance, "__bytes__"):
            return bytes(instance)
        elif hasattr(instance, "__str__"):
            return str(instance).encode("utf-8")
    else:
        if hasattr(instance, "__str__"):
            return bytes(instance)
        elif hasattr(instance, "__unicode__"):
            return unicode(instance).encode("utf-8")

    return to_bytes(repr(instance))

def get_stop_words(language):
    language = normalize_language(language)
    try:
        stopwords_path = f"data/stopwords/{language}.txt"
        stopwords_data = load_resource(stopwords_path)
    except FileNotFoundError:
        raise LookupError("Stop-words are not available for language %s." % language)
    return parse_stop_words(stopwords_data)


def normalize_language(language):
    for lookup_key in ("alpha_2", "alpha_3"):
        try:
            lang = languages.get(**{lookup_key: language})
            if lang:
                language = lang.name.lower()
        except KeyError:
            pass

    return language.lower()

def parse_stop_words(data):
    return frozenset(w.rstrip() for w in to_unicode(data).splitlines() if w)