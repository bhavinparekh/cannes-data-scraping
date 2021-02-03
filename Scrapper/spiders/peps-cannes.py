from urllib.parse import urljoin
from scrapy.http import JsonRequest
import scrapy


class pepsSpider(scrapy.Spider):
    # proxy_pool = [os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE1'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE2'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE3'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE4')]
    name = "peps-cannes"
    urls_vactor = [[["Robes Babydoll"], "https://peps-cannes.com/collections/robe-babydoll"],
                   [["Robes Pompadour Camouflage"], "https://peps-cannes.com/collections/robe-pompadour-camouflage"],
                   [["Robes Pompadour Rayées"], "https://peps-cannes.com/collections/robes-pompadour-vichy-rayees"],
                   [["Robes Pompadour Vichy"], "https://peps-cannes.com/collections/pompadour-vichy"],
                   [["Robes Pompadour Double Gaze"], "https://peps-cannes.com/collections/robes-pompadour-double-gaze"],
                   [["Robes Pompadour Brocard"], "https://peps-cannes.com/collections/robes-pompadour"],
                   [["Robes Valentine"], "https://peps-cannes.com/collections/robes-valentine"],
                   [["Robes Pompadour Toile De Jouy"], "https://peps-cannes.com/collections/pompadour-toile-de-jouy"],
                   [["Combinaisons"], "https://peps-cannes.com/collections/combinaison"],
                   [["Outlet"], "https://peps-cannes.com/collections/outlet"]]
    item_url = []
    item = False
    page = 0

    def start_requests(self):
        try:
            data = self.urls_vactor.pop()
            self.cat = data[0]
            self.url = data[1]
            yield scrapy.Request(self.url,
                                 callback=self.parse_api,
                                 dont_filter=True)

        except:
            pass

    def parse_api(self, response):
        if self.item == False:
            print(self.page)

            data = response.xpath('//*[contains(@class,"product-grid-item")]/@href').extract()
            for d in data:
                self.item_url.append("https://peps-cannes.com" + d)
            data = response.css('li a::attr(title)').extract()
            print(data)
            if "Suivant »" in data:
                self.page = self.page + 1
                url = self.url + "?page=" + str(self.page)
                yield scrapy.Request(url,
                                     callback=self.parse_api)
            else:

                url = self.item_url.pop()
                print(url)
                yield JsonRequest(url,
                                  callback=self.parse_api_item)

    def parse_api_item(self, response):
        data = response.xpath('//*[contains(@itemprop,"description")]/p/text()').extract()

        des = ""
        if len(data) >= 1:
            for d in data:
                des = des + d.strip()
        else:
            des = None
        data = response.xpath('//*[contains(@itemprop,"description")]/text()').extract()

        des = ""
        if len(data) >= 1:
            for d in data:
                des = des + d.strip()
        else:
            if (des==""):
                des = None
        yield {
            "url": response.url,

            "title": response.xpath('//*[contains(@itemprop,"name")]/text()').extract()[0].strip(),

            "description": des,

            "categories": self.cat,

            "price": response.xpath('//*[contains(@id,"productPrice-product-template")]/span/text()').extract()[0][1:],

            "currency": "EUR",

            "images": response.xpath('//*[contains(@class,"lazypreload")]/@src').extract(),

            "extra": {

            }}
        try:
            url = self.item_url.pop()
            yield JsonRequest(url,
                              callback=self.parse_api_item, dont_filter=True)
        except:
            try:
                data = self.urls_vactor.pop()
                self.cat = data[0]
                self.url = data[1]
                yield scrapy.Request(self.url,
                                     callback=self.parse_api,
                                     dont_filter=True
                                     )
                # ,
                # meta={'proxy': random.choice(self.proxy_pool)})
            except:
                print(Exception, "b")