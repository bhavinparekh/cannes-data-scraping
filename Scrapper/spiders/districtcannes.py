from urllib.parse import urljoin
from urllib.parse import urlparse
from scrapy.http import JsonRequest
import scrapy


class districtcannesSpider(scrapy.Spider):
    # proxy_pool = [os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE1'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE2'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE3'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE4')]
    name = "districtcannes"
    urls_vactor = [[["GENESIS"], "https://districtcannes.com/collections/hauts", 5],
                   [["ICHI"], "https://districtcannes.com/collections/bas", 1],
                   [["LA PETITE ETOILE"],
                    "https://districtcannes.com/collections/la-petite-etoile", 1],
                   [["ONE TEE"], "https://districtcannes.com/collections/robes", 1],
                   [["ACCESSOIRES"], "https://districtcannes.com/collections/accessoires", 1],
                   [["OUTLET GENESIS"], "https://districtcannes.com/collections/outlet-genesis", 7]]
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
                             callback=self.parse_api)

    def parse_api(self, response):
        print(response.url)

        data = response.xpath('//*[contains(@class,"full-width-link")]/@href').extract()
        print(data)
        for d in data:
            self.item_url.append("https://districtcannes.com" + d)

        if (self.page < self.total_page):
            self.page = self.page + 1
            url = self.url + "?page=" + str(self.page)
            yield scrapy.Request(url,
                                 callback=self.parse_api)
        else:
            self.item_url = list(dict.fromkeys(self.item_url))
            url = self.item_url.pop()
            print(url)
            yield JsonRequest(url,
                              callback=self.parse_api_item)

    def parse_api_item(self, response):
        data = response.xpath('//*[contains(@class,"product-single__description")]/p/span/text()').extract()
        des = ""
        if len(data) >= 1:
            for d in data:
                des = des + d.strip()
        else:
            pass
        data = response.xpath('//*[contains(@class,"product-single__description")]/p/text()').extract()
        if len(data) >= 1:
            for d in data:
                des = des + d.strip()
        else:
            des = None
        img = response.xpath('//*[contains(@class,"product-single__thumbnail-image")]/@src').extract()
        if (len(img) < 1):
            img = response.xpath('//*[contains(@class,"zoomImg")]/@src').extract()
        yield {
            "url": response.url,

            "title": response.xpath('//*[contains(@class,"product-single__title")]/text()').extract()[0].strip(),

            "description": des,

            "categories": self.cat,

            "price": response.xpath('//*[contains(@class,"price-item")]/text()').extract()[0].strip()[1:],

            "currency": "EUR",

            "images": img,

            "extra": {

            }}

        try:
            url = self.item_url.pop().replace("\\", "").strip()
            url = url.replace("\"", '')
            yield JsonRequest(url,
                              callback=self.parse_api_item)
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
