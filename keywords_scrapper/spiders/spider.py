from abc import ABC

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from keywords_scrapper.items import ScrapperItem
from urllib.parse import urlparse


class WebsiteSpider(CrawlSpider, ABC):
    name = "webcrawler"
    rules = [Rule(LinkExtractor(), follow=True, callback="send_item_to_db")]
    crawl_count = 0

    def __init__(self, website_url, *args, **kwargs):
        super(WebsiteSpider, self).__init__(*args, **kwargs)
        self.start_urls = [website_url]
        domain = urlparse(website_url).netloc
        self.allowed_domains = [domain]  # doesn't allow going to other sites

    def send_item_to_db(self, response):
        self.__class__.crawl_count += 1
        scraper_item = ScrapperItem()
        scraper_item['url'] = response.url
        scraper_item['text'] = response.text
        return scraper_item

    def _requests_to_follow(self, response):
        if getattr(response, "encoding", None) is not None:
            return CrawlSpider._requests_to_follow(self, response)
        else:
            return []
