

from boilerpy3 import extractors
import re


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