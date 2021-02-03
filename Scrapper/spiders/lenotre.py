from urllib.parse import urljoin
from scrapy.http import JsonRequest
import scrapy

urls_vactor = [[["CADEAUX D'AFFAIRES"],
                "https://lenotre.com/index.php/espace-entreprises-lenotre/espace-entreprises-lenotre-cadeaux-d-affaires.html"],
               [["PAUSE COCKTAIL"],
                "https://lenotre.com/index.php/espace-entreprises-lenotre/espace-entreprises-lenotre-pause-cocktail.html"],
               [["Pâtisserie", "buches"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_noel_2020_produits_buches"],
               [["Pâtisserie", "patisseries individuelles"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_patisseries_individuelles"],
               [["Pâtisserie", "patisseries a partager"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_patisseries_a_partager"],
               [["Pâtisserie", "cocktail_sucre"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_cocktail_sucre"],
               [["Pâtisserie", "macarons"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_macarons"],
               [["Pâtisserie", "glaces"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_glaces"],
               [["galettes"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_noel_2020_produits_galettes"],
               [["Boulangerie", "viennoiseries"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_viennoiseries"],
               [["Boulangerie", "pain"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_pain"],
               [["Boulangerie", "teatime"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_teatime"],
               [["Traiteur", "cocktail sale"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_cocktail_sale"],
               [["Traiteur", "entrees"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_entrees"],
               [["Traiteur", "plats"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_plats"],
               [["Traiteur", "accompagnements"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_accompagnements"],
               [["Traiteur", "cocktail sucre"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_cocktail_sucre"],
               [["Confiserie", "macarons"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_macarons"],
               [["Confiserie", "chocolats"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_chocolats"],
               [["Confiserie", "autres gourmandises"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_autres_gourmandises"],
               [["Confiserie", "fruits"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_preparations_fruits"],
               [["A offrir", "carte cadeau"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_carte_cadeau"],
               [["A offrir", "macarons"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_macarons"],
               [["A offrir", "chocolats"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_chocolats"],
               [["Cave", "vins"], "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_vins"],
               [["Cave", "champagnes"],
                "https://lenotre.com/landing/index/ajax?blocid=landing_collection_produits_champagnes"]]


class lenSpider(scrapy.Spider):
    # proxy_pool = [os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE1'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE2'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE3'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE4')]
    name = "lenotre"
    url = ""
    cat = []
    item_url = []
    item = False
    page = 1

    def start_requests(self):
        try:
            data = urls_vactor.pop()
            self.cat = data[0]
            self.url = data[1]
            yield scrapy.Request(self.url,
                                 callback=self.parse_api,
                                 dont_filter=True)
            # ,
            # meta={'proxy': random.choice(self.proxy_pool)})
        except:
            pass

    def parse_api(self, response):
        if self.item == False:
            data = response.css('figcaption a::attr(href)').extract()
            for d in data:
                self.item_url.append(d)
            if (self.page < 1):
                self.page = self.page + 1
                url = self.url + str(self.page)
                yield scrapy.Request(url,
                                     callback=self.parse_api,
                                     dont_filter=True)
            else:
                self.item_url = list(dict.fromkeys(self.item_url))
                url = self.item_url.pop()
                yield JsonRequest(url,
                                  callback=self.parse_api_item,
                                  dont_filter=True)

    def parse_api_item(self, response):
        try:
            data = response.css('div.description p::text').extract()
            des = ""
            if len(data) >= 1:
                for d in data:
                    des = des + d.strip()
            else:
                des = None
            data = response.xpath('//div[@class="product-name"]/h1/text()').extract()
            if len(data) >= 1:
                tt = data[0].strip()
            else:
                tt = None
            data = response.css('span.price::text').extract()
            if len(data) >= 1:
                pri = data[0].strip().split()[0]
            else:
                pri = None
            data = response.css('span.sku::text').extract()
            if len(data) >= 1:
                ref = data[0].strip()
            else:
                ref = None
            if (tt != None):
                yield {
                    "url": response.url,

                    "title": tt,

                    "description": des,

                    "categories": self.cat,

                    "price": pri,

                    "currency": "EUR",

                    "images": response.css('img.gallery-image::attr(src)').extract(),

                    "extra": {
                        "reference": ref
                    }}
        except:
            print(Exception, "a")
        if (len(self.item_url) != 0):
            url = self.item_url.pop()
            yield JsonRequest(url,
                              callback=self.parse_api_item,
                              dont_filter=True)
        else:
            try:
                data = urls_vactor.pop()
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
