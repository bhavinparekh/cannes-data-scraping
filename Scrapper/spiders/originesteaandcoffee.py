from urllib.parse import urljoin
from scrapy.http import JsonRequest
import scrapy


class otcSpider(scrapy.Spider):
    # proxy_pool = [os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE1'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE2'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE3'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE4')]
    name = "originesteaandcoffee"
    urls_vactor = [[["Les ateliers"], "http://www.originesteaandcoffee.com/800-les-ateliers", 1],
                   [["Cafés"], "http://www.originesteaandcoffee.com/821-nos-cafes", 5],
                   [["Thés"],
                    "http://www.originesteaandcoffee.com/822-nos-thes", 31],
                   [["Nos Infusions"], "http://www.originesteaandcoffee.com/823-nos-infusions", 14],
                   [["Epicerie Sucrée"], "http://www.originesteaandcoffee.com/824-epicerie-sucree", 5],
                   [["Accessoires"], "http://www.originesteaandcoffee.com/976-accessoires", 15],

                   ]

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
        if self.item == False:
            print(self.page)

            data = response.css('a.product_img_link::attr(href)').extract()
            for d in data:
                self.item_url.append(d)
            if (self.page < self.total_page):
                self.page = self.page + 1
                url = self.url + "?p=" + str(self.page)
                yield scrapy.Request(url,
                                     callback=self.parse_api)
            else:
                self.item_url = list(dict.fromkeys(self.item_url))
                url = self.item_url.pop()
                print(url)
                yield JsonRequest(url,
                                  callback=self.parse_api_item)

    def parse_api_item(self, response):
        data = response.xpath('//div[@id="short_description_block"]')
        des = ""
        if len(data) >= 1:
            for d in data:
                try:
                    values = d.xpath('//div[@id="short_description_block"]/p/text()').extract()
                    for v in values:
                        des = des + v.strip()
                except:
                    values = d.xpath('//div[@id="short_description_block"]/p/span/text()').extract()
                    for v in values:
                        des = des + v.strip()
        else:
            des = None
        try:
            ref=response.xpath('//span[@class="editable"]/text()').extract()[0].strip()
        except:
            ref=None

        if (response.xpath('//span[@id="our_price_display"]/text()').extract()[0].strip()[:-1].find("/")):
            p = response.xpath('//span[@id="our_price_display"]/text()').extract()[0].split()[0].strip()[:-1]
        else:
            p = response.xpath('//span[@id="our_price_display"]/text()').extract()[0].strip()[:-1]
        yield {
            "url": response.url,

            "title": response.xpath('//h1[@class="heading"]/text()').extract()[0].strip(),

            "description": des,

            "categories": self.cat,

            "price": p,

            "currency": "EUR",

            "images": response.xpath('//ul[@id="thumbs_list_frame"]/li/a/img/@src').extract(),

            "extra": {
                "Référence":ref
            }}
        try:
            url = self.item_url.pop()
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
