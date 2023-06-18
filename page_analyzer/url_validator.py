import validators


def validate_url(url):
    errors = []
    if url == '':
        errors.append('empty_url')
    if len(url) > 255:
        errors.append('very_long')
    if not validators.url(url):
        errors.append('invalid_url')
    return errors
