# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

class CdchinatopSpider(scrapy.Spider):
    name = 'cdchinatop'
    #allowed_domains = ['http://www.baidu.com']
    start_urls = ['http://www.chinadaily.com.cn/']

    def parse(self, response):
        cd_st = response.text
        cd_st_soup = BeautifulSoup(cd_st, 'lxml')
        url = cd_st_soup.find('div', {'class': "tmR"}).find('a').get('href')
        yield scrapy.Request(url, callback=self.parseAgain)

    def parseAgain(self,response):
        cd_f = response.text
        cd_soup = BeautifulSoup(cd_f, 'lxml')
        text_all = cd_soup.find("h1").string + '\n'
        for child in cd_soup.body.find("div", {'id': "Content"}).find_all("p"):
            text_all += child.string + '\n'
        if cd_soup.find('div',{"id":"Content"}).parent.get('class') == 'picshow' :      #图集式新闻的爬取无法做到
            url = cd_soup.find('div',{"class":"picshow"}).a.get('href')
            yield scrapy.Request(url,callback=self.parseAgain)
        with open('cdchinatop.txt', 'w',encoding='utf-8',errors='ignore') as f:
            f.write(text_all)
        self.log('Saved file cdchinatop.')
        pass
