from urllib.parse import urljoin
from urllib.parse import urlparse
from scrapy.http import JsonRequest
import scrapy


class canoliveSpider(scrapy.Spider):
    # proxy_pool = [os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE1'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE2'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE3'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE4')]
    name = "cannolive"
    urls_vactor = [[["Epicerie fine"], "https://cannolive.fr/58-epicerie-fine", 13],
                   [["Huile d'Olive"], "https://cannolive.fr/48-huile-d-olive", 2],
                   [["Miels"], "https://cannolive.fr/14-miels", 3],
                   [["Confiseries"], "https://cannolive.fr/15-confiseries", 2],
                   [["Plantes & Aromates"], "https://cannolive.fr/16-plantes-et-aromates", 2],
                   [["Produits Bio"], "https://cannolive.fr/18-produits-bio", 1],
                   [["Cosmétique"], "https://cannolive.fr/52-cosmetique", 1],
                   [["Idées cadeaux"], "https://cannolive.fr/59-idees-cadeaux", 3]]

    url = ""
    cat = []
    item_url = []
    total_page = 1
    item = False
    page = 1

    def start_requests(self):
        data = self.urls_vactor.pop()
        self.cat = data[0]
        self.url = data[1]
        self.total_page = data[2]
        yield scrapy.Request(self.url,
                             callback=self.parse_api, dont_filter=True)
        # ,
        # meta={'proxy': random.choice(self.proxy_pool)})

    def parse_api(self, response):
        print(response.url)

        data = response.xpath('//*[contains(@class,"thumbnail")]/@href').extract()
        for d in data:
            self.item_url.append(d)
        if (self.page < self.total_page):
            self.page = self.page + 1
            url = self.url + "?page=" + str(self.page)
            yield scrapy.Request(url,
                                 callback=self.parse_api,
                                 dont_filter=True
                                 )
        else:
            self.item_url = list(dict.fromkeys(self.item_url))
            url = self.item_url.pop().replace("\\", "").strip()
            url = url.replace("\"", '')

            yield scrapy.Request(url,
                                 callback=self.parse_api_item,
                                 dont_filter=True
                                 )

    def parse_api_item(self, response):
        data = response.xpath('//*[contains(@class,"product-description")]/p/text()').extract()

        des = ""
        if len(data) >= 1:
            for d in data:
                des = des + d.strip()
        else:
            des = None
        yield {
            "url": response.url,

            "title": response.xpath('//*[contains(@class,"prodetail-tile")]/text()').extract()[0].strip(),

            "description": des,

            "categories": self.cat,

            "price": response.xpath('//*[contains(@itemprop,"price")]/text()').extract()[0].strip()[:-2],

            "currency": "EUR",

            "images": list(dict.fromkeys(response.xpath('//*[contains(@class,"thumb")]/@src').extract())),

            "extra": {
                "product-reference": response.xpath('//*[contains(@class,"product-reference")]/span/text()').extract()
            }}

        try:
            url = self.item_url.pop().replace("\\", "").strip()
            url = url.replace("\"", '')
            yield scrapy.Request(url,
                                 callback=self.parse_api_item, dont_filter=True)
        except:
            try:
                self.page = 1
                data = self.urls_vactor.pop()
                self.cat = data[0]
                self.url = data[1]
                self.total_page = data[2]
                yield scrapy.Request(self.url,
                                     callback=self.parse_api,
                                     dont_filter=True
                                     )
                # ,
                # meta={'proxy': random.choice(self.proxy_pool)})
            except:
                print(Exception, "b")
