from urllib.parse import urljoin
from scrapy.http import JsonRequest
import scrapy



class gfeSpider(scrapy.Spider):
    # proxy_pool = [os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE1'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE2'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE3'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE4')]
    name = "gallico-fashion"
    allowed_domains = ['www.gallico-fashion.com']
    url="https://www.gallico-fashion.com/"
    item_url=[]
    item=False
    page=1
    catURL=""
    #,"52-cosmetique","59-idees-cadeaux"
    cat=["classical-h-back","classical-x-back","classical-y-back","creatives-voyages","no-buzz-airport-friendly","nœuds-papillon",
         "ceintures-sans-boucle","quick-fix","bretelles-pour-enfants","séries-limitées"]
    def start_requests(self):
        for i, url in enumerate(self.cat):

            yield scrapy.Request(self.url+url+"/", meta={'cookiejar': i},
                                     callback=self.parse_api)


    def parse_api(self, response):
        data = response.xpath('//div[@class="description"]/p/text()').extract()
        if len(data) >= 1:
            des = data[0].strip()
        else:
            des = None
        yield {
            "url": response.url,

            "title":  response.css('h4.fn::text').extract()[0].strip(),

            "description": des,

            "categories": None,

            "price":response.css('p.cc-shop-product-price-item::text').extract()[0].strip().split()[0],

            "currency": "EUR",

            "images": response.css('div.cc-m-gallery-cool-item div a img::attr(src)').extract(),

            "extra": {

                "verities":  response.css('select.cc-product-variant-selectbox option::text').extract()


            }}


