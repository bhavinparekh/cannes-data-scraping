#!/bin/bash
rm -r stores
mynvidia() {

  (
    nvidia-smi -L
    nvidia-smi -q -d temperature | grep GPU
  ) |
    scrapy crawl 1000gants -o stores/1000gants.json &
  scrapy crawl boucherieagricoledelivery -o stores/boucherieagricoledelivery.json &
  scrapy crawl boutiqueonlyonemandelieu -o stores/boutiqueonlyonemandelieu.json &
  scrapy crawl cannolive -o stores/cannolive.json &
  scrapy crawl collection-t -o stores/collection_t.json &
  scrapy crawl couleursafran -o stores/couleursafran.json &
  scrapy crawl destination-bio -o stores/destination_bio.json &
  scrapy crawl districtcannes -o stores/districtcannes.json &
  scrapy crawl eden-park -o stores/eden_park.json &
  scrapy crawl gallico-fashion -o stores/gallico_fashion.json &
  scrapy crawl jeromedeoliveira -o stores/jeromedeoliveira.json &
  scrapy crawl ladrogueriedecharlotte -o stores/ladrogueriedecharlotte.json &
  scrapy crawl lagrandecoutellerie -o stores/lagrandecoutellerie.json &
  scrapy crawl lenotre -o stores/lenotre.json &
  scrapy crawl madeinrotin -o stores/madeinrotin.json &
  scrapy crawl manuelabiocca -o stores/manuelabiocca.json &
  scrapy crawl mavillemonshopping -o stores/mavillemonshopping.json &
  scrapy crawl mekanova -o stores/mekanova.json &
  scrapy crawl originesteaandcoffee -o stores/originesteaandcoffee.json &
  scrapy crawl peps-cannes -o stores/peps_cannes.json &
  scrapy crawl plaza-shoes -o stores/plaza-shoes.json &
}

str=$(mynvidia | grep "GPU $i:")
newstr=${str:49:2}
