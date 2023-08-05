

import urllib.parse



def get(url, soup):
    return extract_feeds(url, soup)


def extract_feeds(url, soup):

    feeds = []

    ref_feeds = soup.findAll(type='application/rss+xml') + soup.findAll(type='application/atom+xml')

    for feed in ref_feeds:

        feed_url = feed.get('href', None)

        # Convert to absolute url
        feed_url = urllib.parse.urljoin(url, feed_url)

        # Compile into structured record
        feed_record = {
            '@type': 'schema:datafeed',
            'schema:title': feed.get('title', None),
            'schema:url': feed_url
        }
        
        # Skip if already in list
        if feed_record  in feeds:
            continue

        # Add to list if url exist
        if feed_record.get('schema:url', None):
            feeds.append(feed_record)
    
    return feeds
