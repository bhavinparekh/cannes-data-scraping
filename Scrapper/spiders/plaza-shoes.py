from urllib.parse import urljoin
from scrapy.http import JsonRequest
import scrapy


class psSpider(scrapy.Spider):
    # proxy_pool = [os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE1'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE2'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE3'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE4')]
    name = "plaza-shoes"

    urls_vactor = [[["CHAUSSURES HOMMES "], "http://www.plaza-shoes.com/15-chaussures-hommes", 4],
                   [["ACCESSOIRES "], "http://www.plaza-shoes.com/23-accessoires", 2],
                   [["CARLOS SANTOS"],
                    "http://www.plaza-shoes.com/2_carlos-santos", 3]
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
                                  callback=self.parse_api_item, dont_filter=True)

    def parse_api_item(self, response):

        data = response.xpath('//div[@id="short_description_content"]/p/text()').extract()

        des = ""
        if len(data) >= 1:
            for d in data:
                des = des + d.strip()
        else:
            des = None
        try:
            size=response.css('select.attribute_select  option::text').extract()
        except:
            size=None
        yield {
            "url": response.url,

            "title": response.css('div.pb-center-column h1::text').extract()[0].strip(),

            "description": des,

            "categories": self.cat,

            "price": response.xpath('//span[@id="our_price_display"]/@content').extract()[0].strip(),

            "currency": "EUR",

            "images": response.xpath('//img[@id="bigpic"]/@src').extract(),

            "extra": {

                "État": response.css('span.editable::text').extract(),
                "Référence": response.xpath('//p[@id="product_reference"]/span/@content').extract(),
                "POINTURE": size

            }}
        try:
            url = self.item_url.pop()
            yield JsonRequest(url,
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
