from abc import ABC

from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import ScrapperItem


class WebsiteSpider(CrawlSpider, ABC):
    name = "webcrawler"
    allowed_domains = ["devtomanager.com"]
    start_urls = ["https://devtomanager.com"]
    rules = [Rule(LinkExtractor(), follow=True, callback="send_item_to_db")]
    crawl_count = 0

    def send_item_to_db(self, response):
        self.__class__.crawl_count += 1
        item = ScrapperItem()
        item['url'] = response.url
        return item

    def _requests_to_follow(self, response):
        if getattr(response, "encoding", None) is not None:
            return CrawlSpider._requests_to_follow(self, response)
        else:
            return []


if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(WebsiteSpider)
    process.start()  # the script will block here until the crawling is finished
