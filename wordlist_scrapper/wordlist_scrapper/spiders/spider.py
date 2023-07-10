from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item
import requests

def find_all_substrings(string, sub):

    import re
    starts = [match.start() for match in re.finditer(sub, string)]
    return starts

class WebsiteSpider(CrawlSpider):

    name = "webcrawler"

    crawl_count = 0
    words_found = 0     

    def __init__(self, surls=None, adomain=None, adeny=None, *args, **kwargs):
        self.start_urls = [f"{surls}"]
        domain2 = adomain.replace("www.","")
        self.allowed_domains = [f"{adomain}", f"{domain2}"]
        if adeny:
            self.rules = [Rule(LinkExtractor(deny=adeny), follow=True, callback="check_buzzwords")]
        else:
            self.rules = [Rule(LinkExtractor(), follow=True, callback="check_buzzwords")]
              
        super(WebsiteSpider, self).__init__(*args, **kwargs)

    def check_buzzwords(self, response):

        self.__class__.crawl_count += 1

        crawl_count = self.__class__.crawl_count

        wordlist = [
            r"\bchor\b",
            r"\bschulchor\b",
            "chöre",
            "choere",
            ]

        url = response.url
        contenttype = response.headers.get("content-type", "").decode('utf-8').lower()
        data = response.body.decode('utf-8').lower()

        for word in wordlist:
            substrings = find_all_substrings(data, word)
            for pos in substrings:
                ok = False
                if not ok:
                    self.__class__.words_found += 1
                    print(word + ";" + url + ";")
                    break
        return Item()

    def _requests_to_follow(self, response):
        if getattr(response, "encoding", None) != None:
                return CrawlSpider._requests_to_follow(self, response)
        else:
                return []