

import extruct
from w3lib.html import get_base_url

from ioc_finder import find_iocs
from bs4 import BeautifulSoup
import requests
import urllib.parse
from urllib.parse import urlparse
import html2text
import pprint
pp = pprint.PrettyPrinter(indent=4)
from boilerpy3 import extractors
import re
import json


def get(url, html):
    return extract_text(url, html)



def extract_text(url, html):

    # Get text from webpage



    extractor = extractors.ArticleExtractor()

    text = extractor.get_content(html)

    # Condenses all repeating newline characters into one single newline character

    text = '\n'.join([p for p in re.split('\n|\r', text) if len(p) > 0])


    record = [{
        '@type': 'schema:webpage',
        'schema:url': url,
        'schema:text': text
    }]



    return record