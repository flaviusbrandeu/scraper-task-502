import argparse
from scrapy.crawler import CrawlerProcess
from keywords_scrapper.spiders.spider import WebsiteSpider
from scrapy.utils.project import get_project_settings


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("url",
                        help="url of website from which to start the scraper")
    args = parser.parse_args()
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(WebsiteSpider, args.url)
    process.start()  # the script will block here until the crawling is finished
