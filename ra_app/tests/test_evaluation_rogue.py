# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from pytest import approx

from sumy.evaluation import rouge_n, rouge_l_sentence_level, rouge_l_summary_level
from ra_app.evaluation.rogue import get_ngrams, split_into_words, get_word_ngrams, len_lcs, recon_lcs, union_lcs
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser


def test_get_ngrams():
    assert not get_ngrams(3, "")

    correct_ngrams = [("t", "e"), ("e", "s"), ("s", "t"),
                      ("t", "i"), ("i", "n"), ("n", "g")]
    found_ngrams = get_ngrams(2, "testing")
    print(f"Correct n-grams: {correct_ngrams}")
    print(f"Found n-grams: {found_ngrams}")

    assert len(correct_ngrams) == len(found_ngrams)
    for ngram in correct_ngrams:
        assert ngram in found_ngrams


def test_split_into_words():
    sentences1 = PlaintextParser.from_string("One, two two. Two. Three.", Tokenizer("english")).document.sentences
    words1 = split_into_words(sentences1)
    print(f"Words from sentences1: {words1}")
    assert ["One", "two", "two", "Two", "Three"] == words1

    sentences2 = PlaintextParser.from_string("two two. Two. Three.", Tokenizer("english")).document.sentences
    words2 = split_into_words(sentences2)
    print(f"Words from sentences2: {words2}")
    assert ["two", "two", "Two", "Three"] == words2


def test_get_word_ngrams():
    sentences = PlaintextParser.from_string("This is a test.", Tokenizer("english")).document.sentences
    expected_ngrams = {("This", "is"), ("is", "a"), ("a", "test")}
    found_ngrams = get_word_ngrams(2, sentences)
    print(f"Expected n-grams: {expected_ngrams}")
    print(f"Found n-grams: {found_ngrams}")

    assert expected_ngrams == found_ngrams


def test_ngrams_for_more_sentences_should_not_return_words_at_boundaries():
    sentences = PlaintextParser.from_string("This is a pencil.\nThis is a eraser.\nThis is a book.", Tokenizer("english")).document.sentences
    expected_ngrams = {("This", "is"), ("is", "a"), ("a", "pencil"), ("a", "eraser"), ("a", "book")}
    found_ngrams = get_word_ngrams(2, sentences)
    print(f"Expected n-grams: {expected_ngrams}")
    print(f"Found n-grams: {found_ngrams}")

    assert expected_ngrams == found_ngrams


def test_len_lcs():
    lcs_len1 = len_lcs("1234", "1224533324")
    print(f"Length of LCS for '1234' and '1224533324': {lcs_len1}")
    assert lcs_len1 == 4

    lcs_len2 = len_lcs("thisisatest", "testing123testing")
    print(f"Length of LCS for 'thisisatest' and 'testing123testing': {lcs_len2}")
    assert lcs_len2 == 7


def test_recon_lcs():
    lcs1 = recon_lcs("1234", "1224533324")
    print(f"LCS for '1234' and '1224533324': {lcs1}")
    assert lcs1 == ("1", "2", "3", "4")

    lcs2 = recon_lcs("thisisatest", "testing123testing")
    print(f"LCS for 'thisisatest' and 'testing123testing': {lcs2}")
    assert lcs2 == ("t", "s", "i", "t", "e", "s", "t")


