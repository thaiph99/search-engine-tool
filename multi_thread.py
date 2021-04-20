from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import requests
import re


class MultiThreadScraper:

    def __init__(self, base_url):

        self.base_url = base_url
        self.root_url = '{}://{}'.format(urlparse(self.base_url).scheme,
                                         urlparse(self.base_url).netloc)
        self.pool = ThreadPoolExecutor(max_workers=20)
        self.scraped_pages = set([])
        self.to_crawl = Queue()
        self.to_crawl.put(self.base_url)

    def parse_links(self, html):

        def is_valid(url1):
            return re.findall(r'\.[a-z]{3}', url1) and re.search(r'https://', url1)

        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            url = link['href']

            list_remove = ['#box_comment_vne', '#box_comment',
                           'https://youtube.com',
                           'https://twitter.com',
                           'https://facebook.com',
                           'https://www.facebook.com',
                           'https://www.twitter.com',
                           'https://www.youtube.com']

            for removee in list_remove:
                url = url.replace(removee, '')

            # if url.startswith('/') or url.startswith(self.root_url):
            #     url = urljoin(self.root_url, url)
            #     if url not in self.scraped_pages:
            #         self.to_crawl.put(url)

            if url not in self.scraped_pages and is_valid(url):
                self.to_crawl.put(url)

    def scrape_info(self, html):
        return

    def post_scrape_callback(self, res):
        result = res.result()
        if result and result.status_code == 200:
            self.parse_links(result.text)
            self.scrape_info(result.text)

    @staticmethod
    def scrape_page(url):
        try:
            res = requests.get(url, timeout=(3, 30))
            return res
        except requests.RequestException:
            return

    def run_scraper(self):
        cnt = 0
        while True:
            try:
                target_url = self.to_crawl.get(timeout=60)
                if target_url not in self.scraped_pages:
                    print("Scraping URL: {}".format(target_url))
                    print(cnt)
                    cnt += 1
                    self.scraped_pages.add(target_url)
                    job = self.pool.submit(self.scrape_page, target_url)
                    job.add_done_callback(self.post_scrape_callback)
            except Empty:
                return
            except Exception as e:
                print(e)
                continue


if __name__ == '__main__':
    s = MultiThreadScraper("http://www.vnexpress.net")
    s.run_scraper()
