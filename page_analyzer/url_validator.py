import validators


def validate_url(url):
    errors = []
    if url == '':
        errors.append('empty_url')
    elif len(url) > 255:
        errors.append('very_long')
    elif not validators.url(url):
        errors.append('invalid_url')
    return errors
