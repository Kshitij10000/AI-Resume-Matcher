import re
from spacy.lang.en.stop_words import STOP_WORDS
import spacy

#model = spacy.load("en_core_web_lg")
          

def get_phone_numbers(string):
    r = re.compile(
        r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
    )
    phone_numbers = r.findall(string)
    return phone_numbers


def get_email_addresses(string):
    r = re.compile(r"[\w\.-]+@[\w\.-]+")
    return r.findall(string)


def get_urls(spacy_doc_parser):
    url_list = [token.text for token in spacy_doc_parser if token.like_url]
    return url_list


def get_locations(spacy_doc_parser):
    locations = [
        location.text for location in spacy_doc_parser.ents if location.label_.lower() == "loc"]
    return locations


def clean_resume(text: str):
    if not text:
        return
    spacy_doc_parser = model(text)
    replaces = []
    
    mobile_numbers = get_phone_numbers(text)
    replaces.extend(mobile_numbers)
    
    emails = get_email_addresses(text)
    replaces.extend(emails)
    
    urls = get_urls(spacy_doc_parser)
    replaces.extend(urls)

    for replace in replaces:
        text = text.replace(replace, "")
    return text

def remove_stopwords(text):
    doc = model(text)
    filtered_tokens = [token.text for token in doc if token.text not in STOP_WORDS]
    filtered_text = " ".join(filtered_tokens)
    filtered_text = filtered_text
    return filtered_text