from bs4 import BeautifulSoup

from kraken_extract_from_html.extractors.extract_feeds import extract_feeds
from kraken_extract_from_html.extractors.extract_images import extract_images
from kraken_extract_from_html.extractors.extract_links import extract_links
from kraken_extract_from_html.extractors.extract_schemas import extract_schemas
from kraken_extract_from_html.extractors.extract_src import extract_src
from kraken_extract_from_html.extractors.extract_text import extract_text
from kraken_extract_from_html.extractors.extract_title import extract_title



def get(url, html):
    return process_extraction(url, html)

def kraken_extract_from_html(url, html):
    return process_extraction(url, html)


def process_extraction(url, html, image_urls = None):

    records = []

    
    text = extract_text(url, html)
    records+=text
    
    soup = _get_soup(html)


    links = extract_links(url, soup)
    records+=links


    images = extract_images(url, soup)
    records += images


    feeds = extract_feeds(url, soup)
    records += feeds

    schemas = extract_schemas(url, html)
    records += schemas

    src = extract_src(url, soup)
    records += src

    texts = extract_text(url, html)
    records += texts

    titles = extract_title(url, soup)
    records += titles


    return records




def _get_soup(html):

    soup = BeautifulSoup(html, 'html.parser')

    return soup




