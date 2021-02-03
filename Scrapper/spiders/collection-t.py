from urllib.parse import urljoin
from scrapy.http import JsonRequest
import scrapy


class collectionSpider(scrapy.Spider):
    # proxy_pool = [os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE1'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE2'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE3'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE4')]
    name = "collection-t"
    urls_vactor = [[["thés"], "http://collection-t.fr/12-nos-thes", 5],
                   [["grands crus"], "http://collection-t.fr/73-nos-grands-crus", 1],
                   [["infusions"], "http://collection-t.fr/15-nos-infusions", 2],
                   [["accessoires"], "http://collection-t.fr/13-nos-accessoires", 3]]
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

    def parse_api(self, response):

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
        data = response.xpath('//div[@class="rte section-body"]/p/text()').extract()
        des = ""
        if len(data) >= 1:
            for d in data:
                des = des + d.strip()
        else:
            des = None

        yield {
            "url": response.url,

            "title": response.xpath('//h1[@itemprop="name"]/text()').extract()[0].strip(),

            "description": des,

            "categories": self.cat,

            "price": response.xpath('//div[@itemprop="price"]/text()').extract()[0].strip().split()[0],

            "currency": "EUR",

            "images": response.xpath('//ul[@id="thumbs_list_frame"]/li/a/img/@src').extract(),

            "extra": {

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
