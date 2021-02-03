from scrapy.http import JsonRequest
from time import sleep
import scrapy
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ladroSpider(scrapy.Spider):

    name = "ladrogueriedecharlotte"
    urls_vactor = [
        [["La sélection de Noël"], "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?CatID=3989892", 3],
        [["Les Jouets", "Les Animaux Sauteurs"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3974466&PBCATName=Les%20Animaux%20Sauteurs",
         1],
        [["Les Jouets", "Les autres"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3991033&PBCATName=Les%20autres",
         1],
        [["Les Jouets", "Les Jouets en Bois"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3974467&PBCATName=Les%20Jouets%20en%20Bois",
         3],
        [["Les Jouets", "Les Peluches"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3974469&PBCATName=Les%20Peluches",
         1],
        [["Les Jouets", "Les poupées"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3976874&PBCATName=Les%20poup%E9es",
         1],
        [["Les senteurs", "Les bougies parfumées"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3976928&PBCATName=Les%20bougies%20parfum%E9es",
         2],
        [["Les senteurs", "Les Parfums d'intérieur"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3983057&PBCATName=Les%20Parfums%20d%27int%E9rieur",
         1],
        [["Les senteurs", "Les recharges bouquets parfumés"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3983074&PBCATName=Les%20recharges%20bouquets%20parfum%E9s",
         1],
        [["Beauté & Bien-Être", "Hygiène"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3989131&PBCATName=Hygi%E8ne",
         1],
        [["Beauté & Bien-Être", "Savons"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3965537&PBCATName=Savons",
         1],
        [["Décoration", "Décoration de Noël"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3974455&PBCATName=D%E9coration%20de%20No%EBl",
         1],
        [["Décoration", "Décoration d'Intérieur"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3974470&PBCATName=D%E9coration%20d%27Int%E9rieur",
         1],
        [["La table", "Le Petit Electroménager"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3974449&PBCATName=Le%20Petit%20Electrom%E9nager",
         2],
        [["La table", "Le repas"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3965540&PBCATName=Le%20repas",
         1],
        [["La Cuisine & Ses ustensiles", "La Préparation"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3965541&PBCATName=La%20Pr%E9paration",
         2],
        [["La Cuisine & Ses ustensiles", "Le Petit électroménager"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3974448&PBCATName=Le%20Petit%20%E9lectrom%E9nager",
         2],
        [["La Vannerie", "Sacs"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3908469&PBCATName=Sacs",
         2],
        [["La droguerie", "L'entretien"],
         "https://www.ladrogueriedecharlotte.com/PBSCCatalog.asp?ActionID=67174912&PBCATID=3989893&PBCATName=L%27entretien",
         1]]

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

        if (self.page < self.total_page):
            self.driver.get(self.url)
            while True:
                try:
                    sleep(3)
                    urls = self.driver.find_elements_by_xpath('//*[contains(@class,"PBItemImg")]/a')
                    for u in urls:
                        self.item_url.append(u.get_attribute("href"))
                    next = self.driver.find_elements_by_xpath('//*[@class="navbar"]/ul/li/a')[self.page]
                    self.page = self.page + 1
                    next.click()
                except:
                    self.page = 0
                    break
        try:
            self.item_url = list(dict.fromkeys(self.item_url))
            url = self.item_url.pop()
            yield scrapy.Request(url,
                                 callback=self.parse_api_item,
                                 dont_filter=True)
        except:
            self.page = 0
            data = self.urls_vactor.pop()
            self.cat = data[0]
            self.url = data[1]
            self.total_page = data[2]
            yield scrapy.Request(self.url,
                                 callback=self.parse_api,
                                 dont_filter=True
                                 )

    def parse_api_item(self, response):
        try:
            data = response.xpath('//*[contains(@itemprop,"description")]/text()').extract()
            print(data)
            if (data[0] == '\r\n' or data[0] == " "):
                data = response.xpath('//*[contains(@itemprop,"description")]/p/span/text()').extract()
            des = ""
            if len(data) >= 1:
                for d in data:
                    des = des + d.strip()
            else:
                des = None
            data = response.xpath('//*[contains(@class,"ox-text__inner")]/div/text()').extract()
            detail = ""
            if len(data) >= 1:
                for d in data:
                    detail = detail + d.strip()
            else:
                detail = None
            yield {
                "url": response.url,

                "title": response.xpath('//*[contains(@class,"PBItemTitle")]/text()').extract()[0].strip(),

                "description": des,

                "categories": self.cat,

                "price": response.xpath('//*[contains(@class,"PBSalesPrice")]/text()').extract()[0][:-3].strip(),

                "currency": "EUR",

                "images": response.xpath('//*[contains(@itemprop,"image")]/@src').extract(),

                "extra": {
                    "detail": detail
                }}
        except:
            pass
        try:

            url = self.item_url.pop()
            yield JsonRequest(url,
                              callback=self.parse_api_item,
                              dont_filter=True)
        except:
            self.page = 0
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
