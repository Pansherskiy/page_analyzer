import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def normalize_url(url):
    scheme = urlparse(url).scheme
    netloc = urlparse(url).netloc
    normal_url = f'{scheme}://{netloc}'
    return normal_url


def parse_url(url):
    try:
        normal_url = normalize_url(url)
        html_content = requests.get(normal_url)
    except requests.exceptions.ConnectionError:
        return None
    response = html_content.status_code
    soup = BeautifulSoup(html_content.content, 'html.parser')
    h1 = ' '.join(soup.find('h1').text.split()) if soup.find('h1') else ''
    title = soup.title.string if soup.title else ''
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if description_tag else ''
    return response, h1, title, description
