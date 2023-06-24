import requests
from bs4 import BeautifulSoup


def parse_url(url):
    try:
        html_content = requests.get(url)
    except requests.exceptions.ConnectionError:
        return None
    response = html_content.status_code
    soup = BeautifulSoup(html_content.content, 'html.parser')
    h1 = ' '.join(soup.find('h1').text.split()) if soup.find('h1') else ''
    title = soup.title.string if soup.title else ''
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if description_tag else ''
    return response, h1, title, description
