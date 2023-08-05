

import urllib.parse




def get(url, soup):

    return extract_images(url, soup)




def extract_images(url, soup):

    images = []
    ref_images = soup.findAll('img')

    for img in ref_images:

        image_url = img.get('src', '')


        new_i = image_url
        if new_i.startswith('//'):
            new_i = 'https:' + new_i

        # Convert to absolute url
        image_url = urllib.parse.urljoin(url, new_i)

        # Compile into structured record
        image = {
            '@type': 'schema:ImageObject',
            'schema:title': img.get('title', None),
            'schema:contentUrl': new_i,
            'schema:url': url
        }
        
        # Skip if already in list
        if image in images:
            continue



        # POst thumbnail on image sharing site
            

        # Add to list if url exist
        if image.get('schema:contenturl', None):
            images.append(image)
    
    return images

