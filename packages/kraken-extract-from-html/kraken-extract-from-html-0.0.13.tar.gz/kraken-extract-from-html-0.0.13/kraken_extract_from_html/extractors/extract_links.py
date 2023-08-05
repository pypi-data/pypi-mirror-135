


import urllib.parse

def get(url, soup):
    return extract_links(url, soup)


def extract_links(url, soup):

    links = []

    # Get links
    href_links = soup.find_all('a')
    
    for link in href_links:
        link_url = link.get('href', None)
        link_title = link.text

        # Clean link title
        link_title = link_title.replace('\n', '')
        link_title = link_title.replace('\r', '')
        link_title = link_title.replace('  ', ' ')
        link_title = link_title.strip()


        # Convert to absolute url
        link_url = urllib.parse.urljoin(url, link_url)

        # Compile into structured record
        link_record = {
            '@type': 'schema:webpage',
            'schema:title': link_title,
            'schema:url': link_url
        }

        # Add to list if url exist
        if link_record.get('schema:url', None):
            links.append(link_record)

    return links
