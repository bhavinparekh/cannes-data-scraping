from urllib.parse import urljoin
from urllib.parse import urlparse
from scrapy.http import JsonRequest
import scrapy


class mavilleSpider(scrapy.Spider):
    # proxy_pool = [os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE1'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE2'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE3'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE4')]
    name = "mavillemonshopping"
    urls_vactor = [
        [["POUR L’APÉRO CE SOIR"], "https://www.mavillemonshopping.fr/fr/selections/pour-l-apero-ce-soir", 1],
        [["IDÉES CADEAUX !"], "https://www.mavillemonshopping.fr/fr/selections/idees-cadeaux", 1],
        [["OGONI"], "https://www.mavillemonshopping.fr/fr/cannes/cannes/ogoni", 2],
        [["JEUX ET DÉCO POUR ENFANTS"], "https://www.mavillemonshopping.fr/fr/selections/jeux-et-deco-pour-enfants", 1]]

    cat = []
    url = ""
    item_url = []
    item = False
    page = 1
    ui = "https://www.mavillemonshopping.fr/"

    def start_requests(self):
        try:
            data = self.urls_vactor.pop()
            self.cat = data[0]
            self.url = data[1]
            yield scrapy.Request(self.url,
                                 callback=self.parse_api,
                                 dont_filter=True)
            # ,
            # meta={'proxy': random.choice(self.proxy_pool)})
        except:
            pass
        # ,
        # meta={'proxy': random.choice(self.proxy_pool)})

    def parse_api(self, response):
        data = response.xpath('//*[contains(@class,"container-img")]/a/@href').extract()

        for d in data:
            self.item_url.append(d)
        data = response.css('a::attr(rel)').extract()

        if "next" in data:
            self.page = self.page + 1
            url = self.url + "?page=" + str(self.page)
            yield scrapy.Request(url,
                                 callback=self.parse_api)
        else:
            self.item_url = list(dict.fromkeys(self.item_url))
            url = self.item_url.pop()
            yield scrapy.Request(urljoin(self.ui, url),
                             callback=self.parse_api_item)

    def parse_api_item(self, response):

        data = response.xpath('//div[@id="product-description"]/p/text()').extract()
        des = ""
        if len(data) >= 1:
            for d in data:
                des = des + d.strip()
        else:
            des = None

        yield {
            "url": response.url,

            "title": response.xpath('//h1[@id="product-name"]/text()').extract()[0].strip(),

            "description": des,

            "categories": self.cat,

            "price": response.xpath('//span[@id="product-price"]/text()').extract()[0].strip()[:-1],

            "currency": "EUR",

            "images": response.xpath('//div[@class="bx-pager"]/a/div/img/@src').extract(),

            "extra": {

            }}

        if (len(self.item_url) != 0):
            url = self.item_url.pop()
            yield scrapy.Request(urljoin(self.ui, url),
                                 callback=self.parse_api_item)

        else:
            data = self.urls_vactor.pop()
            self.cat = data[0]
            self.url = data[1]
            yield scrapy.Request(self.url,
                                 callback=self.parse_api,
                                 dont_filter=True)
