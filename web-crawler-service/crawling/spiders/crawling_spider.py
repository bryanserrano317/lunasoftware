import scrapy
import logging
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawling.middlewares import DomainFilterMiddleware


class CrawlingSpider(CrawlSpider):
    name = "crawling"
    allowed_domains = ['leetcode.com']
    start_urls = ["https://leetcode.com/problemset/"]
    handle_httpstatus_list = [404, 403, 302]

    rules = (
        Rule(LinkExtractor(allow="/", deny=("contact-us", "patient-portal")), callback="parse_item"),
    )

    def parse_item(self, response):
        if response.status != 404 and response.status != 403:
            title = response.css("p::text").getall()
            text = response.css("li::text").getall()
            
            if title and text:
                yield {
                    "url": response.url,
                    "title": title,
                    "text": response.css("li::text").get().replace("\n", "").replace(" ", "").strip(),
                }

    def closed(self, reason):
        logging.info("Scrapy finished. Reason: %s", reason)


