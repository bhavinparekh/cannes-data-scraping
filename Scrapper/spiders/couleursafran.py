from time import sleep
import scrapy
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class couleSpider(scrapy.Spider):
    # proxy_pool = [os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE1'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE2'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE3'),
    #               os.environ.get('LUM_CUSTOMER_HIVEWAY_ZONE_LAKETAHOE4')]
    name = "couleursafran"
    url = "https://www.couleursafran.com/boutique-couleur-safran.html"
    item_url = []
    item = False
    page = 1

    def __init__(self):
        chromedriver_autoinstaller.install()
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=options)
        self.driver.implicitly_wait(3)

    def start_requests(self):
        yield scrapy.Request(self.url,
                             callback=self.parse_api)

    def parse_api(self, response):

        product_url = []
        self.driver.get('https://www.couleursafran.com/boutique-couleur-safran.html')
        for i in range(3):

            url = self.driver.find_elements_by_css_selector("div.thumbnail a")
            for u in url:
                product_url.append(u.get_attribute("href"))

            try:
                next_page = self.driver.find_element_by_xpath("//a[@rel='next']")
                self.driver.get(next_page.get_attribute("href"))
            except:
                pass
        data = {}
        data[''] = []
        product_url = list(dict.fromkeys(product_url))
        for url in product_url:
            self.driver.get(url)
            sleep(1)

            try:
                img = self.driver.find_elements_by_css_selector('a.cboxElement')
                image = []
                for i in img:
                    image.append(i.get_attribute("href"))
                title = self.driver.find_element_by_xpath("//h1").text
            except:
                continue
            try:
                price = self.driver.find_element_by_xpath("//span[@class='tw-price']").text[:-1]
            except:
                price = None
            try:
                des = self.driver.find_element_by_xpath("//div[@class='ptext']/p").text
            except:
                try:
                    des = self.driver.find_element_by_xpath("//div[@class='ptext']/div").text
                except:
                    des = None
            try:
                yield {"url": url,

                       "title": title,

                       "description": des,

                       "categories": ["Boutique"],

                       "price": price,

                       "currency": "EUR",

                       "images": image,

                       "extra": {

                       }}

            except:
                pass
