from urllib.parse import urljoin
from urllib.parse import urlparse
from scrapy.http import JsonRequest
import scrapy


class ptiSpider(scrapy.Spider):
    # proxy_pool = [os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE1'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE2'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE3'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE4')]
    name = "jeromedeoliveira"
    urls_vactor = [[["Les pâtisseries"], "https://jeromedeoliveira.com/27-les-patisseries", 2],
                   [["Choco'addict"], "https://jeromedeoliveira.com/10-choco-addict", 4],
                   [["Accros aux cakes"],
                    "https://jeromedeoliveira.com/11-accros-aux-cakes", 1],
                   [["Gourmandises de D'jé"], "https://jeromedeoliveira.com/17-gourmandises-de-d-je", 2]]
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

        data = response.xpath('//*[contains(@class,"thumbnail")]/@href').extract()
        for d in data:
            self.item_url.append(d)
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
                              callback=self.parse_api_item, dont_filter=True)

    def parse_api_item(self, response):
        data = response.xpath('//*[contains(@itemprop,"description")]/text()').extract()
        des = ""
        if len(data) >= 1:
            for d in data:
                des = des + d.strip()
        else:
            pass
        data = response.xpath('//*[contains(@itemprop,"description")]/p/text()').extract()
        if len(data) >= 1:
            for d in data:
                des = des + d.strip()
        else:
            if des == "":
                des = None
        t = response.xpath('//*[contains(@class,"h1")]/text()').extract()
        if len(t) != 0:
            yield {
                "url": response.url,

                "title": t,

                "description": des,

                "categories": self.cat,

                "price": response.xpath('//*[contains(@itemprop,"price")]/text()').extract()[0].strip().split()[0],

                "currency": "EUR",

                "images": response.xpath('//*[contains(@class,"js-qv-product-cover")]/@src').extract(),

                "extra": {

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
