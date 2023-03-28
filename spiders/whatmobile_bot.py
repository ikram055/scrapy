import scrapy
from termcolor import colored
from ..items import WhatmobileScrapperItem
from urllib.parse import urljoin


class WhatmobileBotSpider(scrapy.Spider):
    name = "whatmobile-bot"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.data = dict()
    start_urls = [
        "https://www.whatmobile.com.pk/"
    ]

    mobile_list = ["Samsung_Mobiles_Prices", "Huawei_Mobiles_Prices"]
    def parse(self, response):
        # Find all the links to the individual mobile pages
        for link in self.mobile_list:
            yield response.follow(urljoin(self.start_urls[0], link), self.parse_mobile_link)

    def parse_mobile_link(self, response):
        # Extract the name, OS, price, and rating of the mobile
        for mobile_link in response.css(".mobiles> .item a::attr(href)").extract():
            # Follow the link to the mobile page
            yield response.follow(mobile_link, self.parse_mobile)

    def parse_mobile(self, response):
        product = WhatmobileScrapperItem()

        item_name = str(response.css(
            "#centerContainer h1.hdng3::text").extract())
        
        item_price = response.css("#centerContainer > div > div:nth-child(2) > div > div.Heading1 > table:nth-child(3) > tbody > tr:nth-child(1) > td > strong:nth-child(1)::text").extract()

        self.data[item_name] = dict()
        temp = response.css("#centerContainer tbody tr ")
        for i in temp:
            name = i.css("td:not(:first-child)::text").extract()
            head = i.css("th::text").extract()

            if len(head) == 1 and len(name)==1:
                head,name = head[0],name[0]
            else:
                continue
            # if len(name) == 1:
            #     name = name[0]
            # else:
            #     continue

            self.data[item_name][head] = name
        product['name'] = item_name
        product['operating_system'] = self.data[item_name]["OS"]
        product['processor'] = self.data[item_name]["Chipset"]
        product['ram'] = self.data[item_name]['Built-in']
        product['Battery'] = self.data[item_name]['Capacity']
        product['Resolution'] = self.data[item_name]['Resolution']
        product['price'] = item_price

        yield product
