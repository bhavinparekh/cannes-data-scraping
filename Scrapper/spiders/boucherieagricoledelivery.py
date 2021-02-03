from urllib.parse import urljoin
from scrapy.http import JsonRequest
import scrapy


class boucheriSpider(scrapy.Spider):
    # proxy_pool = [os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE1'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE2'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE3'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE4')]
    urls_vactor = [[["BOEUF"], "https://www.boucherieagricoledelivery.com/categorie/boeuf", 2],
                   [["VEAU"], "https://www.boucherieagricoledelivery.com/categorie/veau", 1],
                   [["AGNEAU"],
                    "https://www.boucherieagricoledelivery.com/categorie/vente-d-agneau-et-de-mouton-en-direct", 1],
                   [["PORC"], "https://www.boucherieagricoledelivery.com/categorie/porc", 1],
                   [["PORC IBERIQUE"], "https://www.boucherieagricoledelivery.com/categorie/porc-iberique", 1],
                   [["VOLAILLE"], "https://www.boucherieagricoledelivery.com/categorie/volaille", 1],
                   [["CHARCUTERIE"], "https://www.boucherieagricoledelivery.com/categorie/charcuterie", 2],
                   [["VIANDES D’EXCEPTION"], "https://www.boucherieagricoledelivery.com/categorie/viandes-d-exception",
                    1],
                   [["NOS SPÉCIALITÉS MAISON"],
                    "https://www.boucherieagricoledelivery.com/categorie/nos-specialites-maison", 1]
                   ]
    name = "boucherieagricoledelivery"
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

            data = response.css('a.product-image::attr(href)').extract()
            for d in data:
                self.item_url.append(d)
            if (self.page < self.total_page):
                self.page = self.page + 1
                url = self.url+"?p=" + str(self.page)
                yield scrapy.Request(url,
                                     callback=self.parse_api)
            else:
                self.item_url = list(dict.fromkeys(self.item_url))
                url = self.item_url.pop()
                print(url)
                yield JsonRequest(url,
                                  callback=self.parse_api_item)

    def parse_api_item(self, response):
        data = response.xpath('//div[@class="product-desc"]/p/text()').extract()
        des = ""
        if len(data) >= 1:
            for d in data:
                des = des + d.strip()
        else:
            des = None

        yield {
            "url": response.url,

            "title": response.xpath('//h1[@class="product-title"]/text()').extract()[0].strip(),

            "description": des,

            "categories": self.cat,

            "price": response.xpath('//span[@class="product-price"]/text()').extract()[0].strip().split()[0],

            "currency": "EUR",

            "images": list(dict.fromkeys(response.xpath('//img[@alt="product"]/@src').extract())),

            "extra": {

            }}

        try:
            url = self.item_url.pop()
            yield JsonRequest(url,
                              callback=self.parse_api_item)
        except:
            try:
                self.page=1
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
