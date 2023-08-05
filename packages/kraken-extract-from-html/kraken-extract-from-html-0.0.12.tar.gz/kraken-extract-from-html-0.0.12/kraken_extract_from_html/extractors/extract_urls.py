


def get(url, urls):
    return extract_urls(url, urls)



def extract_urls(url, urls):
    
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
