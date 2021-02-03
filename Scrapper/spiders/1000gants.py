from urllib.parse import urljoin
from scrapy.http import JsonRequest
import scrapy


class gantsSpider(scrapy.Spider):
    # proxy_pool = [os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE1'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE2'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE3'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE4')]
    name = "1000gants"
    urls_vactor = [[["Femme"], "https://www.1000gants.com/gants?f%5B0%5D=field_genre%3A3", 26],
                   [["Homme"], "https://www.1000gants.com/gants?f%5B0%5D=field_genre%3A4", 7],
                   [["NOUVEAUTÉS"], "https://www.1000gants.com/gants?f%5B0%5D=field_inspiration%3A13", 3],
                   [["PROMOTIONS"], "https://www.1000gants.com/gants?f%5B0%5D=field_inspiration%3A53", 1]]
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
        # ,
        # meta={'proxy': random.choice(self.proxy_pool)})

    def parse_api(self, response):
        print(self.page)

        data = response.css('figure.field-images a::attr(href)').extract()
        for d in data:
            self.item_url.append(d)
        if (self.page < self.total_page):
            self.page = self.page + 1
            url = self.url + "&page=" + str(self.page)
            yield scrapy.Request(url,
                                 callback=self.parse_api, dont_filter=True)
        else:
            url = self.item_url.pop()
            print(url)
            yield JsonRequest(urljoin('https://www.1000gants.com/', url),
                              callback=self.parse_api_item, dont_filter=True)

    def parse_api_item(self, response):
        data = response.css('div.field-body p:nth-child(1)::text')
        if len(data) >= 1:
            des = data.extract()[0].strip()
        else:
            des = None
        yield {
            "url": response.url,

            "title": response.css('div.product-left h1::text').extract()[0].strip(),

            "description": des,

            "categories": self.cat,

            "price":
                response.css('div.commerce-product-field div.field-commerce-price::text').extract()[0].strip().split()[
                    0],

            "currency": "EUR",

            "images": response.css('div.cloud-zoom-gallery-thumbs a::attr(href)').extract(),

            "extra": {

                "size": response.css('div.form-radios label.option::text').extract(),

                "marque": None

            }}

        try:
            url = self.item_url.pop()
            print(url)
            yield JsonRequest(urljoin('https://www.1000gants.com/', url),
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
