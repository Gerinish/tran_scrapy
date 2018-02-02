# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

class CnnmoneySpider(scrapy.Spider):
    name = 'cnnmoney'
    #allowed_domains = ['baidu.com']
    start_urls = ['http://money.cnn.com/?iid=back_cnnmoney']

    def parse(self, response):
        cnn_st = response.text
        cnn_st_soup = BeautifulSoup(cnn_st, 'lxml')
        url = 'http://money.cnn.com' + cnn_st_soup.find("a",{"class":"title"}).get('href') + "?iid=hp-toplead-intl"
        yield scrapy.Request(url, callback=self.parseAgain)

    def parseAgain(self,response):
        cnn_f = response.text
        cnn_soup = BeautifulSoup(cnn_f, 'lxml')
        text_all = cnn_soup.find("h1",{'class':"article-title speakable"}).string + '\n'
        for i in cnn_soup.find('h2',{"class":"speakable"}).previous_sibling.next_siblings:
            if i.name == 'div':
                continue
            else:
                try:
                    text_all += i
                except:
                    for x in i.descendants:
                        try:
                            try:
                                if x.get('class') == 'inStoryHeading':   #此处换行应该多一行，失败
                                    text_all += '\n'
                            except:
                                pass
                            text_all += x
                        except:
                            continue
                    text_all += '\n'
        with open('cnnmoney.txt', 'w',encoding='utf-8',errors='ignore') as f:
            f.write(text_all)
        self.log('Saved file cnnmoney.')