import sys, requests
from urllib.parse import urlsplit, urljoin
from crawl import extract_page_data, normalize_url

def main():
    if len(sys.argv) < 2:
        print("no website provided")
        exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        exit(1)

    # Start crawl with BASE_URL
    BASE_URL = sys.argv[1]
    print("starting crawl of:", BASE_URL)
    
    # Get html
    def get_html(url):
        r = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
        if r.status_code > 400:
            raise ConnectionError
        elif r.headers.get('content-type').split(";")[0] != "text/html":
            raise TypeError(r.headers.get('content-type'))
        return r.text


    def crawl_page(base_url, current_url = None, page_data=None):
        if current_url == None:
            current_url = base_url
            print("New crawl.")
        if urlsplit(current_url).netloc != urlsplit(base_url).netloc:
            print("Domains not equal, out of scope.")
            return
        normalized = normalize_url(current_url)
        if page_data == None:
            page_data = {}
        if normalized in page_data.keys(): 
            print("Page already indexed.")
            return
        html = get_html(current_url)
        result = extract_page_data(html, current_url)
        page_data[normalized] = result
        print("Got result")
        print(page_data)
        for url in result["outgoing_links"]:
            crawl_page(base_url, url, page_data)
        

    crawl_page(BASE_URL)



if __name__ == "__main__":
    main()
