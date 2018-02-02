# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re

class BbcbusinessSpider(scrapy.Spider):
    name = 'bbcbusiness'
    #allowed_domains = ['baidu.com']
    start_urls = ['http://www.bbc.com/news/business']

    def parse(self, response):     #找头条
        bbc_st = response.text
        bbc_st_soup = BeautifulSoup(bbc_st, 'lxml')
        txt_1 = bbc_st_soup.head.find('script',{'type':"application/ld+json"}).next_sibling.next_sibling.string
        url = 'http://www.bbc.com' + bbc_st_soup.find('a',{'class':'title-link'}).get("href")
        yield scrapy.Request(url, callback=self.parseAgain)

    def parseAgain(self, response):    #找文章
        bbc_f = response.text
        bbc_soup = BeautifulSoup(bbc_f, 'lxml')
        essay = bbc_soup.head.title.string + '\n'     #标题
        for i in bbc_soup.body.find('p',{"class":"story-body__introduction"}).previous_sibling.next_siblings:
            if i.name in ['h1','h2']:
                essay += '\n'
                essay = self.findText(essay,i)
            elif i.name == 'p':
                essay = self.findText(essay,i)
            #elif i.name == 'hr':
             #   if i.next_sibling.name in ['h1','h2','ul','li']:
             #       essay += '\n'
             #       essay = self.findText(essay, i)
             #   else:
             #       break
            else:
                continue
        with open('bbcbusiness.txt', 'w',encoding='utf-8',errors='ignore') as f:
            f.write(essay)
        self.log('Saved file bbcbusiness.')

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

