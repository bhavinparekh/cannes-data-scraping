from scrapy.http import JsonRequest
from time import sleep
import scrapy
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ladroSpider(scrapy.Spider):

    name = "lagrandecoutellerie"
    urls_vactor = [
        [["TABLE"], "https://www.lagrandecoutellerie.fr/fr/11-table", 25],
        [["CUISINE"], "https://www.lagrandecoutellerie.fr/fr/10-cuisine", 13],
        [["OUTDOOR"], "https://www.lagrandecoutellerie.fr/fr/15-couteaux-de-poche", 12],
        [["LUXE"], "https://www.lagrandecoutellerie.fr/fr/16-luxe", 3],
        [["CAVE"], "https://www.lagrandecoutellerie.fr/fr/17-cave", 4]]

    url = ""
    item_url = []
    item = False
    page = 0
    total_page = 1
    cat = []

    def __init__(self):
        chromedriver_autoinstaller.install()
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=options)
        self.driver.implicitly_wait(3)

    def start_requests(self):
        try:
            data = self.urls_vactor.pop()
            self.cat = data[0]
            self.url = data[1]
            self.total_page = data[2]
            yield scrapy.Request(self.url,
                                 callback=self.parse_api,
                                 dont_filter=True)
            # ,
            # meta={'proxy': random.choice(self.proxy_pool)})
        except:
            pass

    def parse_api(self, response):

        data = response.css('a.product-thumbnail::attr(href)').extract()
        for d in data:
            self.item_url.append(d)
        if (self.page < self.total_page):
            self.page = self.page + 1
            url = self.url + "?page=" + str(self.page)
            yield scrapy.Request(url,
                                 callback=self.parse_api)
        else:
            self.item_url = list(dict.fromkeys(self.item_url))
            url = self.item_url.pop()
            self.driver.get(url)
            try:
                sleep(1)
                button = self.driver.find_element_by_xpath('//*[contains(@class,"cookie_actions")]/div/input')
                button.click()
            except:
                pass
            while True:
                try:
                    sleep(1)

                    img = self.driver.find_elements_by_xpath('//*[contains(@class,"product-img")]/div/img')
                    imgs = []
                    for u in img:
                        imgs.append(u.get_attribute("src"))

                    data = self.driver.find_elements_by_xpath('//*[contains(@class,"description-block-1")]/p')
                    des = ""
                    for d in data:
                        try:
                            des = des + d.text
                        except:
                            des = des + d.find_elements_by_xpath(
                                '//*[contains(@class,"description-block-1")]/p/sapn').text

                    title = self.driver.find_element_by_xpath('//*[contains(@class,"product-page-title")]').text

                    price = \
                        self.driver.find_element_by_xpath('//*[contains(@class,"current-price")]/span').text.split()[0]

                    yield {
                        "url": self.driver.current_url,

                        "title": title,

                        "description": des,

                        "categories": self.cat,

                        "price": price,

                        "currency": "EUR",

                        "images": imgs,

                        "extra": {

                        }}
                    self.item_url = list(dict.fromkeys(self.item_url))
                    url = self.item_url.pop()
                    self.driver.get(url)
                except:
                    break
            self.page = 0
            data = self.urls_vactor.pop()
            self.cat = data[0]
            self.url = data[1]
            self.total_page = data[2]
            yield scrapy.Request(self.url,
                                 callback=self.parse_api,
                                 dont_filter=True
                                 )

    # def parse_api_item(self, response):
    #     try:
    #         data = response.xpath('//div[@product-img"]').extract()
    #         print(data)
    #         # if (data[0] == '\r\n' or data[0] == " "):
    #         #     data = response.xpath('//*[contains(@itemprop,"description")]/p/span/text()').extract()
    #         # des = ""
    #         # if len(data) >= 1:
    #         #     for d in data:
    #         #         des = des + d.strip()
    #         # else:
    #         #     des = None
    #         # data = response.xpath('//*[contains(@class,"ox-text__inner")]/div/text()').extract()
    #         # detail = ""
    #         # if len(data) >= 1:
    #         #     for d in data:
    #         #         detail = detail + d.strip()
    #         # else:
    #         #     detail = None
    #         # yield {
    #         #     "url": response.url,
    #         #
    #         #     "title": response.xpath('//*[contains(@class,"PBItemTitle")]/text()').extract()[0].strip(),
    #         #
    #         #     "description": des,
    #         #
    #         #     "categories": self.cat,
    #         #
    #         #     "price": response.xpath('//*[contains(@class,"PBSalesPrice")]/text()').extract()[0][:-3].strip(),
    #         #
    #         #     "currency": "EUR",
    #         #
    #         #     "images": response.xpath('//*[contains(@itemprop,"image")]/@src').extract(),
    #         #
    #         #     "extra": {
    #         #         "detail": detail
    #         #     }}
    #     except:
    #         pass
    #     try:
    #
    #         url = self.item_url.pop()
    #         yield JsonRequest(url,
    #                           callback=self.parse_api_item,
    #                           dont_filter=True)
    #     except:
    #         self.page = 1
    #         data = self.urls_vactor.pop()
    #         self.cat = data[0]
    #         self.url = data[1]
    #         self.total_page = data[2]
    #         yield scrapy.Request(self.url,
    #                              callback=self.parse_api,
    #                              dont_filter=True
    #                              )
    #     # ,
    #     # meta={'proxy': random.choice(self.proxy_pool)})
