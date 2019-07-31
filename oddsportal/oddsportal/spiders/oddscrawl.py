# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import OddsportalItem
from scrapy_splash import SplashRequest
from scrapy_splash.response import SplashTextResponse, SplashJsonResponse
from scrapy.http import HtmlResponse
from scrapy import Request

class OddsSpider(CrawlSpider):
    name = 'odds'
    allowed_domains = ['www.oddsportal.com']

    start_urls = ['https://www.oddsportal.com/soccer/africa/africa-cup-of-nations/results/']

    #def start_requests(self):
      #  yield SplashRequest(self.link, args={'wait': 4}, meta={'real_url': self.link})


    rules = (
       # Rule(LinkExtractor(allow=('/soccer/'),
                #           deny=('/standings/')), process_request='use_splash'),
        Rule(LinkExtractor(allow=(r'/soccer/[a-z-]+/[a-z0-9-]+/[a-zA-Z0-9-]+/'),
                           deny=("/soccer/[a-z-]+/[a-z0-9-]+/results",
                                 "/soccer/[a-z-]+/[a-z0-9-]+/standing",
                                 )), callback='parse_items', process_request='use_splash', follow=True)
    )


    def _requests_to_follow(self, response):
        if not isinstance(
                response,
                (HtmlResponse, SplashJsonResponse, SplashTextResponse)):
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)




    #def splash_request(self, request):
      #  return SplashRequest(url=request.url, args={'wait': 4}, meta={'real_url': request.url})

    def use_splash(self, request):
        request.meta.update(splash={
            'args': {
                'wait': 1,
            },
            'endpoint': 'render.html',
        })
        return request


    def parse_items(self,response):

        items = OddsportalItem()
        items['country'] = response.css("a:nth-child(4)::text").get()
        items['liga'] = response.css("a:nth-child(5)::text").get()
        items['teams'] = response.css("h1::text").get()
        items['data'] = response.css(".t1559221200-4-1-1-1::text").get()
        yield items
        SplashRequest()