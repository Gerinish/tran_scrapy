# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

class CdbusinessSpider(scrapy.Spider):
    name = 'cdbusiness'
    #allowed_domains = ['baidu.com']
    start_urls = ['http://usa.chinadaily.com.cn/business']

    def parseAgain(self,response):#找文章
        cd_f = response.text
        cd_soup = BeautifulSoup(cd_f, 'lxml')
        text_all = cd_soup.find("div", {'class': "main_art"}).h1.string + '\n'
        for child in cd_soup.body.find("div", {'id': "Content"}).find_all("p"):
            text_all = self.findText(text_all,child)
        with open('cdbusiness.txt', 'w',encoding='utf-8',errors='ignore') as f:
            f.write(text_all)
        self.log('Saved file cdbusiness.')

    def parse(self, response):#找头条
        cd_st = response.text
        cd_st_soup = BeautifulSoup(cd_st,'lxml')
        url = cd_st_soup.find('div',{'class':"tmR"}).div.div.h1.a.get('href')
        yield scrapy.Request(url,callback=self.parseAgain)

    def findText(self,in_txt,in_soup):
        try:
            in_txt += '\n' + in_soup
        except:
            for x in in_soup.descendants:
                try:
                    in_txt += x
                except:
                    continue
            in_txt += '\n'
        return in_txt