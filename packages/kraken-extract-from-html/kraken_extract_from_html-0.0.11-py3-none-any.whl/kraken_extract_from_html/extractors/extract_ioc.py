


from ioc_finder import find_iocs


def get(url, html):
    return extract_iocs(url, html)



def extract_iocs(url, html):


    iocs = find_iocs(html)

    schemas = []

    schemas += _extract_urls(url, iocs['urls'])
    schemas += _extract_emails(iocs['email_addresses'])

    return schemas

