import urllib.parse
from urllib.parse import urlparse

def get(url, soup):
    return extract_src(url, soup)


def extract_src(url, soup):

    urls = []
    tag_list = soup.findAll(lambda tag: 'src' in tag.attrs)

    if not tag_list:
        return []

    for t in tag_list:
        
        src_url = t['src']

        # Correct for relative path if required, don't if not as it may point elsewhere
        if not src_url.startswith('http') or not src_url.startswith('//'):
            src_url = urllib.parse.urljoin(url, t['src'])
        
        urls.append(src_url)
        
    return _extract_urls(url, urls)


def _extract_urls(url, urls):
    
    if not isinstance(urls, list):
        urls = [urls]


    schemas = []

    for i in urls:
        new_i = i
        if new_i.startswith('//'):
            new_i = 'https:' + new_i

        new_i = new_i.lower()
        file_name = new_i.split('?')


        image_list = ['.jpeg', '.jpg', '.gif', '.png']
        video_list = ['.mp4', '.mpg', '.mpeg', '.mov']
        
        if any(file_name[0].endswith(s) for s in image_list):
            record = {
                '@type': 'schema:imageObject',
                'schema:url': url,
                'schema:contentUrl': new_i
                }

            schemas.append(record)

        elif any(file_name[0].endswith(s) for s in video_list):
            record = {
            '@type': 'schema:videoObject',
            'schema:url': url,
            'schema:contentUrl': new_i
            }

            schemas.append(record)

        else:
            #todo returns too many schemas
            a=1
            '''
            record = {
            '@type': 'schema:digitalDocument',
            'schema:url': url
            }

            schemas.append(record)
            '''

    return schemas