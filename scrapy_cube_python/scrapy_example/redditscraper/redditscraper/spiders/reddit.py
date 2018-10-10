# -*- coding: utf-8 -*-
import scrapy


class RedditSpider(scrapy.Spider):
    name = 'reddit'
    allowed_domains = ['reddit.com']
    start_urls = ['http://reddit.com/']
    max_pages = 10
    seen_pages = 0

    def parse(self, response):
        threads = response.xpath('//div[@id="siteTable"]').css("div.link")
        # parse thread data; yield dicts containing desired data
        for th in threads:
            yield {
                "title": th.css("a.title").xpath("text()").extract_first(),
                "author": th.css("a.author").xpath("text()").extract_first(),
                "score": th.css("div.score.unvoted").xpath("@title").extract_first()
            }

            next_page = response.xpath('//span[@class="next-button"]//href').extract_first()
            if next_page is not None and self.seen_pages < self.max_pages:
                self.seen_pages += 1
            yield scrapy.Request(next_page, callback=self.parse)
