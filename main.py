import sys, requests, asyncio, aiohttp
from urllib.parse import urlsplit, urljoin
from crawl import extract_page_data, normalize_url

class AsyncCrawler:
    def __init__(self, base_url, max_conc, max_pages):
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data = {}
        self.visited = set()
        self.lock = asyncio.Lock()
        self.max_concurrency = max_conc
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        if self.should_stop == True:
            return False
        async with self.lock:
            if normalized_url in self.visited:
                return False
            elif len(self.visited) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                return False
            else:
                self.visited.add(normalized_url)
                return True

    async def get_html(self, url):
        async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as r:
            if r.status > 400:
                raise ConnectionError
            elif r.headers.get('content-type').split(";")[0] != "text/html":
                raise TypeError(r.headers.get('content-type'))
            resp = await r.text()
            return resp

    async def crawl_page(self, url):
        if self.should_stop == True:
            return
        if urlsplit(url).netloc != urlsplit(self.base_url).netloc:
            return
        
        normalized = normalize_url(url)

        added_visit = await self.add_page_visit(normalized)
        if added_visit == False:
            return
        
        async with self.semaphore:
            html = await self.get_html(url)
            result = extract_page_data(html, url)

            async with self.lock:
                self.page_data[normalized] = result
                print("Wrote result", url)

        task_list = set()
        for url in result["outgoing_links"]:
            task = asyncio.create_task(self.crawl_page(url))
            task_list.add(task)
            self.all_tasks.add(task)
        try:    
            await asyncio.gather(*task_list)
        finally:
            for task in task_list:
                self.all_tasks.remove(task)
        
    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data
        
async def crawl_site_async(url, max_conc, max_pages):
    async with AsyncCrawler(url, max_conc, max_pages) as crawler:
        resp = await crawler.crawl()
        return resp

async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        exit(1)
    elif len(sys.argv) > 4:
        print("too many arguments provided")
        exit(1)

    # Start crawl with BASE_URL
    BASE_URL = sys.argv[1]
    if len(sys.argv) > 2:
        MAX_CONC = int(sys.argv[2])
    else:
        MAX_CONC = 10
    if len(sys.argv) > 3:
        MAX_PAGES = int(sys.argv[3])
    else:
        MAX_PAGES = 50
        
    
    print("starting crawl of:", BASE_URL)    
    page_data = await crawl_site_async(BASE_URL, MAX_CONC, MAX_PAGES)
    for page in page_data:
        print(page)

 

if __name__ == "__main__":
    asyncio.run(main())
