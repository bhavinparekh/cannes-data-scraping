from time import sleep
import scrapy
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class edenSpider(scrapy.Spider):
    name = "eden-park"
    urls_vactor = [[["Enfant"], "https://www.eden-park.com/fr_fr/enfant.html"],
                   [["Homme"], "https://www.eden-park.com/fr_fr/homme.html"],
                   [["Femme"], "https://www.eden-park.com/fr_fr/femme.html"],
                   [["La décoration de maison"], "https://www.eden-park.com/fr_fr/maison.html"]]

    url = ""
    item_url = []
    item = False
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
            yield scrapy.Request(self.url,
                                 callback=self.parse_api,
                                 dont_filter=True)
            # ,
            # meta={'proxy': random.choice(self.proxy_pool)})
        except:
            pass

    def parse_api(self, response):

        self.driver.get(self.url)
        try:
            button = self.driver.find_element_by_css_selector("button.amgdprcookie-button")
            button.click()
        except:
            pass
        while True:
            try:
                sleep(1)
                urls = self.driver.find_elements_by_css_selector("a.product-item-slide")
                for u in urls:
                    self.item_url.append(u.get_attribute("href"))
                try:
                    next_page = self.driver.find_element_by_css_selector("li.pages-item-disabled a.next")
                    break
                except:
                    next_page = self.driver.find_element_by_css_selector("a.next")
                    self.driver.get(next_page.get_attribute("href"))
            except:
                break
        try:
            self.item_url = list(dict.fromkeys(self.item_url))
            url = self.item_url.pop()
            self.item_url.append(url)
            yield scrapy.Request(url,
                                 callback=self.parse_api_item,
                                 dont_filter=True)
        except:
            self.page = 0
            data = self.urls_vactor.pop()
            self.cat = data[0]
            self.url = data[1]

            yield scrapy.Request(self.url,
                                 callback=self.parse_api,
                                 dont_filter=True
                                 )

    def parse_api_item(self, response):
        product_url = list(dict.fromkeys(self.item_url))
        for url in product_url:
            self.driver.get(url)
            sleep(1)
            try:
                img = self.driver.find_elements_by_xpath("//img[@itemprop='image']")
                image = []
                for i in img:
                    image.append(i.get_attribute("src"))
                title = self.driver.find_element_by_xpath("//span[@itemprop='name']").text
            except:
                title = None
                image = None
            try:
                price = self.driver.find_element_by_xpath("//meta[@itemprop='price']").get_attribute("content")
            except:
                price = None
            try:
                des = self.driver.find_element_by_xpath("//div[@itemprop='description']/p/span").text
            except:
                des = None
            try:
                yield {"url": self.driver.current_url,

                       "title": title,

                       "description": des,

                       "categories": self.cat,

                       "price": price,

                       "currency": "EUR",

                       "images": image,

                       "extra": {

                       }}

            except:
                pass

        self.page = 0
        self.item_url = []
        data = self.urls_vactor.pop()
        self.cat = data[0]
        self.url = data[1]

        yield scrapy.Request(self.url,
                             callback=self.parse_api,
                             dont_filter=True)
