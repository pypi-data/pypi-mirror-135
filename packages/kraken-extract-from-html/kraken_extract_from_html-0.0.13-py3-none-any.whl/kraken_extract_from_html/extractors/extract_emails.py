

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


def get():
    return _extract_emails()

def extract_emails():
    return _extract_emails()



def _extract_emails(emails):

    schemas = []
    for email in emails:
        record = {
            '@type': 'schema:contactPoint',
            'schema:email': email
            }

        schemas.append(record)

    return schemas
