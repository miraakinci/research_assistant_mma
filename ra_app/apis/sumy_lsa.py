from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


def summarize_lsa(input_text):
    # Split the text into sentences and get the first and last one
    sentences = input_text.strip().split('. ')
    first_sentence = sentences[0] + "."
    last_sentence = sentences[-1] if sentences[-1] != first_sentence else ""
    if last_sentence and not last_sentence.endswith('.'):
        last_sentence += "."

    # Combine first and last sentences for summarization
    text_to_summarize = first_sentence + " " + last_sentence

    # Parse the combined text
    parser = PlaintextParser.from_string(text_to_summarize, Tokenizer("english"))

    # Create an LSA summarizer
    summarizer = LsaSummarizer()

    # adjust sentences_count if needed
    summary = summarizer(parser.document, sentences_count=2)
    summary_text = ' '.join(str(sentence) for sentence in summary)
    return summary_text