def test_rouge_n():
    candidate_text = "pulses may ease schizophrenic voices"
    candidate = PlaintextParser(candidate_text, Tokenizer("english")).document.sentences

    reference1_text = "magnetic pulse series sent through brain may ease schizophrenic voices"
    reference1 = PlaintextParser(reference1_text, Tokenizer("english")).document.sentences

    reference2_text = "yale finds magnetic stimulation some relief to schizophrenics imaginary voices"
    reference2 = PlaintextParser.from_string(reference2_text, Tokenizer("english")).document.sentences

    rouge_n_score1 = rouge_n(candidate, reference1, 1)
    print(f"ROUGE-1 score (candidate vs reference1): {rouge_n_score1}")
    assert rouge_n_score1 == approx(4/10)

    rouge_n_score2 = rouge_n(candidate, reference2, 1)
    print(f"ROUGE-1 score (candidate vs reference2): {rouge_n_score2}")
    assert rouge_n_score2 == approx(1/10)

    rouge_n_score3 = rouge_n(candidate, reference1, 2)
    print(f"ROUGE-2 score (candidate vs reference1): {rouge_n_score3}")
    assert rouge_n_score3 == approx(3/9)

    rouge_n_score4 = rouge_n(candidate, reference2, 2)
    print(f"ROUGE-2 score (candidate vs reference2): {rouge_n_score4}")
    assert rouge_n_score4 == approx(0/9)

    rouge_n_score5 = rouge_n(candidate, reference1, 3)
    print(f"ROUGE-3 score (candidate vs reference1): {rouge_n_score5}")
    assert rouge_n_score5 == approx(2/8)

    rouge_n_score6 = rouge_n(candidate, reference2, 3)
    print(f"ROUGE-3 score (candidate vs reference2): {rouge_n_score6}")
    assert rouge_n_score6 == approx(0/8)

    rouge_n_score7 = rouge_n(candidate, reference1, 4)
    print(f"ROUGE-4 score (candidate vs reference1): {rouge_n_score7}")
    assert rouge_n_score7 == approx(1/7)

    rouge_n_score8 = rouge_n(candidate, reference2, 4)
    print(f"ROUGE-4 score (candidate vs reference2): {rouge_n_score8}")
    assert rouge_n_score8 == approx(0/7)

    # These tests will apply when multiple reference summaries can be input
    # assert rouge_n(candidate, [reference1, reference2], 1) == approx(5/20)
    # assert rouge_n(candidate, [reference1, reference2], 2) == approx(3/18)
    # assert rouge_n(candidate, [reference1, reference2], 3) == approx(2/16)
    # assert rouge_n(candidate, [reference1, reference2], 4) == approx(1/14)


def test_rouge_l_sentence_level():
    reference_text = "police killed the gunman"
    reference = PlaintextParser(reference_text, Tokenizer("english")).document.sentences

    candidate1_text = "police kill the gunman"
    candidate1 = PlaintextParser(candidate1_text, Tokenizer("english")).document.sentences

    candidate2_text = "the gunman kill police"
    candidate2 = PlaintextParser(candidate2_text, Tokenizer("english")).document.sentences

    candidate3_text = "the gunman police killed"
    candidate3 = PlaintextParser(candidate3_text, Tokenizer("english")).document.sentences

    rouge_l_score1 = rouge_l_sentence_level(candidate1, reference)
    print(f"ROUGE-L score (candidate1 vs reference): {rouge_l_score1}")
    assert rouge_l_score1 == approx(3/4)

    rouge_l_score2 = rouge_l_sentence_level(candidate2, reference)
    print(f"ROUGE-L score (candidate2 vs reference): {rouge_l_score2}")
    assert rouge_l_score2 == approx(2/4)

    rouge_l_score3 = rouge_l_sentence_level(candidate3, reference)
    print(f"ROUGE-L score (candidate3 vs reference): {rouge_l_score3}")
    assert rouge_l_score3 == approx(2/4)


def test_union_lcs():
    reference_text = "one two three four five"
    reference = PlaintextParser(reference_text, Tokenizer("english")).document.sentences

    candidate_text = "one two six seven eight. one three eight nine five."
    candidates = PlaintextParser(candidate_text, Tokenizer("english")).document.sentences

    union_lcs_score = union_lcs(candidates, reference[0])
    print(f"Union LCS score: {union_lcs_score}")
    assert union_lcs_score == approx(4/5)


def test_rouge_l_summary_level():
    reference_text = "one two three four five. one two three four five."
    reference = PlaintextParser(reference_text, Tokenizer("english")).document.sentences

    candidate_text = "one two six seven eight. one three eight nine five."
    candidates = PlaintextParser(candidate_text, Tokenizer("english")).document.sentences

    rouge_l_summary_score = rouge_l_summary_level(candidates, reference)
    print(f"ROUGE-L summary level score: {rouge_l_summary_score}")
