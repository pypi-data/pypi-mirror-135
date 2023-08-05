from bs4 import BeautifulSoup


from .extractors import extract_feeds
from .extractors import extract_images
from .extractors import extract_links
from .extractors import extract_schemas
from .extractors import extract_src
from .extractors import extract_text
from .extractors import extract_title



def get(url, html):
    return process_extraction(url, html)



def process_extraction(url, html, image_urls = None):

    records = []

    
    text = extract_text.get(url, html)
    records+=text
    
    soup = _get_soup(html)


    links = extract_links.get(url, soup)
    records+=links


    images = extract_images.get(url, soup)
    records += images


    feeds = extract_feeds.get(url, soup)
    records += feeds

    schemas = extract_schemas.get(url, html)
    records += schemas

    src = extract_src.get(url, soup)
    records += src

    texts = extract_text.get(url, html)
    records += texts

    titles = extract_title.get(url, soup)
    records += titles


    return records




def _get_soup(html):

    soup = BeautifulSoup(html, 'html.parser')

    return soup




