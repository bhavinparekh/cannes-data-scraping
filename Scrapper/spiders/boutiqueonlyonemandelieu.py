from urllib.parse import urljoin
from scrapy.http import JsonRequest
import scrapy



class BouSpider(scrapy.Spider):
    # proxy_pool = [os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE1'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE2'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE3'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE4')]
    name = "boutiqueonlyonemandelieu"
    url="https://boutiqueonlyonemandelieu.fr/catalogue"
    item_url=[]
    item=False
    page=1
    def start_requests(self):
        yield scrapy.Request(self.url,
                                 callback=self.parse_api)
                                 # ,
                                 # meta={'proxy': random.choice(self.proxy_pool)})

    def parse_api(self, response):
        if self.item==False:
            print(self.page)

            data=response.css('a.product-grid::attr(href)').extract()
            for d in data:
                self.item_url.append(d)
            if (self.page<3):
                self.page=self.page+1
                url = "https://boutiqueonlyonemandelieu.fr/catalogue?page="+str(self.page)
                yield scrapy.Request(url,
                                         callback=self.parse_api)
            else:
                url=self.item_url.pop()
                print(url)
                yield JsonRequest(urljoin('https://boutiqueonlyonemandelieu.fr', url),
                                  callback=self.parse_api_item)
    def parse_api_item(self, response):

        yield {
            "url": response.url,

            "title": response.css('td.product-title h1::text').extract()[0].strip(),

            "description": None,

            "categories": response.css('div.product-info-grid a::text').extract()[0].strip().split(),

            "price":response.css('td.ProductActionTable-price span div span  span.integer::text').extract()[0].strip(),

            "currency": "EUR",

            "images": response.xpath('//div[@id="product-gallery"]/a/img/@src').extract(),

            "extra": {




            }}
        url = self.item_url.pop()
        print(url)
        yield JsonRequest(urljoin('https://boutiqueonlyonemandelieu.fr', url),
                          callback=self.parse_api_item)

