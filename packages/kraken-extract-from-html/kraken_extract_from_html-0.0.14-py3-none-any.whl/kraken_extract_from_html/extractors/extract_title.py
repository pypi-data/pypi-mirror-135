

def get(url, soup):
    return extract_title(url, soup)



def extract_title(url, soup):
    
    if soup.title:
        title = soup.title.string


        record = {
            '@type': 'schema:WebPage',
            'schema:url': url,
            'schema:headline': title
        }


        return [record]
    return []


