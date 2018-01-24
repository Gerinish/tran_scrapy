# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

class CdeuukSpider(scrapy.Spider):
    name = 'cdeuuk'
    #allowed_domains = ['http://www.baidu.com']
    start_urls = ['http://europe.chinadaily.com.cn/59b908a5a3108c54ed7e1904']

    def parse(self, response):
        cd_st = response.text
        cd_st_soup = BeautifulSoup(cd_st, 'lxml')
        url = cd_st_soup.find('span', {'class': "tw3_01_2_p"}).find('a').get('href')
        yield scrapy.Request(url, callback=self.parseAgain)

    def parseAgain(self,response):
        cd_f = response.text
        cd_soup = BeautifulSoup(cd_f, 'lxml')
        text_all = cd_soup.find("h1").string + '\n'
        for child in cd_soup.body.find("div", {'id': "Content"}).find_all("p"):
            text_all += child.string + '\n'
        with open('cdeuuk.txt', 'w',encoding='utf-8',errors='ignore') as f:
            f.write(text_all)
        self.log('Saved file cdeuuk.')
        pass
