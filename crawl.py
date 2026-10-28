from urllib.parse import urlsplit, urljoin
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

def get_urls_from_html(html:str, base_url:str) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    urls = soup.find_all('a')
    resultlist = []
    for url in urls:
        resultlist.append(urljoin(base_url, url.get('href')))
    return resultlist

def get_images_from_html(html:str, base_url:str) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    imgs = soup.find_all('img')
    resultlist = []
    for img in imgs:
        if img.get('src') != "": 
            resultlist.append(urljoin(base_url, img.get('src')))
    return resultlist
