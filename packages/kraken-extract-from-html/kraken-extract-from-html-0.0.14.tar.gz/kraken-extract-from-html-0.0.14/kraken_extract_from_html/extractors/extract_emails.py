



def get():
    return _extract_emails()

def extract_emails():
    return _extract_emails()



def _extract_emails(emails):

    schemas = []
    for email in emails:
        record = {
            '@type': 'schema:contactPoint',
            'schema:email': email
            }

        schemas.append(record)

    return schemas
