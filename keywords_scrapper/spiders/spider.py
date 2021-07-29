from abc import ABC

from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item


def find_all_substrings(string, sub):
    import re
    starts = [match.start() for match in re.finditer(re.escape(sub), string)]
    return starts


class WebsiteSpider(CrawlSpider, ABC):
    name = "webcrawler"
    allowed_domains = ["devtomanager.com"]
    start_urls = ["https://devtomanager.com"]
    rules = [Rule(LinkExtractor(), follow=True, callback="check_keywords")]

    crawl_count = 0
    words_found = 0

    def check_keywords(self, response):

        self.__class__.crawl_count += 1

        crawl_count = self.__class__.crawl_count

        words = [
            "mentor",
            "Blog",
            "Developer to Manager",
        ]

        url = response.url
        content_type = response.headers.get("content-type", "").decode('utf-8').lower()
        data = response.body.decode('utf-8')

        for word in words:
            substrings = find_all_substrings(data, word)
            for pos in substrings:
                self.__class__.words_found += 1
                print(word + "," + url + ",")
        return Item()

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