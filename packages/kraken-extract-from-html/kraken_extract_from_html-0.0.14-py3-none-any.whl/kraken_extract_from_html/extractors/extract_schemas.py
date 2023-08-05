import extruct
from w3lib.html import get_base_url


def get(url, html):
    return extract_schemas(url, html)


def extract_schemas(url, html):
    """ Extract schemas from webpage
    """

    schemas = []

    base_url = get_base_url(html, url)

    data = extruct.extract(html, base_url=base_url, uniform=True)

    for i in data:

        for p in data[i]:

            schemas.append(p)

    return schemas
