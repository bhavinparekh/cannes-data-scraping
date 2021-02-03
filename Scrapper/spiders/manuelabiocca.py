from urllib.parse import urljoin
from scrapy.http import JsonRequest
import scrapy


class menuSpider(scrapy.Spider):
    # proxy_pool = [os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE1'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE2'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE3'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE4')]
    name = "manuelabiocca"
    urls_vactor = [[["BIJOUX"], "https://www.manuelabiocca.com/shop/fr/16-bijoux"],
                   [["Corsets"], "https://www.manuelabiocca.com/shop/fr/13-corsets"],
                   [["Sacs"], "https://www.manuelabiocca.com/shop/fr/17-sacs"],
                   [["Accessoires"], "https://www.manuelabiocca.com/shop/fr/15-accessoires"],
                   [["Vêtements"], "https://www.manuelabiocca.com/shop/fr/14-vetements"],
                   [["Parures Florales"], "https://www.manuelabiocca.com/shop/fr/42-parures-florales"],
                   [["Deco Maison"], "https://www.manuelabiocca.com/shop/fr/46-deco-maison"],
                   [["Masques barrières"], "https://www.manuelabiocca.com/shop/fr/49-masques-barrieres"],
                   [["Doodoogoths"], "https://www.manuelabiocca.com/shop/fr/48-doodoogoths"],
                   [["Outlet"], "https://www.manuelabiocca.com/shop/fr/50-outlet"]]
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
            data = response.css('a.product_img_link::attr(href)').extract()
            for d in data:
                self.item_url.append(d)
            data = response.css('li.pagination_next ::attr(href)').extract()
            if (len(data) != 0):
                url = "https://www.manuelabiocca.com" + data[0]
                yield scrapy.Request(url,
                                     callback=self.parse_api)
            else:
                url = self.item_url.pop()
                print(url)
                yield JsonRequest(url,
                                  callback=self.parse_api_item)

    def parse_api_item(self, response):
        print(response.url)

        data = response.xpath('//div[@id="short_description_content"]/p/text()').extract()
        print(data)

        if len(data) >= 1:
            des = data[0].strip()
        else:
            des = None

        yield {
            "url": response.url,

            "title": response.xpath('//h1[@itemprop="name"]/text()').extract()[0].strip(),

            "description": des,

            "categories": self.cat,

            "price": response.xpath('//span[@id="our_price_display"]/text()').extract()[0].strip().split()[0],

            "currency": "EUR",

            "images": response.xpath('//ul[@id="thumbs_list_frame"]/li/a/@href').extract(),

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
