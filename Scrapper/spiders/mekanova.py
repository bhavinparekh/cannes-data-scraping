from urllib.parse import urljoin
from urllib.parse import urlparse
from scrapy.http import JsonRequest
import scrapy


class mekanovaSpider(scrapy.Spider):
    # proxy_pool = [os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE1'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE2'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE3'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE4')]
    name = "mekanova"
    urls_vactor = [
        'https://mekanova.art/?product_cat=alexis-carpentier',
        'https://mekanova.art/?product_cat=allain',
        'https://mekanova.art/?product_cat=allain-et-schull',
        'https://mekanova.art/?product_cat=amelie-sernis',
        'https://mekanova.art/?product_cat=arnus',
        'https://mekanova.art/?product_cat=aster-cassel',
        'https://mekanova.art/?product_cat=barbara-schull',
        'https://mekanova.art/?product_cat=chris-krainik',
        'https://mekanova.art/?product_cat=frank-eric-zeidler',
        'https://mekanova.art/?product_cat=juli-about',
        'https://mekanova.art/?product_cat=kartini-thomas',
        'https://mekanova.art/?product_cat=mathilde-oscar',
        'https://mekanova.art/?product_cat=olivia-paroldi',
        'https://mekanova.art/?product_cat=olivier-fonseca',
        'https://mekanova.art/?product_cat=richard-pellegrino',
        'https://mekanova.art/?product_cat=van-lith-et-buffile',
        'https://mekanova.art/?product_cat=animaliere',
        'https://mekanova.art/?product_cat=art-toys',
        'https://mekanova.art/?product_cat=contemporaine',
        'https://mekanova.art/?product_cat=ex-votos-coeurs',
        'https://mekanova.art/?product_cat=moderne',
        'https://mekanova.art/?product_cat=objets-de-curiosite',
        'https://mekanova.art/?product_cat=urbaine',
        'https://mekanova.art/?product_cat=assiettes-plats-saladiers',
        'https://mekanova.art/?product_cat=bols-tasses-mugs',
        'https://mekanova.art/?product_cat=boite',
        'https://mekanova.art/?product_cat=bougies',
        'https://mekanova.art/?product_cat=bouteilles-et-flacons',
        'https://mekanova.art/?product_cat=coupelles-plateaux',
        'https://mekanova.art/?product_cat=pichets',
        'https://mekanova.art/?product_cat=vases',
        'https://mekanova.art/?product_cat=dessins',
        'https://mekanova.art/?product_cat=estampes-urbaines',
        'https://mekanova.art/?product_cat=illustrations',
        'https://mekanova.art/?product_cat=photographies',
        'https://mekanova.art/?product_cat=alexis-carpentier-artisans',
        'https://mekanova.art/?product_cat=aurelie-sellin',
        'https://mekanova.art/?product_cat=barbara-schull-kraft',
        'https://mekanova.art/?product_cat=jonathan-reynaud',
        'https://mekanova.art/?product_cat=kathryn-oldfield',
        'https://mekanova.art/?product_cat=loupmana',
        'https://mekanova.art/?product_cat=severine-b-raku',
        'https://mekanova.art/?product_cat=art-prints',
        'https://mekanova.art/?product_cat=beautiful-bizarre',
        'https://mekanova.art/?product_cat=livres']

    url = ""
    cat = []
    item_url = []
    total_page = 1
    item = False
    page = 1

    def start_requests(self):
        data = self.urls_vactor.pop()
        self.url = data
        yield scrapy.Request(self.url,
                             callback=self.parse_api, dont_filter=True)

    def parse_api(self, response):
        data = response.xpath('//*[contains(@class,"woocommerce-LoopProduct-link")]/@href').extract()
        try:
            cat = response.xpath('//*[contains(@class,"woocommerce-breadcrumb")]/a/text()').extract()
            for i in cat[1:]:
                self.cat.append(i.strip())
        except:
            cat = response.xpath('//*[contains(@class,"woocommerce-breadcrumb")]/text()').extract()
            self.cat.append(cat)
        try:
            cat = response.xpath('//*[contains(@class,"woocommerce-breadcrumb")]/text()').extract()[1].strip()[
                  1:].strip()
            if (cat != '' and cat != "Page"):
                self.cat.append(cat)
        except:
            pass

        for d in data:
            self.item_url.append(d)

        try:
            url = response.xpath('//*[contains(@class,"next")]/@href').extract()[0]
            print(url)
            self.cat = []
            yield scrapy.Request(url,
                                 callback=self.parse_api, dont_filter=True)
        except:
            url = self.item_url.pop()
            yield scrapy.Request(url,
                                 callback=self.parse_api_item, dont_filter=True)

    def parse_api_item(self, response):
        data = response.xpath('//*[contains(@class,"et_pb_tab_content")]/p/text()').extract()
        des = ""
        if len(data) >= 1:
            for d in data:
                des = des + d.strip()
        else:
            des = None
        data = response.xpath('//*[contains(@class,"woocommerce-product-attributes-item__value")]/text()').extract()
        Poids = ""
        if len(data) >= 1:
            for d in data:
                Poids = Poids + d.strip()
        else:
            Poids = None

        yield {
            "url": response.url,

            "title": response.xpath('//*[contains(@class,"et_pb_module_inner")]/h1/text()').extract()[0].strip(),

            "description": des,

            "categories": self.cat,

            "price": response.xpath('//*[contains(@class,"woocommerce-Price-amount")]/bdi/text()').extract()[0],

            "currency": "EUR",

            "images": response.xpath('//*[contains(@class,"wp-post-image")]/@src').extract(),

            "extra": {
                "Poids": Poids
            }}

        try:
            url = self.item_url.pop()
            yield JsonRequest(url,
                              callback=self.parse_api_item,
                              dont_filter=True)
        except:

            data = self.urls_vactor.pop()
            self.cat = []
            self.url = data
            yield scrapy.Request(self.url,
                                 callback=self.parse_api,
                                 dont_filter=True
                                 )
            # ,
            # meta={'proxy': random.choice(self.proxy_pool)})
