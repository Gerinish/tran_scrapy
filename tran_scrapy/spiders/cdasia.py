# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import json


class CnntopSpider(scrapy.Spider):
    name = 'cdasia'
    #allowed_domains = ['http://www.baidu.com']
    start_urls = ['https://www.chinadailyhk.com/subjects/asia/list/asia_list.html']

    def parse(self, response):
        cd_st = response.text
        cd_st_soup = BeautifulSoup(cd_st, 'lxml')
        url ='https://www.chinadailyhk.com' + cd_st_soup.find('div', {'class': "am-slider-desc"}).a.get('href')
        yield scrapy.Request(url, callback=self.parseAgain)

    def parseAgain(self,response):
        cd_f = response.text
        cd_soup = BeautifulSoup(cd_f, 'lxml')
        text_all = cd_soup.find("div",{'class':"news-hd"}).h5.string + '\n'
        for child in cd_soup.body.find("div", {'class': "news-cut"}).children:
            if child.name != 'p':
                if child.name in ['h1','h2']:
                    text_all += '\n'
                    text_all = self.findText(text_all,child)
                else:
                    continue
            elif child.name == 'hr':
                if child.next_sibling.name in ['h1','h2']:
                    text_all += '\n'
                    text_all = self.findText(text_all, child)
                else:
                    break
            else:
                text_all = self.findText(text_all,child)
        with open('cdasia.txt', 'w',encoding='utf-8',errors='ignore') as f:
            f.write(text_all)
        self.log('Saved file cdasia.')

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