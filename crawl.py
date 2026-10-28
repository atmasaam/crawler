from urllib.parse import urlsplit
from bs4 import BeautifulSoup, Tag

def normalize_url(domain):
    split_url = urlsplit(domain)
    result = split_url.netloc + split_url.path
    result = result.rstrip("/")
    return result

def get_heading_from_html(html:str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    h_tag = soup.find('h1')
    if h_tag == None:
        h_tag = soup.find('h2')
    if h_tag == None:
        return ""
    return h_tag.get_text(strip=True) 

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    p = soup.find('p')
    if p == None:
        return ""
    return p.get_text(strip=True)


